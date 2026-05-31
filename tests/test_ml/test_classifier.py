"""Unit tests for ML feature extractor and classifier."""
import pytest
from ml_engine.feature_extractor import FeatureExtractor, _shannon_entropy, _digit_ratio
from ml_engine.classifier import AdClassifier


class TestFeatureExtractor:
    def setup_method(self):
        self.fe = FeatureExtractor()

    def test_returns_correct_feature_count(self):
        features = self.fe.extract("https://github.com/user/repo")
        assert len(features) == len(FeatureExtractor.FEATURE_NAMES)

    def test_ad_domain_has_more_keywords(self):
        ad_features = self.fe.extract("https://ads.doubleclick.net/click?id=1")
        benign_features = self.fe.extract("https://github.com/repos")
        # ad_keyword_count_domain should be higher for the ad URL
        kw_idx = FeatureExtractor.FEATURE_NAMES.index("ad_keyword_count_domain")
        assert ad_features[kw_idx] >= benign_features[kw_idx]

    def test_ip_detection(self):
        features = self.fe.extract("https://192.168.1.1/track.gif")
        ip_idx = FeatureExtractor.FEATURE_NAMES.index("has_ip_address")
        assert features[ip_idx] == 1

    def test_suspicious_tld(self):
        features = self.fe.extract("https://ads.download/banner")
        tld_idx = FeatureExtractor.FEATURE_NAMES.index("suspicious_tld")
        assert features[tld_idx] == 1

    def test_redirect_param(self):
        features = self.fe.extract("https://example.com/go?url=https://other.com")
        redir_idx = FeatureExtractor.FEATURE_NAMES.index("has_redirect_param")
        assert features[redir_idx] == 1

    def test_entropy_nonzero(self):
        assert _shannon_entropy("abcdef") > 0
        assert _shannon_entropy("") == 0

    def test_digit_ratio(self):
        assert _digit_ratio("12345") == 1.0
        assert _digit_ratio("abcde") == 0.0
        assert _digit_ratio("") == 0.0

    def test_batch_extract(self):
        urls = ["https://example.com", "https://ads.com/track"]
        batch = self.fe.extract_batch(urls)
        assert len(batch) == 2
        assert all(len(f) == len(FeatureExtractor.FEATURE_NAMES) for f in batch)


class TestAdClassifier:
    def test_train_and_predict(self):
        clf = AdClassifier()
        ad_urls = [
            "https://ads.doubleclick.net/pixel?id=1",
            "https://pagead2.googlesyndication.com/ads",
            "https://tracking.example.com/click?ad=1",
        ] * 10
        benign_urls = [
            "https://github.com/user/repo",
            "https://docs.python.org/3/library",
            "https://stackoverflow.com/questions/1",
        ] * 10

        urls = ad_urls + benign_urls
        labels = [1] * len(ad_urls) + [0] * len(benign_urls)
        clf.train(urls, labels)

        assert clf.is_ready
        score = clf.predict_proba("https://ads.doubleclick.net/pixel?id=99")
        assert 0.0 <= score <= 1.0

    def test_predict_without_training_raises(self):
        clf = AdClassifier()
        with pytest.raises(RuntimeError):
            clf.predict("https://example.com")

    def test_save_and_load(self, tmp_path):
        clf = AdClassifier()
        urls = ["https://ad.example.com"] * 5 + ["https://github.com"] * 5
        labels = [1] * 5 + [0] * 5
        clf.train(urls, labels)

        model_file = str(tmp_path / "model.joblib")
        clf.save(model_file)

        clf2 = AdClassifier(model_file)
        assert clf2.is_ready
        score = clf2.predict_proba("https://ad.example.com")
        assert 0.0 <= score <= 1.0
