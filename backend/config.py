"""Central application configuration via pydantic-settings."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # App
    APP_ENV: str = "development"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8765
    APP_SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Database
    DATABASE_URL: str = "sqlite:///./adblocker.db"

    # Filter sources
    EASYLIST_URL: str = "https://easylist.to/easylist/easylist.txt"
    EASYPRIVACY_URL: str = "https://easylist.to/easylist/easyprivacy.txt"
    UBLOCK_URL: str = "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt"

    # Scheduler
    FILTER_UPDATE_INTERVAL: int = 24  # hours

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 120

    # ML
    ML_MODEL_PATH: str = "./ml_engine/data/model.joblib"
    ML_TRAINING_DATA: str = "./ml_engine/data/training_data.csv"
    ML_CONFIDENCE_THRESHOLD: float = 0.75

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/adblocker.log"

    # CORS
    CORS_ORIGINS: str = "chrome-extension://,moz-extension://,ms-browser-extension://"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
