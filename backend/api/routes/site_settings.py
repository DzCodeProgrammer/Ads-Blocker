"""
/api/site-settings — per-domain blocking mode management.

GET    /api/site-settings              — list all site settings
GET    /api/site-settings/{domain}     — get setting for domain
PUT    /api/site-settings/{domain}     — set mode (normal/aggressive/disabled)
DELETE /api/site-settings/{domain}     — reset to global default
"""
from __future__ import annotations
import re
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.repositories.site_repo import SiteRepository
from backend.models.site_setting import SiteMode

router = APIRouter(prefix="/api/site-settings", tags=["site-settings"])

_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


class SiteSettingUpdate(BaseModel):
    mode: str = "normal"
    block_scripts: bool = True
    block_images: bool = False
    block_xhr: bool = True
    block_frames: bool = True
    block_media: bool = False
    block_websocket: bool = True

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        allowed = {m.value for m in SiteMode}
        if v not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        return v


def _validate_domain(domain: str) -> str:
    domain = domain.strip().lower()
    if not _DOMAIN_RE.match(domain):
        raise HTTPException(status_code=422, detail="Invalid domain format")
    return domain


@router.get("")
async def list_site_settings(db: Session = Depends(get_db)):
    repo = SiteRepository(db)
    settings = repo.list_all()
    return [
        {
            "domain": s.domain,
            "mode": s.mode.value,
            "block_scripts": s.block_scripts,
            "block_images": s.block_images,
            "block_xhr": s.block_xhr,
            "block_frames": s.block_frames,
            "block_media": s.block_media,
            "block_websocket": s.block_websocket,
            "updated_at": s.updated_at.isoformat(),
        }
        for s in settings
    ]


@router.get("/{domain}")
async def get_site_setting(domain: str, db: Session = Depends(get_db)):
    domain = _validate_domain(domain)
    repo = SiteRepository(db)
    s = repo.get(domain)
    if not s:
        return {"domain": domain, "mode": "normal"}
    return {
        "domain": s.domain,
        "mode": s.mode.value,
        "block_scripts": s.block_scripts,
        "block_images": s.block_images,
        "block_xhr": s.block_xhr,
        "block_frames": s.block_frames,
        "block_media": s.block_media,
        "block_websocket": s.block_websocket,
    }


@router.put("/{domain}")
async def update_site_setting(
    domain: str,
    body: SiteSettingUpdate,
    db: Session = Depends(get_db),
):
    domain = _validate_domain(domain)
    repo = SiteRepository(db)
    repo.update(
        domain,
        mode=SiteMode(body.mode),
        block_scripts=body.block_scripts,
        block_images=body.block_images,
        block_xhr=body.block_xhr,
        block_frames=body.block_frames,
        block_media=body.block_media,
        block_websocket=body.block_websocket,
    )
    return {"status": "updated", "domain": domain, "mode": body.mode}


@router.delete("/{domain}")
async def reset_site_setting(domain: str, db: Session = Depends(get_db)):
    domain = _validate_domain(domain)
    ok = SiteRepository(db).delete(domain)
    if not ok:
        raise HTTPException(status_code=404, detail="No custom setting for this domain")
    return {"status": "reset", "domain": domain}
