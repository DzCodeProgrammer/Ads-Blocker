"""
/api/stats — dashboard statistics endpoints.

GET /api/stats/summary        — total blocked, today, trackers, rules count
GET /api/stats/top-domains    — top N most-blocked domains
GET /api/stats/daily          — per-day counts for last N days
GET /api/stats/breakdown      — rule-type breakdown
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.services.stats_service import StatsService

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/summary")
async def summary(db: Session = Depends(get_db)):
    return StatsService(db).get_summary()


@router.get("/top-domains")
async def top_domains(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return StatsService(db).get_top_domains(limit=limit)


@router.get("/daily")
async def daily(
    days: int = Query(default=7, ge=1, le=90),
    db: Session = Depends(get_db),
):
    return StatsService(db).get_daily_stats(days=days)


@router.get("/breakdown")
async def breakdown(db: Session = Depends(get_db)):
    return StatsService(db).get_rules_breakdown()
