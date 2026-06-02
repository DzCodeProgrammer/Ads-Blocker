"""
Behavioral Analyzer — detect suspicious request patterns for a browsing session.

Analyzes sequences of requests to identify:
  - Redirect chains typical of ad tracking
  - High-frequency beacon pings
  - Pixel chain patterns (1x1 image sequences to multiple domains)
  - Suspiciously coordinated XHR bursts (tracker sync)
"""
from __future__ import annotations
import logging
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class RequestEvent:
    url: str
    domain: str
    content_type: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BehavioralSignal:
    suspicious: bool
    reason: str
    confidence: float  # [0, 1]
    domains_involved: list[str] = field(default_factory=list)


class BehavioralAnalyzer:
    """
    Stateful per-tab analyzer — call record() on each request,
    then analyze() to get a BehavioralSignal.
    """

    # Thresholds
    PING_BURST_THRESHOLD = 5     # pings to distinct domains within 5s → suspicious
    REDIRECT_CHAIN_THRESHOLD = 4  # 4+ redirects → suspicious
    PIXEL_BURST_THRESHOLD = 6    # 6+ image requests to distinct ad-ish domains

    def __init__(self, window_seconds: int = 30) -> None:
        self._window = timedelta(seconds=window_seconds)
        self._events: deque[RequestEvent] = deque(maxlen=500)
        self._domain_counts: dict[str, int] = defaultdict(int)

    def record(self, url: str, domain: str, content_type: str) -> None:
        now = datetime.utcnow()
        # Prune old events outside window
        cutoff = now - self._window
        while self._events and self._events[0].timestamp < cutoff:
            old = self._events.popleft()
            self._domain_counts[old.domain] -= 1

        ev = RequestEvent(url=url, domain=domain, content_type=content_type)
        self._events.append(ev)
        self._domain_counts[domain] += 1

    def analyze(self) -> BehavioralSignal:
        if not self._events:
            return BehavioralSignal(suspicious=False, reason="no data", confidence=0.0)

        ping_domains = {
            e.domain for e in self._events
            if e.content_type in ("ping", "xmlhttprequest") and self._is_ad_domain(e.domain)
        }
        if len(ping_domains) >= self.PING_BURST_THRESHOLD:
            return BehavioralSignal(
                suspicious=True,
                reason=f"Tracker sync burst: {len(ping_domains)} tracker XHR domains",
                confidence=0.85,
                domains_involved=list(ping_domains)[:10],
            )

        pixel_domains = {
            e.domain for e in self._events
            if e.content_type == "image" and self._is_ad_domain(e.domain)
        }
        if len(pixel_domains) >= self.PIXEL_BURST_THRESHOLD:
            return BehavioralSignal(
                suspicious=True,
                reason=f"Pixel tracking burst: {len(pixel_domains)} tracking pixel domains",
                confidence=0.75,
                domains_involved=list(pixel_domains)[:10],
            )

        # Redirect chain: many different domains visited quickly
        if len(self._domain_counts) >= self.REDIRECT_CHAIN_THRESHOLD:
            redirect_like = [
                d for d, c in self._domain_counts.items()
                if c == 1 and self._is_ad_domain(d)
            ]
            if len(redirect_like) >= self.REDIRECT_CHAIN_THRESHOLD:
                return BehavioralSignal(
                    suspicious=True,
                    reason=f"Redirect chain through {len(redirect_like)} ad domains",
                    confidence=0.70,
                    domains_involved=redirect_like[:10],
                )

        return BehavioralSignal(suspicious=False, reason="normal", confidence=0.0)

    def reset(self) -> None:
        self._events.clear()
        self._domain_counts.clear()

    @staticmethod
    def _is_ad_domain(domain: str) -> bool:
        dl = domain.lower()
        keywords = [
            "ad", "track", "pixel", "beacon", "metric", "analytics",
            "stat", "click", "impression", "sync", "partner", "affiliate",
        ]
        return any(kw in dl for kw in keywords)
