"""ORM model for recording every blocked network request."""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base


class BlockedRequest(Base):
    __tablename__ = "blocked_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(4096), nullable=False)
    domain: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    rule_matched: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    is_tracker: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ml_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    ml_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    tab_url: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    blocked_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<BlockedRequest id={self.id} domain={self.domain!r}>"
