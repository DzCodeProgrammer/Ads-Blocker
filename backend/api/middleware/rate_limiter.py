"""Rate limiting middleware using slowapi (Starlette-compatible limiter)."""
from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.config import get_settings

settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)
