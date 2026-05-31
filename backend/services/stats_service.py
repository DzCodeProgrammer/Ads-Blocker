"""Stats service — aggregates blocking statistics for the dashboard."""
from __future__ import annotations
from sqlalchemy.orm import Session
from backend.database.repositories.stats_repo import StatsRepository
from backend.database.repositories.filter_repo import FilterRepository


class StatsService:
    def __init__(self, db: Session) -> None:
        self._stats = StatsRepository(db)
        self._filter = FilterRepository(db)

    def get_summary(self) -> dict:
        return {
            "total_blocked": self._stats.total_blocked(),
            "blocked_today": self._stats.blocked_today(),
            "tracker_blocked": self._stats.tracker_count(),
            "rules_count": sum(self._filter.count_by_type().values()),
        }

    def get_top_domains(self, limit: int = 10) -> list[dict]:
        return self._stats.top_domains(limit=limit)

    def get_daily_stats(self, days: int = 7) -> list[dict]:
        return self._stats.daily_stats(days=days)

    def get_rules_breakdown(self) -> dict[str, int]:
        return self._filter.count_by_type()
