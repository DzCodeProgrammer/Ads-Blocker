"""
Update service — wraps APScheduler to periodically refresh filter lists.
Started once at application startup via lifespan context.
"""
from __future__ import annotations
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from backend.config import get_settings
from backend.filters.updater import FilterUpdater

logger = logging.getLogger(__name__)

_scheduler = AsyncIOScheduler()
_updater = FilterUpdater()


async def _run_update() -> None:
    from backend.database.db import SessionLocal
    from backend.services.blocking_service import reload_engine
    settings = get_settings()
    db = SessionLocal()
    try:
        counts = _updater.update_all(db, settings)
        total = sum(counts.values())
        logger.info(f"Filter update complete — {total} rules loaded")
        reload_engine(db)
    except Exception as exc:
        logger.exception(f"Filter update failed: {exc}")
    finally:
        db.close()


def start_scheduler() -> None:
    settings = get_settings()
    _scheduler.add_job(
        _run_update,
        trigger=IntervalTrigger(hours=settings.FILTER_UPDATE_INTERVAL),
        id="filter_update",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info(
        f"Filter scheduler started — interval={settings.FILTER_UPDATE_INTERVAL}h"
    )


def stop_scheduler() -> None:
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("Filter scheduler stopped")


async def trigger_update_now() -> dict[str, int]:
    """Manually trigger an immediate update (called from admin API route)."""
    from backend.database.db import SessionLocal
    from backend.services.blocking_service import reload_engine
    settings = get_settings()
    db = SessionLocal()
    try:
        counts = _updater.update_all(db, settings)
        reload_engine(db)
        return counts
    finally:
        db.close()
