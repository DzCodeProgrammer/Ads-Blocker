"""
/api/export — import / export custom filter rules in EasyList format.

GET  /api/export/rules     — export custom rules as .txt
POST /api/export/import    — import rules from EasyList-format text body
"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.repositories.filter_repo import FilterRepository
from backend.filters.easylist_parser import EasyListParser
from backend.models.filter_rule import FilterRule, RuleType
from backend.services.blocking_service import reload_engine

router = APIRouter(prefix="/api/export", tags=["export"])


class ImportRequest(BaseModel):
    text: str
    overwrite: bool = False


@router.get("/rules", response_class=PlainTextResponse)
async def export_rules(db: Session = Depends(get_db)):
    repo = FilterRepository(db)
    rules = [
        r for r in repo.get_all_active()
        if r.source == "custom"
    ]
    lines = [
        "! AdBlocker Pro — Custom Filter Rules",
        "! Exported rules (EasyList format)",
        "!",
    ]
    for rule in rules:
        if rule.rule_type == RuleType.WHITELIST:
            lines.append(f"@@||{rule.pattern}^")
        else:
            prefix = "/" if rule.is_regex else "||"
            suffix = "/" if rule.is_regex else "^"
            lines.append(f"{prefix}{rule.pattern}{suffix}")
    return "\n".join(lines)


@router.post("/import")
async def import_rules(body: ImportRequest, db: Session = Depends(get_db)):
    if len(body.text) > 5_000_000:
        raise HTTPException(status_code=413, detail="Import too large (max 5 MB)")

    parser = EasyListParser()
    parsed = parser.parse(body.text)
    repo = FilterRepository(db)

    if body.overwrite:
        repo.delete_by_source("custom")

    imported = 0
    for p in parsed:
        if p.is_cosmetic or not p.pattern:
            continue
        rt = RuleType.WHITELIST if p.is_exception else RuleType.BLACKLIST
        repo.add(FilterRule(
            pattern=p.pattern[:2048],
            rule_type=rt,
            source="custom",
            is_regex=p.is_regex,
            comment="Imported",
        ))
        imported += 1

    reload_engine(db)
    return {"status": "imported", "count": imported}
