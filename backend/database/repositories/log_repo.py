"""Repository for NetworkLog — the real-time request log."""
from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, func
from backend.models.network_log import NetworkLog, RequestStatus


class LogRepository:
    MAX_ROWS = 5_000  # keep log compact

    def __init__(self, db: Session) -> None:
        self._db = db

    def record(self, entry: NetworkLog) -> NetworkLog:
        self._db.add(entry)
        self._db.commit()
        self._prune()
        return entry

    def recent(self, limit: int = 200, tab_url: str | None = None) -> list[NetworkLog]:
        stmt = select(NetworkLog).order_by(NetworkLog.timestamp.desc()).limit(limit)
        if tab_url:
            stmt = stmt.where(NetworkLog.tab_url == tab_url)
        return list(self._db.execute(stmt).scalars())

    def count_by_status(self) -> dict[str, int]:
        rows = self._db.execute(
            select(NetworkLog.status, func.count()).group_by(NetworkLog.status)
        ).all()
        return {r[0].value: r[1] for r in rows}

    def cname_incidents(self, limit: int = 50) -> list[NetworkLog]:
        stmt = (
            select(NetworkLog)
            .where(NetworkLog.is_cname_cloaked == True)  # noqa: E712
            .order_by(NetworkLog.timestamp.desc())
            .limit(limit)
        )
        return list(self._db.execute(stmt).scalars())

    def clear(self) -> int:
        result = self._db.execute(delete(NetworkLog))
        self._db.commit()
        return result.rowcount

    def _prune(self) -> None:
        """Keep only the newest MAX_ROWS entries to bound table size."""
        count = self._db.execute(select(func.count(NetworkLog.id))).scalar_one()
        if count > self.MAX_ROWS:
            cutoff_id = self._db.execute(
                select(NetworkLog.id)
                .order_by(NetworkLog.id.desc())
                .offset(self.MAX_ROWS)
                .limit(1)
            ).scalar_one_or_none()
            if cutoff_id:
                self._db.execute(
                    delete(NetworkLog).where(NetworkLog.id <= cutoff_id)
                )
                self._db.commit()
