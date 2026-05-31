"""
Ad-detection classifier using scikit-learn Random Forest.

Trained to distinguish ad/tracker URLs (label=1) from benign URLs (label=0).
The model file is persisted with joblib for fast cold-start loading.
"""
from __future__ import annotations
import logging
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import joblib

from ml_engine.feature_extractor import FeatureExtractor

logger = logging.getLogger(__name__)


class AdClassifier:
    """Thin wrapper around an sklearn Pipeline (scaler + ensemble)."""

    def __init__(self, model_path: str | None = None) -> None:
        self._extractor = FeatureExtractor()
        self._pipeline: Pipeline | None = None
        if model_path and Path(model_path).exists():
            self.load(model_path)

    # ------------------------------------------------------------------ build

    def _build_pipeline(self) -> Pipeline:
        return Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_leaf=2,
                class_weight="balanced",
                n_jobs=-1,
                random_state=42,
            )),
        ])

    # ----------------------------------------------------------------- train

    def train(self, urls: list[str], labels: list[int]) -> dict:
        X = np.array(self._extractor.extract_batch(urls), dtype=float)
        y = np.array(labels, dtype=int)

        self._pipeline = self._build_pipeline()
        scores = cross_val_score(self._pipeline, X, y, cv=5, scoring="f1", n_jobs=-1)
        self._pipeline.fit(X, y)

        logger.info(f"Model trained — CV F1: {scores.mean():.4f} ± {scores.std():.4f}")
        return {
            "cv_f1_mean": float(scores.mean()),
            "cv_f1_std": float(scores.std()),
            "n_samples": len(urls),
        }

    # --------------------------------------------------------------- predict

    def predict(self, url: str) -> int:
        if not self._pipeline:
            raise RuntimeError("Model not trained or loaded")
        features = np.array([self._extractor.extract(url)], dtype=float)
        return int(self._pipeline.predict(features)[0])

    def predict_proba(self, url: str) -> float:
        """Return probability that URL is an ad/tracker (class 1)."""
        if not self._pipeline:
            raise RuntimeError("Model not trained or loaded")
        features = np.array([self._extractor.extract(url)], dtype=float)
        return float(self._pipeline.predict_proba(features)[0][1])

    def predict_batch(self, urls: list[str]) -> list[float]:
        if not self._pipeline:
            raise RuntimeError("Model not trained or loaded")
        X = np.array(self._extractor.extract_batch(urls), dtype=float)
        return self._pipeline.predict_proba(X)[:, 1].tolist()

    # ------------------------------------------------------------------- I/O

    def save(self, path: str) -> None:
        if not self._pipeline:
            raise RuntimeError("Nothing to save — train or load first")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self._pipeline, path)
        logger.info(f"Model saved → {path}")

    def load(self, path: str) -> None:
        self._pipeline = joblib.load(path)
        logger.info(f"Model loaded ← {path}")

    @property
    def is_ready(self) -> bool:
        return self._pipeline is not None
