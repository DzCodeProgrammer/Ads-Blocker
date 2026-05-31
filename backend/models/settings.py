"""ORM model for persisting user-level settings (on/off, whitelist mode, etc.)."""
from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    block_ads: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    block_trackers: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    block_malware: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    enable_ml: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    dark_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    show_counter: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
