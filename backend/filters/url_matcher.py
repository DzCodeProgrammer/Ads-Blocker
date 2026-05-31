"""
Fast URL matching engine.

Uses three data structures for O(1) / O(log n) lookups:
  1. Exact-domain set — fastest path
  2. Suffix trie (dict) — matches subdomains
  3. Regex list — slowest, only for regex rules
"""
from __future__ import annotations
import re
import tldextract
from typing import Optional


class UrlMatcher:
    def __init__(self) -> None:
        self._exact: set[str] = set()
        self._suffix: set[str] = set()       # eTLD+1 keys
        self._substrings: list[str] = []
        self._regexes: list[re.Pattern] = []
        self._whitelist: set[str] = set()    # whitelisted eTLD+1 domains

    # ------------------------------------------------------------------ build

    def add_domain(self, domain: str, is_whitelist: bool = False) -> None:
        domain = domain.lower().strip(".")
        if is_whitelist:
            self._whitelist.add(domain)
            return
        extracted = tldextract.extract(domain)
        if extracted.subdomain:
            self._exact.add(domain)
        self._suffix.add(f"{extracted.domain}.{extracted.suffix}")

    def add_substring(self, pattern: str) -> None:
        self._substrings.append(pattern.lower())

    def add_regex(self, pattern: str) -> None:
        try:
            self._regexes.append(re.compile(pattern, re.IGNORECASE))
        except re.error:
            pass  # silently skip malformed regex rules

    def rebuild_from_rules(self, rules) -> None:
        """Populate matcher from a list of FilterRule ORM objects."""
        self._exact.clear()
        self._suffix.clear()
        self._substrings.clear()
        self._regexes.clear()
        self._whitelist.clear()

        from backend.models.filter_rule import RuleType

        for rule in rules:
            is_wl = rule.rule_type == RuleType.WHITELIST
            if rule.is_regex:
                if not is_wl:
                    self.add_regex(rule.pattern)
            elif "." in rule.pattern and "/" not in rule.pattern:
                self.add_domain(rule.pattern, is_whitelist=is_wl)
            else:
                if not is_wl:
                    self.add_substring(rule.pattern)

    # ----------------------------------------------------------------- match

    def is_whitelisted(self, url: str) -> bool:
        domain = self._extract_domain(url)
        ext = tldextract.extract(domain)
        etld1 = f"{ext.domain}.{ext.suffix}"
        return domain in self._whitelist or etld1 in self._whitelist

    def should_block(self, url: str) -> tuple[bool, Optional[str]]:
        """Returns (block, matched_pattern)."""
        if self.is_whitelisted(url):
            return False, None

        url_lower = url.lower()
        domain = self._extract_domain(url_lower)
        ext = tldextract.extract(domain)
        etld1 = f"{ext.domain}.{ext.suffix}"

        if domain in self._exact:
            return True, domain
        if etld1 in self._suffix:
            return True, etld1

        for sub in self._substrings:
            if sub in url_lower:
                return True, sub

        for rx in self._regexes:
            m = rx.search(url_lower)
            if m:
                return True, rx.pattern

        return False, None

    @staticmethod
    def _extract_domain(url: str) -> str:
        try:
            # Strip protocol
            if "://" in url:
                url = url.split("://", 1)[1]
            domain = url.split("/")[0].split("?")[0].split(":")[0]
            return domain.lower()
        except Exception:
            return url
