"""
Predictor — thin production-facing wrapper loaded lazily by FilterEngine.

Usage:
    predictor = AdPredictor()
    score = predictor.predict_proba("https://ads.example.com/pixel.gif")
    # returns float in [0, 1]; ≥ threshold → block
"""
from __future__ import annotations
import logging
from pathlib import Path
from ml_engine.classifier import AdClassifier
from backend.config import get_settings

logger = logging.getLogger(__name__)


class AdPredictor:
    def __init__(self) -> None:
        settings = get_settings()
        model_path = settings.ML_MODEL_PATH
        self._clf = AdClassifier()
        if Path(model_path).exists():
            self._clf.load(model_path)
        else:
            logger.warning(
                f"ML model not found at {model_path}. "
                "Run: python -m ml_engine.trainer"
            )

    @property
    def is_ready(self) -> bool:
        return self._clf.is_ready

    def predict_proba(self, url: str) -> float:
        """Return ad probability in [0, 1]. Returns 0.0 if model not ready."""
        if not self.is_ready:
            return 0.0
        try:
            return self._clf.predict_proba(url)
        except Exception as exc:
            logger.debug(f"Prediction error for {url!r}: {exc}")
            return 0.0
