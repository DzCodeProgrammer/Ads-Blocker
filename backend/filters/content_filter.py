"""
Content-type aware filter — like uBlock Origin's dynamic filtering.

Allows blocking per request type (script, image, XHR, frame, media, etc.)
with per-site overrides. Aggressive mode blocks all 3rd-party scripts/frames.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContentPolicy:
    """Global content-type policy (can be overridden per site)."""
    # Default: block scripts/XHR/frames from 3rd parties only
    block_scripts_3p: bool = True
    block_scripts_1p: bool = False
    block_xhr_3p: bool = True
    block_xhr_1p: bool = False
    block_frames_3p: bool = True
    block_frames_1p: bool = False
    block_images: bool = False
    block_media: bool = False
    block_fonts_3p: bool = False
    block_stylesheets: bool = False
    block_websocket: bool = True
    block_ping: bool = True


# Aggressive mode preset (like Brave's aggressive shield)
AGGRESSIVE_POLICY = ContentPolicy(
    block_scripts_3p=True,
    block_scripts_1p=False,
    block_xhr_3p=True,
    block_xhr_1p=False,
    block_frames_3p=True,
    block_frames_1p=False,
    block_images=False,
    block_media=False,
    block_fonts_3p=True,
    block_stylesheets=False,
    block_websocket=True,
    block_ping=True,
)

NORMAL_POLICY = ContentPolicy()


class ContentTypeFilter:
    """Decide whether content type alone warrants blocking (before URL pattern check)."""

    def __init__(self, policy: ContentPolicy | None = None) -> None:
        self._global = policy or NORMAL_POLICY
        self._site_policies: dict[str, ContentPolicy] = {}

    def set_site_policy(self, domain: str, policy: ContentPolicy) -> None:
        self._site_policies[domain] = policy

    def set_global_policy(self, policy: ContentPolicy) -> None:
        self._global = policy

    def should_block_by_type(
        self,
        content_type: str,
        is_third_party: bool,
        site_domain: Optional[str] = None,
    ) -> bool:
        policy = self._site_policies.get(site_domain or "", self._global)

        match content_type:
            case "script":
                return policy.block_scripts_3p if is_third_party else policy.block_scripts_1p
            case "xmlhttprequest":
                return policy.block_xhr_3p if is_third_party else policy.block_xhr_1p
            case "sub_frame":
                return policy.block_frames_3p if is_third_party else policy.block_frames_1p
            case "image":
                return policy.block_images
            case "media":
                return policy.block_media
            case "font":
                return policy.block_fonts_3p and is_third_party
            case "stylesheet":
                return policy.block_stylesheets
            case "websocket":
                return policy.block_websocket
            case "ping":
                return policy.block_ping
            case _:
                return False

    def load_from_site_setting(self, domain: str, setting) -> None:
        """Sync ContentPolicy from a SiteSetting ORM object."""
        from backend.models.site_setting import SiteMode

        if setting.mode == SiteMode.AGGRESSIVE:
            self._site_policies[domain] = AGGRESSIVE_POLICY
        elif setting.mode == SiteMode.DISABLED:
            self._site_policies[domain] = ContentPolicy(
                block_scripts_3p=False, block_xhr_3p=False,
                block_frames_3p=False, block_websocket=False, block_ping=False,
            )
        else:
            self._site_policies[domain] = ContentPolicy(
                block_scripts_3p=setting.block_scripts,
                block_xhr_3p=setting.block_xhr,
                block_frames_3p=setting.block_frames,
                block_images=setting.block_images,
                block_media=setting.block_media,
                block_websocket=setting.block_websocket,
                block_ping=True,
            )
