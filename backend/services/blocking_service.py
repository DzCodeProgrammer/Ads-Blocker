"""
Blocking service — application-layer facade between API routes and FilterEngine.

Responsibilities:
  • Own the FilterEngine singleton
  • Record each blocked request to DB
  • Reload engine when rules change
"""
from __future__ import annotations
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.filters.filter_engine import FilterEngine, CheckResult
from backend.models.blocked_request import BlockedRequest
from backend.database.repositories.filter_repo import FilterRepository
from backend.database.repositories.stats_repo import StatsRepository

logger = logging.getLogger(__name__)

# Module-level singleton so all requests share one compiled matcher
_engine = FilterEngine()


def get_engine() -> FilterEngine:
    return _engine


def reload_engine(db: Session) -> int:
    repo = FilterRepository(db)
    rules = repo.get_all_active()
    _engine.load_from_db(rules)
    return len(rules)


class BlockingService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._stats_repo = StatsRepository(db)

    def check_and_record(
        self,
        url: str,
        tab_url: str | None = None,
        enable_ml: bool = True,
    ) -> CheckResult:
        result = _engine.check_url(url, enable_ml=enable_ml)

        if result.blocked:
            entry = BlockedRequest(
                url=url[:4096],
                domain=result.domain[:512],
                rule_matched=result.matched_rule,
                is_tracker=result.is_tracker,
                is_ml_detected=result.ml_blocked,
                ml_confidence=result.ml_confidence,
                tab_url=(tab_url or "")[:4096],
                blocked_at=datetime.utcnow(),
            )
            self._stats_repo.record(entry)

        return result

    def add_custom_rule(self, pattern: str, rule_type_str: str, comment: str = "") -> None:
        from backend.models.filter_rule import FilterRule, RuleType
        rt = RuleType(rule_type_str)
        rule = FilterRule(
            pattern=pattern[:2048],
            rule_type=rt,
            source="custom",
            comment=comment or None,
        )
        repo = FilterRepository(self._db)
        repo.add(rule)
        reload_engine(self._db)

    def remove_rule(self, rule_id: int) -> bool:
        repo = FilterRepository(self._db)
        ok = repo.deactivate(rule_id)
        if ok:
            reload_engine(self._db)
        return ok
