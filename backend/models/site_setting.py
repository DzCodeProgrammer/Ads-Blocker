"""ORM: per-domain user preferences (disable, aggressive, normal mode)."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base


class SiteMode(str, enum.Enum):
    NORMAL = "normal"           # standard blocking
    AGGRESSIVE = "aggressive"   # block all 3rd-party scripts/frames
    DISABLED = "disabled"       # no blocking (user whitelisted the site)


class SiteSetting(Base):
    __tablename__ = "site_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    domain: Mapped[str] = mapped_column(String(512), nullable=False, unique=True, index=True)
    mode: Mapped[SiteMode] = mapped_column(SAEnum(SiteMode), default=SiteMode.NORMAL)
    block_scripts: Mapped[bool] = mapped_column(Boolean, default=True)
    block_images: Mapped[bool] = mapped_column(Boolean, default=False)
    block_xhr: Mapped[bool] = mapped_column(Boolean, default=True)
    block_frames: Mapped[bool] = mapped_column(Boolean, default=True)
    block_media: Mapped[bool] = mapped_column(Boolean, default=False)
    block_websocket: Mapped[bool] = mapped_column(Boolean, default=True)
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
