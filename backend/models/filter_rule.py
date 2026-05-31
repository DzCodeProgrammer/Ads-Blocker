"""ORM model for filter rules (blacklist / whitelist / easylist)."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base


class RuleType(str, enum.Enum):
    BLACKLIST = "blacklist"
    WHITELIST = "whitelist"
    EASYLIST = "easylist"
    EASYPRIVACY = "easyprivacy"
    UBLOCK = "ublock"
    ML_DETECTED = "ml_detected"


class FilterRule(Base):
    __tablename__ = "filter_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pattern: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    rule_type: Mapped[RuleType] = mapped_column(Enum(RuleType), nullable=False)
    source: Mapped[str] = mapped_column(String(256), nullable=False, default="custom")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_regex: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    hit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<FilterRule id={self.id} type={self.rule_type} pattern={self.pattern!r}>"
