"""
CNAME Uncloaking — detect trackers hidden behind first-party CNAME aliases.

Example: stats.myshop.com → CNAME → eu.metrics.tracker.io
DNS resolution reveals the real tracker domain behind the friendly alias.

Uses Cloudflare DNS-over-HTTPS (DoH) — no system DNS changes needed.
"""
from __future__ import annotations
import logging
import httpx
import tldextract

logger = logging.getLogger(__name__)

DOH_URL = "https://cloudflare-dns.com/dns-query"
MAX_DEPTH = 5

# Known tracker base domains (eTLD+1 level)
_TRACKER_BASE_DOMAINS = frozenset([
    "doubleclick.net", "googlesyndication.com", "googletagmanager.com",
    "facebook.com", "facebook.net", "connect.facebook.net",
    "scorecardresearch.com", "quantserve.com", "hotjar.com",
    "mixpanel.com", "segment.io", "segment.com", "amplitude.com",
    "fullstory.com", "mouseflow.com", "crazyegg.com",
    "newrelic.com", "datadoghq.com", "sentry.io",
    "adnxs.com", "rubiconproject.com", "pubmatic.com", "openx.net",
    "criteo.com", "criteo.net", "taboola.com", "outbrain.com",
    "moatads.com", "doubleverify.com", "adsrvr.org",
    "advertising.com", "yieldmanager.com", "casalemedia.com",
    "snap.licdn.com", "bat.bing.com", "chartbeat.com",
    "chartbeat.net", "optimizely.com", "vwo.com",
])


class CNAMEResolver:
    def __init__(self, timeout: int = 4) -> None:
        self._timeout = timeout
        self._cache: dict[str, str | None] = {}

    def resolve_cname_chain(self, domain: str, depth: int = 0) -> str | None:
        """Walk CNAME chain; return final real domain or None if no CNAME."""
        if depth >= MAX_DEPTH or not domain:
            return None
        if domain in self._cache:
            return self._cache[domain]

        cname_target = self._query_cname(domain)
        if not cname_target or cname_target == domain:
            self._cache[domain] = None
            return None

        # Recurse to follow chained CNAMEs
        deeper = self.resolve_cname_chain(cname_target, depth + 1)
        result = deeper or cname_target
        self._cache[domain] = result
        return result

    def check(self, domain: str) -> tuple[bool, str | None]:
        """
        Returns (is_cname_cloaked_tracker, real_domain).
        is_cname_cloaked=True only when the real domain is a known tracker.
        """
        real = self.resolve_cname_chain(domain)
        if not real:
            return False, None

        ext = tldextract.extract(real)
        base = f"{ext.domain}.{ext.suffix}"
        if base in _TRACKER_BASE_DOMAINS:
            logger.info(f"CNAME uncloaked: {domain} → {real}")
            return True, real

        # Also check keyword heuristics on the real domain
        real_lower = real.lower()
        tracker_kws = ["track", "analytics", "metric", "stat", "pixel", "beacon"]
        if any(kw in real_lower for kw in tracker_kws):
            return True, real

        return False, real

    def _query_cname(self, domain: str) -> str | None:
        try:
            with httpx.Client(timeout=self._timeout, follow_redirects=True) as client:
                resp = client.get(
                    DOH_URL,
                    params={"name": domain, "type": "CNAME"},
                    headers={"accept": "application/dns-json"},
                )
                resp.raise_for_status()
                data = resp.json()
                for ans in data.get("Answer", []):
                    if ans.get("type") == 5:  # CNAME record type
                        return ans["data"].rstrip(".")
        except Exception as exc:
            logger.debug(f"DoH query failed for {domain}: {exc}")
        return None
