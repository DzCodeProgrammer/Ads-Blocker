"""
/api/filters — CRUD for custom filter rules + URL check endpoint.

POST /api/filters/check        — check a URL (called by extension background.js)
GET  /api/filters              — list all active rules
POST /api/filters              — add a custom rule
DELETE /api/filters/{id}       — deactivate a rule
POST /api/filters/update       — trigger remote list update
"""
from __future__ import annotations
import re
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.services.blocking_service import BlockingService, reload_engine
from backend.services.update_service import trigger_update_now
from backend.database.repositories.filter_repo import FilterRepository

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/filters", tags=["filters"])

_SAFE_PATTERN = re.compile(r"^[a-zA-Z0-9\.\-_/\*\|\^\$\[\]\\@\+\?#%=:,~!&]+$")


class CheckRequest(BaseModel):
    url: str
    tab_url: str | None = None
    enable_ml: bool = True

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if len(v) > 4096:
            raise ValueError("URL too long")
        if not v.startswith(("http://", "https://", "ws://", "wss://")):
            raise ValueError("Invalid URL scheme")
        return v


class AddRuleRequest(BaseModel):
    pattern: str
    rule_type: str = "blacklist"
    comment: str = ""

    @field_validator("pattern")
    @classmethod
    def validate_pattern(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 2048:
            raise ValueError("Pattern must be 1-2048 chars")
        if not _SAFE_PATTERN.match(v):
            raise ValueError("Pattern contains invalid characters")
        return v

    @field_validator("rule_type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = {"blacklist", "whitelist"}
        if v not in allowed:
            raise ValueError(f"rule_type must be one of {allowed}")
        return v


@router.post("/check")
async def check_url(req: CheckRequest, db: Session = Depends(get_db)):
    svc = BlockingService(db)
    result = svc.check_and_record(req.url, req.tab_url, req.enable_ml)
    return {
        "url": result.url,
        "domain": result.domain,
        "blocked": result.blocked,
        "matched_rule": result.matched_rule,
        "is_tracker": result.is_tracker,
        "ml_blocked": result.ml_blocked,
        "ml_confidence": result.ml_confidence,
    }


@router.get("")
async def list_rules(
    rule_type: str | None = None,
    db: Session = Depends(get_db),
):
    from backend.models.filter_rule import RuleType
    repo = FilterRepository(db)
    rt = RuleType(rule_type) if rule_type else None
    rules = repo.get_all_active(rt)
    return [
        {
            "id": r.id,
            "pattern": r.pattern,
            "rule_type": r.rule_type,
            "source": r.source,
            "hit_count": r.hit_count,
            "created_at": r.created_at.isoformat(),
        }
        for r in rules
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_rule(req: AddRuleRequest, db: Session = Depends(get_db)):
    svc = BlockingService(db)
    svc.add_custom_rule(req.pattern, req.rule_type, req.comment)
    return {"status": "created", "pattern": req.pattern}


@router.delete("/{rule_id}")
async def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    svc = BlockingService(db)
    ok = svc.remove_rule(rule_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"status": "deactivated", "id": rule_id}


@router.post("/update")
async def update_filters():
    counts = await trigger_update_now()
    total = sum(counts.values())
    return {"status": "updated", "total_rules": total, "details": counts}
