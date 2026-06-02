"""
/api/lists — manage filter list subscriptions (enable/disable/add custom).

GET    /api/lists          — list all filter lists
PUT    /api/lists/{id}     — enable or disable a list
POST   /api/lists          — subscribe to a new filter list URL
DELETE /api/lists/{id}     — unsubscribe from a list
POST   /api/lists/{id}/update — force update a specific list
"""
from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl, field_validator
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.database.db import get_db
from backend.models.filter_list import FilterList
from backend.filters.updater import FilterUpdater
from backend.services.blocking_service import reload_engine

router = APIRouter(prefix="/api/lists", tags=["lists"])

# Built-in lists seeded at startup
BUILTIN_LISTS = [
    {
        "name": "EasyList",
        "url": "https://easylist.to/easylist/easylist.txt",
        "category": "ads",
        "description": "Primary filter list that removes most adverts from international webpages.",
    },
    {
        "name": "EasyPrivacy",
        "url": "https://easylist.to/easylist/easyprivacy.txt",
        "category": "privacy",
        "description": "Completely removes all forms of tracking from the internet.",
    },
    {
        "name": "uBlock Filters",
        "url": "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",
        "category": "ads",
        "description": "uBlock Origin's own filter list.",
    },
    {
        "name": "uBlock Privacy",
        "url": "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt",
        "category": "privacy",
        "description": "uBlock Origin privacy filters.",
    },
    {
        "name": "Peter Lowe's Ad and Tracking Server List",
        "url": "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext",
        "category": "ads",
        "description": "List of ad/tracking servers.",
    },
    {
        "name": "Fanboy's Annoyance List",
        "url": "https://easylist.to/easylist/fanboy-annoyance.txt",
        "category": "annoyances",
        "description": "Blocks Social Media content, in-page pop-ups and other annoyances.",
    },
    {
        "name": "Cookie AutoDelete Supplementary",
        "url": "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/annoyances-cookies.txt",
        "category": "cookies",
        "description": "Blocks cookie notices and GDPR consent banners.",
    },
    {
        "name": "NoCoin — Cryptominer Block",
        "url": "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/resource-abuse.txt",
        "category": "malware",
        "description": "Blocks cryptominer scripts.",
    },
]


def seed_builtin_lists(db: Session) -> None:
    """Seed built-in lists if table is empty."""
    count = db.execute(select(FilterList)).scalars().first()
    if count is not None:
        return
    for item in BUILTIN_LISTS:
        db.add(FilterList(**item, is_builtin=True))
    db.commit()


class AddListRequest(BaseModel):
    name: str
    url: str
    category: str = "custom"
    description: str = ""

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 256:
            raise ValueError("Name must be 1-256 chars")
        return v

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("https://", "http://")):
            raise ValueError("URL must start with http(s)://")
        return v[:2048]


class UpdateListRequest(BaseModel):
    is_enabled: bool | None = None


@router.get("")
async def list_filter_lists(db: Session = Depends(get_db)):
    seed_builtin_lists(db)
    lists = list(db.execute(select(FilterList)).scalars())
    return [
        {
            "id": fl.id,
            "name": fl.name,
            "url": fl.url,
            "category": fl.category,
            "description": fl.description,
            "is_enabled": fl.is_enabled,
            "is_builtin": fl.is_builtin,
            "rule_count": fl.rule_count,
            "last_updated": fl.last_updated.isoformat() if fl.last_updated else None,
        }
        for fl in lists
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_list(body: AddListRequest, db: Session = Depends(get_db)):
    existing = db.execute(select(FilterList).where(FilterList.url == body.url)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="List already subscribed")
    fl = FilterList(
        name=body.name,
        url=body.url,
        category=body.category,
        description=body.description,
        is_builtin=False,
    )
    db.add(fl)
    db.commit()
    db.refresh(fl)
    return {"status": "subscribed", "id": fl.id}


@router.put("/{list_id}")
async def toggle_list(list_id: int, body: UpdateListRequest, db: Session = Depends(get_db)):
    fl = db.get(FilterList, list_id)
    if not fl:
        raise HTTPException(status_code=404, detail="List not found")
    if body.is_enabled is not None:
        fl.is_enabled = body.is_enabled
        db.commit()
    return {"status": "updated", "id": list_id, "is_enabled": fl.is_enabled}


@router.delete("/{list_id}")
async def remove_list(list_id: int, db: Session = Depends(get_db)):
    fl = db.get(FilterList, list_id)
    if not fl:
        raise HTTPException(status_code=404, detail="List not found")
    if fl.is_builtin:
        raise HTTPException(status_code=403, detail="Cannot delete built-in lists, only disable them")
    db.delete(fl)
    db.commit()
    return {"status": "deleted", "id": list_id}


@router.post("/{list_id}/update")
async def update_single_list(list_id: int, db: Session = Depends(get_db)):
    fl = db.get(FilterList, list_id)
    if not fl:
        raise HTTPException(status_code=404, detail="List not found")
    updater = FilterUpdater()
    from backend.models.filter_rule import RuleType
    type_map = {
        "ads": RuleType.EASYLIST,
        "privacy": RuleType.EASYPRIVACY,
        "custom": RuleType.BLACKLIST,
    }
    rt = type_map.get(fl.category, RuleType.EASYLIST)
    raw = updater.fetch_raw(fl.url)
    if not raw:
        raise HTTPException(status_code=502, detail="Failed to fetch filter list")
    rules = updater.parse_to_rules(raw, rt, fl.url)
    from backend.database.repositories.filter_repo import FilterRepository
    repo = FilterRepository(db)
    repo.delete_by_source(fl.url)
    count = repo.bulk_insert(rules)
    fl.rule_count = count
    fl.last_updated = datetime.utcnow()
    db.commit()
    reload_engine(db)
    return {"status": "updated", "rule_count": count}
