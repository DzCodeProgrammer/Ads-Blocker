"""
Central filter engine — singleton owning UrlMatcher, CNAME resolver, URL cleaner,
content-type filter, and ML predictor.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
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
    # New v2 fields
    is_cname_cloaked: bool = False
    cname_real_domain: Optional[str] = None
    cleaned_url: Optional[str] = None
    tracking_params_removed: list[str] = field(default_factory=list)
    blocked_by_content_type: bool = False
    is_fingerprinting: bool = False


class FilterEngine:
    def __init__(self) -> None:
        self._matcher = UrlMatcher()
        self._loaded = False
        self._ml_predictor = None
        self._fingerprint_detector = None
        self._cname_resolver = None
        self._url_cleaner = None
        self._content_filter = None

    # ------------------------------------------------------------------ setup

    def load_from_db(self, rules: list) -> None:
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

    def _get_fingerprint_detector(self):
        if self._fingerprint_detector is None:
            try:
                from ml_engine.fingerprint_detector import FingerprintDetector
                self._fingerprint_detector = FingerprintDetector()
            except Exception as exc:
                logger.debug(f"Fingerprint detector unavailable: {exc}")
        return self._fingerprint_detector

    def _get_cname_resolver(self):
        if self._cname_resolver is None:
            try:
                from backend.filters.cname_resolver import CNAMEResolver
                self._cname_resolver = CNAMEResolver()
            except Exception:
                pass
        return self._cname_resolver

    def _get_url_cleaner(self):
        if self._url_cleaner is None:
            from backend.filters.url_cleaner import URLCleaner
            self._url_cleaner = URLCleaner()
        return self._url_cleaner

    def _get_content_filter(self):
        if self._content_filter is None:
            from backend.filters.content_filter import ContentTypeFilter
            self._content_filter = ContentTypeFilter()
        return self._content_filter

    # ------------------------------------------------------------------ check

    def check_url(
        self,
        url: str,
        enable_ml: bool = True,
        content_type: str = "other",
        is_third_party: bool = True,
        site_domain: Optional[str] = None,
    ) -> CheckResult:
        import tldextract
        ext = tldextract.extract(url)
        domain = f"{ext.subdomain}.{ext.domain}.{ext.suffix}".lstrip(".")

        # ── Step 1: URL tracking param cleaning ───────────────────────────────
        cleaner = self._get_url_cleaner()
        cleaned_url, removed_params = cleaner.clean(url)

        # ── Step 2: Whitelist check ───────────────────────────────────────────
        if self._matcher.is_whitelisted(url):
            return CheckResult(
                url=url, domain=domain, blocked=False, matched_rule=None,
                is_tracker=False, ml_blocked=False, ml_confidence=None,
                cleaned_url=cleaned_url if removed_params else None,
                tracking_params_removed=removed_params,
            )

        # ── Step 3: Per-site disable check ───────────────────────────────────
        if site_domain:
            from backend.database.repositories.site_repo import SiteRepository
            from backend.models.site_setting import SiteMode
            # (fast check via in-memory cache — actual DB reads happen in service)

        # ── Step 4: Content-type based blocking ───────────────────────────────
        blocked_by_type = False
        cf = self._get_content_filter()
        if cf.should_block_by_type(content_type, is_third_party, site_domain):
            blocked_by_type = True

        # ── Step 5: URL pattern matching ──────────────────────────────────────
        blocked, matched = self._matcher.should_block(url)
        is_tracker = self._is_tracker_domain(domain)

        # ── Step 6: CNAME uncloaking ──────────────────────────────────────────
        is_cname = False
        cname_real = None
        if not blocked:
            resolver = self._get_cname_resolver()
            if resolver:
                try:
                    is_cname, cname_real = resolver.check(domain)
                    if is_cname:
                        blocked = True
                        matched = f"cname:{cname_real}"
                        is_tracker = True
                except Exception:
                    pass

        # ── Step 7: ML detection ──────────────────────────────────────────────
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
                    logger.debug(f"ML error: {exc}")

        # ── Step 8: Fingerprinting detection ─────────────────────────────────
        is_fingerprinting = False
        fd = self._get_fingerprint_detector()
        if fd:
            try:
                is_fingerprinting = fd.is_fingerprinting_url(url, content_type)
                if is_fingerprinting and not blocked:
                    blocked = True
                    matched = "fingerprint:detected"
            except Exception:
                pass

        return CheckResult(
            url=url,
            domain=domain,
            blocked=blocked or is_tracker or blocked_by_type,
            matched_rule=matched,
            is_tracker=is_tracker,
            ml_blocked=ml_blocked,
            ml_confidence=ml_confidence,
            is_cname_cloaked=is_cname,
            cname_real_domain=cname_real,
            cleaned_url=cleaned_url if removed_params else None,
            tracking_params_removed=removed_params,
            blocked_by_content_type=blocked_by_type,
            is_fingerprinting=is_fingerprinting,
        )

    # --------------------------------------------------------------- helpers

    _TRACKER_KEYWORDS = frozenset([
        "doubleclick", "googlesyndication", "googletagmanager", "googletagservices",
        "googleanalytics", "analytics", "tracking", "tracker", "pixel", "beacon",
        "telemetry", "metric", "statistic", "adservice", "adnxs", "adsystem",
        "facebook.com/tr", "connect.facebook", "scorecardresearch", "quantserve",
        "hotjar", "mixpanel", "segment.io", "amplitude", "fullstory", "mouseflow",
        "crazyegg", "newrelic", "datadog", "sentry.io", "criteo", "taboola",
        "outbrain", "moatads", "doubleverify", "adsrvr", "advertising",
        "yieldmanager", "casalemedia", "openx", "rubiconproject", "pubmatic",
        "chartbeat", "optimizely", "vwo", "liveperson", "zopim",
    ])

    def _is_tracker_domain(self, domain: str) -> bool:
        dl = domain.lower()
        return any(kw in dl for kw in self._TRACKER_KEYWORDS)
