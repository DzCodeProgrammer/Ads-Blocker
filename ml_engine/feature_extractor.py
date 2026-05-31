"""
Feature extraction from URLs for the ad-detection ML classifier.

Features extracted:
  - Lexical: URL length, token counts, entropy
  - Domain: TLD type, subdomain depth, digit ratio
  - Path: path depth, file extension, query param count
  - Keyword: presence of known ad/tracker keywords
"""
from __future__ import annotations
import math
import re
from urllib.parse import urlparse, parse_qs
import tldextract

_AD_KEYWORDS = [
    "ad", "ads", "advert", "banner", "track", "tracker", "pixel", "beacon",
    "analytics", "metric", "stat", "click", "impression", "sponsor", "promo",
    "campaign", "affiliate", "partner", "remarketing", "retarget",
]

_SUSPICIOUS_TLDS = {"xyz", "top", "click", "download", "stream", "loan", "work"}


def _shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def _digit_ratio(s: str) -> float:
    if not s:
        return 0.0
    return sum(1 for c in s if c.isdigit()) / len(s)


def _count_ad_keywords(text: str) -> int:
    t = text.lower()
    return sum(1 for kw in _AD_KEYWORDS if kw in t)


class FeatureExtractor:
    """Transforms a raw URL string into a fixed-length numeric feature vector."""

    FEATURE_NAMES = [
        "url_length",
        "domain_length",
        "path_length",
        "query_length",
        "subdomain_depth",
        "path_depth",
        "query_param_count",
        "digit_ratio_domain",
        "digit_ratio_path",
        "url_entropy",
        "domain_entropy",
        "has_ip_address",
        "has_port",
        "suspicious_tld",
        "ad_keyword_count_domain",
        "ad_keyword_count_path",
        "has_redirect_param",
        "hyphen_count",
        "dot_count_subdomain",
        "long_subdomain",
    ]

    _IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    _REDIRECT_PARAMS = frozenset(["url", "redirect", "goto", "next", "redir", "out"])

    def extract(self, url: str) -> list[float]:
        parsed = urlparse(url)
        ext = tldextract.extract(url)

        netloc = parsed.netloc or ""
        domain = f"{ext.domain}.{ext.suffix}"
        subdomain = ext.subdomain or ""
        path = parsed.path or ""
        query = parsed.query or ""
        params = parse_qs(query)

        has_port = int(":" in netloc and not netloc.startswith("["))
        has_ip = int(bool(self._IP_RE.match(ext.domain)))
        suspicious_tld = int(ext.suffix.lstrip(".") in _SUSPICIOUS_TLDS)
        has_redirect = int(bool(params.keys() & self._REDIRECT_PARAMS))
        long_subdomain = int(len(subdomain) > 30)

        return [
            len(url),                              # url_length
            len(domain),                           # domain_length
            len(path),                             # path_length
            len(query),                            # query_length
            subdomain.count(".") + 1 if subdomain else 0,  # subdomain_depth
            path.count("/"),                       # path_depth
            len(params),                           # query_param_count
            _digit_ratio(domain),                  # digit_ratio_domain
            _digit_ratio(path),                    # digit_ratio_path
            _shannon_entropy(url),                 # url_entropy
            _shannon_entropy(domain),              # domain_entropy
            has_ip,                                # has_ip_address
            has_port,                              # has_port
            suspicious_tld,                        # suspicious_tld
            _count_ad_keywords(domain),            # ad_keyword_count_domain
            _count_ad_keywords(path),              # ad_keyword_count_path
            has_redirect,                          # has_redirect_param
            url.count("-"),                        # hyphen_count
            subdomain.count("."),                  # dot_count_subdomain
            long_subdomain,                        # long_subdomain
        ]

    def extract_batch(self, urls: list[str]) -> list[list[float]]:
        return [self.extract(u) for u in urls]
