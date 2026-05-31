"""
Filter list updater — fetches remote lists, parses them, and persists to DB.
Scheduled via APScheduler (called from update_service.py).
"""
from __future__ import annotations
import logging
import httpx
from backend.filters.easylist_parser import EasyListParser, ParsedRule
from backend.models.filter_rule import FilterRule, RuleType

logger = logging.getLogger(__name__)

# Remote list → RuleType mapping
FILTER_SOURCES: dict[str, RuleType] = {}


def build_sources(settings) -> dict[str, RuleType]:
    return {
        settings.EASYLIST_URL: RuleType.EASYLIST,
        settings.EASYPRIVACY_URL: RuleType.EASYPRIVACY,
        settings.UBLOCK_URL: RuleType.UBLOCK,
    }


class FilterUpdater:
    def __init__(self) -> None:
        self._parser = EasyListParser()

    def fetch_raw(self, url: str, timeout: int = 30) -> str:
        """Download a filter list. Returns empty string on failure."""
        try:
            with httpx.Client(timeout=timeout, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except Exception as exc:
            logger.error(f"Failed to fetch {url}: {exc}")
            return ""

    def parse_to_rules(
        self, raw: str, rule_type: RuleType, source_url: str
    ) -> list[FilterRule]:
        parsed: list[ParsedRule] = self._parser.parse(raw)
        rules: list[FilterRule] = []
        for p in parsed:
            if p.is_cosmetic or not p.pattern:
                continue
            rt = RuleType.WHITELIST if p.is_exception else rule_type
            rules.append(
                FilterRule(
                    pattern=p.pattern[:2048],
                    rule_type=rt,
                    source=source_url,
                    is_regex=p.is_regex,
                )
            )
        return rules

    def update_all(self, db_session, settings) -> dict[str, int]:
        """Fetch all remote lists, wipe old entries, insert new ones."""
        from backend.database.repositories.filter_repo import FilterRepository
        repo = FilterRepository(db_session)
        sources = build_sources(settings)
        counts: dict[str, int] = {}

        for url, rule_type in sources.items():
            logger.info(f"Updating filter list: {url}")
            raw = self.fetch_raw(url)
            if not raw:
                counts[url] = 0
                continue
            rules = self.parse_to_rules(raw, rule_type, url)
            deleted = repo.delete_by_source(url)
            inserted = repo.bulk_insert(rules)
            logger.info(f"  {url}: deleted={deleted}, inserted={inserted}")
            counts[url] = inserted

        return counts
