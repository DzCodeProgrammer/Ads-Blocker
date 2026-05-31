"""
ML Trainer — loads training data CSV, trains AdClassifier, evaluates, and saves model.

CSV schema:  url (str) , label (0=benign, 1=ad/tracker)

Run:
    conda activate adblocker
    python -m ml_engine.trainer
"""
from __future__ import annotations
import logging
import sys
from pathlib import Path
import pandas as pd
from sklearn.metrics import classification_report
from ml_engine.classifier import AdClassifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_CSV = Path(__file__).parent / "data" / "training_data.csv"
DEFAULT_MODEL = Path(__file__).parent / "data" / "model.joblib"


def generate_sample_data(path: Path) -> None:
    """Generate a small synthetic dataset when no real data is available."""
    import random, string

    ad_domains = [
        "ads.doubleclick.net", "pagead2.googlesyndication.com", "adservice.google.com",
        "pixel.facebook.com", "tr.snapchat.com", "bat.bing.com", "static.ads-twitter.com",
        "analytics.twitter.com", "scorecardresearch.com", "quantserve.com",
        "hotjar.com", "mixpanel.com", "amplitude.com", "segment.io",
        "ads.pubmatic.com", "ads.rubiconproject.com", "sync.liveramp.com",
        "cm.adentifi.com", "ad.yieldmanager.com", "cdn.taboola.com",
    ]
    benign_domains = [
        "github.com", "stackoverflow.com", "docs.python.org", "wikipedia.org",
        "reddit.com", "youtube.com", "news.ycombinator.com", "developer.mozilla.org",
        "npmjs.com", "pypi.org", "medium.com", "dev.to", "twitter.com",
        "linkedin.com", "google.com", "bing.com", "duckduckgo.com",
    ]

    rows = []
    for domain in ad_domains:
        for _ in range(50):
            path_part = "/".join(
                "".join(random.choices(string.ascii_lowercase, k=8))
                for _ in range(random.randint(1, 3))
            )
            rows.append({
                "url": f"https://{domain}/{path_part}?id={''.join(random.choices(string.digits, k=12))}",
                "label": 1,
            })
    for domain in benign_domains:
        for _ in range(50):
            path_part = "/".join(
                "".join(random.choices(string.ascii_lowercase, k=6))
                for _ in range(random.randint(0, 2))
            )
            rows.append({"url": f"https://{domain}/{path_part}", "label": 0})

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Generated {len(df)} sample training rows → {path}")


def train(
    csv_path: Path = DEFAULT_CSV,
    model_path: Path = DEFAULT_MODEL,
) -> None:
    if not csv_path.exists():
        logger.warning(f"No training data at {csv_path} — generating synthetic data")
        generate_sample_data(csv_path)

    df = pd.read_csv(csv_path)
    if "url" not in df.columns or "label" not in df.columns:
        logger.error("CSV must have 'url' and 'label' columns")
        sys.exit(1)

    df = df.dropna(subset=["url", "label"])
    urls = df["url"].astype(str).tolist()
    labels = df["label"].astype(int).tolist()
    logger.info(f"Loaded {len(urls)} samples ({sum(labels)} positive)")

    clf = AdClassifier()
    metrics = clf.train(urls, labels)
    logger.info(f"Training metrics: {metrics}")

    # Full classification report
    import numpy as np
    from ml_engine.feature_extractor import FeatureExtractor
    X = np.array(FeatureExtractor().extract_batch(urls), dtype=float)
    y_pred = clf._pipeline.predict(X)
    logger.info("\n" + classification_report(labels, y_pred, target_names=["benign", "ad"]))

    clf.save(str(model_path))
    logger.info("Training complete")


if __name__ == "__main__":
    train()
