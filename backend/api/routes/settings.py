"""
/api/settings — user preferences (enable/disable, dark mode, ML toggle, etc.)

GET  /api/settings      — fetch current settings
PUT  /api/settings      — update settings
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.models.settings import UserSettings

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingsUpdate(BaseModel):
    is_enabled: bool | None = None
    block_ads: bool | None = None
    block_trackers: bool | None = None
    block_malware: bool | None = None
    enable_ml: bool | None = None
    dark_mode: bool | None = None
    show_counter: bool | None = None


def _get_or_create(db: Session) -> UserSettings:
    obj = db.get(UserSettings, 1)
    if not obj:
        obj = UserSettings(id=1)
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj


@router.get("")
async def get_settings_route(db: Session = Depends(get_db)):
    s = _get_or_create(db)
    return {
        "is_enabled": s.is_enabled,
        "block_ads": s.block_ads,
        "block_trackers": s.block_trackers,
        "block_malware": s.block_malware,
        "enable_ml": s.enable_ml,
        "dark_mode": s.dark_mode,
        "show_counter": s.show_counter,
    }


@router.put("")
async def update_settings(body: SettingsUpdate, db: Session = Depends(get_db)):
    s = _get_or_create(db)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(s, field, value)
    db.commit()
    db.refresh(s)
    return {"status": "updated"}
