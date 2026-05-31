"""
Parse EasyList / uBlock-style ABP filter syntax into normalised FilterRule objects.

Supported syntax:
  ||example.com^          — domain block
  @@||example.com^        — exception / whitelist
  ##.ad-banner            — cosmetic (element-hide) rule
  ! comment               — ignored
  [Adblock Plus ...]      — header line, ignored
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedRule:
    raw: str
    pattern: str
    is_exception: bool = False
    is_cosmetic: bool = False
    is_regex: bool = False
    options: dict = field(default_factory=dict)
    domains: list[str] = field(default_factory=list)


_OPTION_RE = re.compile(r"\$([^$]+)$")
_DOMAIN_ANCHOR = re.compile(r"^\|\|(.+?)\^?$")


class EasyListParser:
    """Stateless parser — returns a list of ParsedRule for a raw filter-list string."""

    def parse(self, raw_text: str) -> list[ParsedRule]:
        rules: list[ParsedRule] = []
        for line in raw_text.splitlines():
            rule = self._parse_line(line.strip())
            if rule:
                rules.append(rule)
        return rules

    def _parse_line(self, line: str) -> Optional[ParsedRule]:
        if not line or line.startswith("!") or line.startswith("[Adblock"):
            return None

        # Cosmetic / element-hide rules  e.g. example.com##.ad
        if "##" in line or "#@#" in line:
            return ParsedRule(raw=line, pattern=line, is_cosmetic=True)

        is_exception = line.startswith("@@")
        if is_exception:
            line = line[2:]

        # Strip inline options  e.g. ||ads.com^$third-party,script
        options: dict[str, str] = {}
        m = _OPTION_RE.search(line)
        if m:
            options = self._parse_options(m.group(1))
            line = line[: m.start()]

        # Normalise domain-anchor syntax  ||ads.example.com^ → ads.example.com
        dm = _DOMAIN_ANCHOR.match(line)
        if dm:
            pattern = dm.group(1).rstrip("^/")
            return ParsedRule(
                raw=line,
                pattern=pattern,
                is_exception=is_exception,
                options=options,
            )

        # Regex rule  e.g. /ads\d+\.js/
        if line.startswith("/") and line.endswith("/"):
            return ParsedRule(
                raw=line,
                pattern=line[1:-1],
                is_exception=is_exception,
                is_regex=True,
                options=options,
            )

        # Plain substring / wildcard rule
        pattern = line.strip("|").strip("^")
        return ParsedRule(
            raw=line,
            pattern=pattern,
            is_exception=is_exception,
            options=options,
        )

    @staticmethod
    def _parse_options(opts_str: str) -> dict[str, str]:
        result: dict[str, str] = {}
        for part in opts_str.split(","):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                result[k] = v
            elif part.startswith("~"):
                result[part[1:]] = "exclude"
            else:
                result[part] = "include"
        return result
