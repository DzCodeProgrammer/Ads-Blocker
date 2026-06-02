"""Repository for SiteSetting (per-domain blocking mode)."""
from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.site_setting import SiteSetting, SiteMode


class SiteRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, domain: str) -> SiteSetting | None:
        return self._db.execute(
            select(SiteSetting).where(SiteSetting.domain == domain)
        ).scalar_one_or_none()

    def get_or_create(self, domain: str) -> SiteSetting:
        obj = self.get(domain)
        if not obj:
            obj = SiteSetting(domain=domain)
            self._db.add(obj)
            self._db.commit()
            self._db.refresh(obj)
        return obj

    def set_mode(self, domain: str, mode: SiteMode) -> SiteSetting:
        obj = self.get_or_create(domain)
        obj.mode = mode
        self._db.commit()
        return obj

    def update(self, domain: str, **kwargs) -> SiteSetting:
        obj = self.get_or_create(domain)
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        self._db.commit()
        self._db.refresh(obj)
        return obj

    def list_all(self) -> list[SiteSetting]:
        return list(self._db.execute(select(SiteSetting)).scalars())

    def delete(self, domain: str) -> bool:
        obj = self.get(domain)
        if not obj:
            return False
        self._db.delete(obj)
        self._db.commit()
        return True

    def is_disabled(self, domain: str) -> bool:
        obj = self.get(domain)
        return obj is not None and obj.mode == SiteMode.DISABLED

    def is_aggressive(self, domain: str) -> bool:
        obj = self.get(domain)
        return obj is not None and obj.mode == SiteMode.AGGRESSIVE
