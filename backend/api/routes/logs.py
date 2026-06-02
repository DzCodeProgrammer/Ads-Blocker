"""
/api/logs — network request log (real-time view of blocked/allowed requests).

GET  /api/logs           — recent request log (last N entries)
GET  /api/logs/cname     — CNAME uncloaking incidents
POST /api/logs/record    — record a log entry (called from background.js)
DELETE /api/logs         — clear the log
"""
from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.repositories.log_repo import LogRepository
from backend.models.network_log import NetworkLog, RequestStatus, ContentType

router = APIRouter(prefix="/api/logs", tags=["logs"])


class LogEntry(BaseModel):
    url: str
    domain: str
    tab_url: str | None = None
    status: str = "blocked"
    content_type: str = "other"
    rule_matched: str | None = None
    is_tracker: bool = False
    is_third_party: bool = False
    is_cname_cloaked: bool = False
    cname_real_domain: str | None = None
    cleaned_url: str | None = None

    @field_validator("url", "domain")
    @classmethod
    def limit_length(cls, v: str) -> str:
        return v[:4096] if v else v


@router.post("/record", status_code=201)
async def record_log(entry: LogEntry, db: Session = Depends(get_db)):
    try:
        status = RequestStatus(entry.status)
    except ValueError:
        status = RequestStatus.BLOCKED
    try:
        ctype = ContentType(entry.content_type)
    except ValueError:
        ctype = ContentType.OTHER

    log = NetworkLog(
        url=entry.url[:4096],
        domain=entry.domain[:512],
        tab_url=(entry.tab_url or "")[:4096] or None,
        status=status,
        content_type=ctype,
        rule_matched=entry.rule_matched,
        is_tracker=entry.is_tracker,
        is_third_party=entry.is_third_party,
        is_cname_cloaked=entry.is_cname_cloaked,
        cname_real_domain=entry.cname_real_domain,
        cleaned_url=entry.cleaned_url,
    )
    repo = LogRepository(db)
    saved = repo.record(log)
    return {"id": saved.id}


@router.get("")
async def get_logs(
    limit: int = Query(default=200, ge=1, le=1000),
    tab_url: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    repo = LogRepository(db)
    entries = repo.recent(limit=limit, tab_url=tab_url)
    return [
        {
            "id": e.id,
            "url": e.url,
            "domain": e.domain,
            "status": e.status.value,
            "content_type": e.content_type.value,
            "rule_matched": e.rule_matched,
            "is_tracker": e.is_tracker,
            "is_third_party": e.is_third_party,
            "is_cname_cloaked": e.is_cname_cloaked,
            "cname_real_domain": e.cname_real_domain,
            "timestamp": e.timestamp.isoformat(),
        }
        for e in entries
    ]


@router.get("/cname")
async def cname_incidents(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    repo = LogRepository(db)
    entries = repo.cname_incidents(limit=limit)
    return [
        {
            "id": e.id,
            "domain": e.domain,
            "cname_real_domain": e.cname_real_domain,
            "url": e.url,
            "timestamp": e.timestamp.isoformat(),
        }
        for e in entries
    ]


@router.delete("")
async def clear_logs(db: Session = Depends(get_db)):
    count = LogRepository(db).clear()
    return {"status": "cleared", "deleted": count}
