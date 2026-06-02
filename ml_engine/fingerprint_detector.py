"""
Fingerprinting Detector — identify URLs serving browser fingerprinting scripts.

Detects:
  - Canvas fingerprinting libraries (fingerprintjs, clientjs, etc.)
  - WebGL fingerprinting
  - AudioContext fingerprinting
  - Battery API, navigator property harvesting
  - Known fingerprinting service domains
"""
from __future__ import annotations
import re
import tldextract

# Known fingerprinting library URL patterns
_FP_URL_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.IGNORECASE) for p in [
        r"fingerprintjs",
        r"fingerprint\.pro",
        r"fpjs\.io",
        r"clientjs",
        r"device-detect",
        r"bowser\.js",
        r"platform\.js",
        r"ua-parser",
        r"detectbrowser",
        r"evercookie",
        r"zombie\.cookie",
        r"supercookie",
        r"canvas[_\-]fingerprint",
        r"webgl[_\-]fingerprint",
        r"audio[_\-]fingerprint",
        r"font[_\-]detect",
        r"human\.js",
        r"threatmetrix",
        r"iovation",
        r"deviceatlas",
        r"wurfl",
        r"51degrees",
    ]
]

# Domains known to serve fingerprinting code
_FP_DOMAINS = frozenset([
    "fingerprint.com", "fpjs.io", "fingerprintjs.com",
    "threatmetrix.com", "iovation.com", "deviceatlas.com",
    "51degrees.com", "wurfl.io", "evercookie.com",
    "tealiumiq.com", "rlcdn.com",  # customer data platforms with heavy FP
    "turn.com", "bluekai.com", "exelate.com",  # data brokers
    "krxd.net", "agkn.com", "brsrvr.com",
])

# Content types that would carry fingerprinting scripts
_SCRIPT_TYPES = frozenset(["script", "xmlhttprequest", "other"])


class FingerprintDetector:
    """Lightweight rule-based fingerprinting URL detector."""

    def is_fingerprinting_url(self, url: str, content_type: str = "other") -> bool:
        if content_type not in _SCRIPT_TYPES:
            return False

        url_lower = url.lower()

        # Check URL patterns
        if any(p.search(url_lower) for p in _FP_URL_PATTERNS):
            return True

        # Check domain
        ext = tldextract.extract(url)
        base = f"{ext.domain}.{ext.suffix}"
        if base in _FP_DOMAINS:
            return True

        # Check for combined fingerprinting signals in path
        path_lower = url_lower.split("?")[0]
        fp_signals = ["canvas", "webgl", "audio", "battery", "navigator", "screen"]
        hits = sum(1 for s in fp_signals if s in path_lower)
        if hits >= 2:
            return True

        return False

    def score(self, url: str) -> float:
        """Return fingerprinting likelihood [0, 1]."""
        url_lower = url.lower()
        score = 0.0

        pattern_hits = sum(1 for p in _FP_URL_PATTERNS if p.search(url_lower))
        score += min(pattern_hits * 0.4, 0.8)

        ext = tldextract.extract(url)
        if f"{ext.domain}.{ext.suffix}" in _FP_DOMAINS:
            score += 0.5

        fp_signals = ["canvas", "webgl", "audio", "battery", "navigator", "screen"]
        signal_hits = sum(1 for s in fp_signals if s in url_lower)
        score += signal_hits * 0.05

        return min(score, 1.0)
