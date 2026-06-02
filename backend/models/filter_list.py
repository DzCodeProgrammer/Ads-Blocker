"""ORM: filter list registry — manage remote filter list subscriptions."""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base


class FilterList(Base):
    __tablename__ = "filter_lists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(64), default="general")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False)
    rule_count: Mapped[int] = mapped_column(Integer, default=0)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
