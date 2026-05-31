"""Repository for blocked-request statistics."""
from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from backend.models.blocked_request import BlockedRequest


class StatsRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def record(self, req: BlockedRequest) -> BlockedRequest:
        self._db.add(req)
        self._db.commit()
        self._db.refresh(req)
        return req

    def total_blocked(self) -> int:
        return self._db.execute(select(func.count(BlockedRequest.id))).scalar_one()

    def blocked_today(self) -> int:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return self._db.execute(
            select(func.count(BlockedRequest.id)).where(BlockedRequest.blocked_at >= today)
        ).scalar_one()

    def top_domains(self, limit: int = 10) -> list[dict]:
        rows = self._db.execute(
            select(BlockedRequest.domain, func.count().label("count"))
            .group_by(BlockedRequest.domain)
            .order_by(func.count().desc())
            .limit(limit)
        ).all()
        return [{"domain": r.domain, "count": r.count} for r in rows]

    def daily_stats(self, days: int = 7) -> list[dict]:
        since = datetime.utcnow() - timedelta(days=days)
        rows = self._db.execute(
            select(
                func.date(BlockedRequest.blocked_at).label("date"),
                func.count().label("count"),
            )
            .where(BlockedRequest.blocked_at >= since)
            .group_by(func.date(BlockedRequest.blocked_at))
            .order_by(func.date(BlockedRequest.blocked_at))
        ).all()
        return [{"date": str(r.date), "count": r.count} for r in rows]

    def tracker_count(self) -> int:
        return self._db.execute(
            select(func.count(BlockedRequest.id)).where(BlockedRequest.is_tracker == True)  # noqa: E712
        ).scalar_one()
