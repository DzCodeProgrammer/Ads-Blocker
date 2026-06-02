"""
FastAPI application factory.

Registers all routers, middleware, lifespan (startup/shutdown), and error handlers.
"""
from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from backend.config import get_settings
from backend.database.db import init_db
from backend.api.middleware.security import SecurityHeadersMiddleware
from backend.api.middleware.rate_limiter import limiter
from backend.api.routes import filters, stats, settings, whitelist
from backend.api.routes import logs, site_settings, lists, export, scriptlets
from backend.services.update_service import start_scheduler, stop_scheduler
from backend.services.blocking_service import reload_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    logger.info("AdBlocker backend starting up")
    init_db()
    from backend.database.db import SessionLocal
    db = SessionLocal()
    try:
        count = reload_engine(db)
        logger.info(f"Engine loaded {count} rules from DB")
    finally:
        db.close()
    start_scheduler()
    yield
    # ── Shutdown ─────────────────────────────────────────────
    stop_scheduler()
    logger.info("AdBlocker backend shut down")


def create_app() -> FastAPI:
    cfg = get_settings()

    app = FastAPI(
        title="AdBlocker API",
        description="Professional Ad Blocker backend — Python/FastAPI",
        version="1.0.0",
        docs_url="/docs" if cfg.APP_ENV == "development" else None,
        redoc_url="/redoc" if cfg.APP_ENV == "development" else None,
        lifespan=lifespan,
    )

    # ── Rate limiter ──────────────────────────────────────────
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Slow down."},
        )

    # ── Security headers ──────────────────────────────────────
    app.add_middleware(SecurityHeadersMiddleware)

    # ── CORS — only allow extension origins ───────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.cors_origins_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # ── Routes ───────────────────────────────────────────────
    app.include_router(filters.router)
    app.include_router(stats.router)
    app.include_router(settings.router)
    app.include_router(whitelist.router)
    app.include_router(logs.router)
    app.include_router(site_settings.router)
    app.include_router(lists.router)
    app.include_router(export.router)
    app.include_router(scriptlets.router)

    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok", "version": "1.0.0"}

    return app
