"""ORM: NetworkLog — per-request log powering the real-time network logger."""
from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.db import Base


class RequestStatus(str, enum.Enum):
    BLOCKED = "blocked"
    ALLOWED = "allowed"
    WHITELISTED = "whitelisted"
    CLEANED = "cleaned"      # URL tracking params stripped


class ContentType(str, enum.Enum):
    SCRIPT = "script"
    IMAGE = "image"
    STYLESHEET = "stylesheet"
    XHR = "xmlhttprequest"
    FRAME = "sub_frame"
    MEDIA = "media"
    FONT = "font"
    WEBSOCKET = "websocket"
    PING = "ping"
    OTHER = "other"


class NetworkLog(Base):
    __tablename__ = "network_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(4096), nullable=False)
    domain: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    tab_url: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    status: Mapped[RequestStatus] = mapped_column(SAEnum(RequestStatus), nullable=False)
    content_type: Mapped[ContentType] = mapped_column(
        SAEnum(ContentType), default=ContentType.OTHER, nullable=False
    )
    rule_matched: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    is_tracker: Mapped[bool] = mapped_column(Boolean, default=False)
    is_third_party: Mapped[bool] = mapped_column(Boolean, default=False)
    is_cname_cloaked: Mapped[bool] = mapped_column(Boolean, default=False)
    cname_real_domain: Mapped[str | None] = mapped_column(String(512), nullable=True)
    cleaned_url: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
