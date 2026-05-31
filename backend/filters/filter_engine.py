"""
Central filter engine — singleton that owns the UrlMatcher and bridges DB + ML.

Pattern: service layer calls engine.check_url(); engine rebuilds from DB on demand.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Optional
from backend.filters.url_matcher import UrlMatcher

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    url: str
    domain: str
    blocked: bool
    matched_rule: Optional[str]
    is_tracker: bool
    ml_blocked: bool
    ml_confidence: Optional[float]


class FilterEngine:
    def __init__(self) -> None:
        self._matcher = UrlMatcher()
        self._loaded = False
        self._ml_predictor = None  # lazy-loaded to avoid circular import

    # ------------------------------------------------------------------ setup

    def load_from_db(self, rules: list) -> None:
        """Rebuild the in-memory matcher from DB rules."""
        self._matcher.rebuild_from_rules(rules)
        self._loaded = True
        logger.info(f"FilterEngine loaded {len(rules)} rules")

    def _get_ml_predictor(self):
        if self._ml_predictor is None:
            try:
                from ml_engine.predictor import AdPredictor
                self._ml_predictor = AdPredictor()
            except Exception as exc:
                logger.warning(f"ML predictor unavailable: {exc}")
        return self._ml_predictor

    # ------------------------------------------------------------------ check

    def check_url(self, url: str, enable_ml: bool = True) -> CheckResult:
        import tldextract
        ext = tldextract.extract(url)
        domain = f"{ext.subdomain}.{ext.domain}.{ext.suffix}".lstrip(".")

        blocked, matched = self._matcher.should_block(url)
        is_tracker = self._is_tracker_domain(domain)

        ml_blocked = False
        ml_confidence: Optional[float] = None

        if not blocked and enable_ml:
            predictor = self._get_ml_predictor()
            if predictor:
                try:
                    score = predictor.predict_proba(url)
                    from backend.config import get_settings
                    threshold = get_settings().ML_CONFIDENCE_THRESHOLD
                    if score >= threshold:
                        ml_blocked = True
                        ml_confidence = score
                        matched = f"ml:score={score:.3f}"
                        blocked = True
                except Exception as exc:
                    logger.debug(f"ML prediction error: {exc}")

        return CheckResult(
            url=url,
            domain=domain,
            blocked=blocked or is_tracker,
            matched_rule=matched,
            is_tracker=is_tracker,
            ml_blocked=ml_blocked,
            ml_confidence=ml_confidence,
        )

    # --------------------------------------------------------------- helpers

    # Well-known tracker TLDs / patterns — fast heuristic
    _TRACKER_KEYWORDS = frozenset([
        "doubleclick", "googlesyndication", "googletagmanager", "googletagservices",
        "googleanalytics", "analytics", "tracking", "tracker", "pixel", "beacon",
        "telemetry", "metric", "statistic", "adservice", "adnxs", "adsystem",
        "facebook.com/tr", "connect.facebook", "scorecardresearch", "quantserve",
        "hotjar", "mixpanel", "segment.io", "amplitude", "fullstory", "mouseflow",
        "crazyegg", "newrelic", "datadog", "sentry.io",
    ])

    def _is_tracker_domain(self, domain: str) -> bool:
        dl = domain.lower()
        return any(kw in dl for kw in self._TRACKER_KEYWORDS)
