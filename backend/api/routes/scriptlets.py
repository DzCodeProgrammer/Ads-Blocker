"""
/api/scriptlets — serve scriptlet JS code to content script injector.

GET  /api/scriptlets               — list available scriptlets
POST /api/scriptlets/bundle        — get a bundle of scriptlets for a domain
GET  /api/scriptlets/{name}        — get single scriptlet code
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.filters.scriptlet_engine import ScriptletEngine

router = APIRouter(prefix="/api/scriptlets", tags=["scriptlets"])

_engine = ScriptletEngine()

# Default scriptlets always injected on all pages
DEFAULT_SCRIPTLETS = [
    "anti-adblock-killer",
    "no-webrtc",
    "no-notification-if",
    "noeval",
]

# Per-domain scriptlet rules (can be expanded dynamically)
DOMAIN_SCRIPTLETS: dict[str, list[str]] = {
    "youtube.com": ["youtube-ad-skip"],
    "twitch.tv": ["no-setTimeout-if"],
    "forbes.com": ["no-setTimeout-if", "remove-class"],
    "wired.com": ["no-setTimeout-if"],
    "wsj.com": ["no-setTimeout-if"],
    "businessinsider.com": ["no-setTimeout-if"],
}


class BundleRequest(BaseModel):
    domain: str
    include_defaults: bool = True


@router.get("")
async def list_scriptlets():
    return {
        "scriptlets": _engine.list_all(),
        "defaults": DEFAULT_SCRIPTLETS,
    }


@router.get("/{name}")
async def get_scriptlet(name: str):
    code = _engine.get(name)
    if not code:
        raise HTTPException(status_code=404, detail=f"Scriptlet '{name}' not found")
    return {"name": name, "code": code}


@router.post("/bundle")
async def get_bundle(body: BundleRequest):
    names: list[str] = []
    if body.include_defaults:
        names.extend(DEFAULT_SCRIPTLETS)

    # Add domain-specific scriptlets
    domain = body.domain.lower().replace("www.", "")
    for d, scripts in DOMAIN_SCRIPTLETS.items():
        if domain == d or domain.endswith("." + d):
            names.extend(s for s in scripts if s not in names)

    code = _engine.get_bundle(names)
    return {
        "domain": body.domain,
        "scriptlets": names,
        "code": code,
    }
