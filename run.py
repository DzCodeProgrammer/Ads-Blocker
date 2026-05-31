"""Entry point — starts FastAPI backend and scheduler."""
import uvicorn
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.api.main import create_app
from backend.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()
    logger.info(f"Starting AdBlocker backend on {settings.APP_HOST}:{settings.APP_PORT}")
    app = create_app()
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.APP_ENV == "development",
    )


if __name__ == "__main__":
    main()
