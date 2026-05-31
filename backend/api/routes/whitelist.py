"""
/api/whitelist — convenience endpoints to manage whitelist rules.

GET    /api/whitelist           — list whitelisted domains
POST   /api/whitelist           — add a domain to whitelist
DELETE /api/whitelist/{rule_id} — remove from whitelist
"""
import re
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.repositories.filter_repo import FilterRepository
from backend.services.blocking_service import BlockingService

router = APIRouter(prefix="/api/whitelist", tags=["whitelist"])

_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


class WhitelistAdd(BaseModel):
    domain: str

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        v = v.strip().lower().lstrip("www.")
        if not _DOMAIN_RE.match(v):
            raise ValueError("Invalid domain format")
        return v


@router.get("")
async def list_whitelist(db: Session = Depends(get_db)):
    repo = FilterRepository(db)
    rules = repo.get_whitelist()
    return [{"id": r.id, "domain": r.pattern, "created_at": r.created_at.isoformat()} for r in rules]


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_whitelist(body: WhitelistAdd, db: Session = Depends(get_db)):
    svc = BlockingService(db)
    svc.add_custom_rule(body.domain, "whitelist", comment="User whitelist")
    return {"status": "whitelisted", "domain": body.domain}


@router.delete("/{rule_id}")
async def remove_whitelist(rule_id: int, db: Session = Depends(get_db)):
    svc = BlockingService(db)
    ok = svc.remove_rule(rule_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"status": "removed", "id": rule_id}
