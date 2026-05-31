"""Unit tests for filter engine and URL matcher."""
import pytest
from backend.filters.url_matcher import UrlMatcher
from backend.filters.easylist_parser import EasyListParser
from backend.filters.filter_engine import FilterEngine


class TestUrlMatcher:
    def setup_method(self):
        self.matcher = UrlMatcher()

    def test_exact_domain_blocked(self):
        self.matcher.add_domain("ads.example.com")
        blocked, rule = self.matcher.should_block("https://ads.example.com/banner.gif")
        assert blocked is True
        assert rule is not None

    def test_etld1_blocked(self):
        self.matcher.add_domain("doubleclick.net")
        blocked, _ = self.matcher.should_block("https://ad.doubleclick.net/track?id=123")
        assert blocked is True

    def test_benign_url_not_blocked(self):
        self.matcher.add_domain("ads.evil.com")
        blocked, _ = self.matcher.should_block("https://github.com/repos")
        assert blocked is False

    def test_whitelist_overrides_blacklist(self):
        self.matcher.add_domain("example.com")           # blacklist
        self.matcher.add_domain("example.com", is_whitelist=True)  # whitelist
        blocked, _ = self.matcher.should_block("https://example.com/page")
        assert blocked is False

    def test_substring_match(self):
        self.matcher.add_substring("pixel.gif")
        blocked, _ = self.matcher.should_block("https://tracker.com/pixel.gif?id=1")
        assert blocked is True

    def test_regex_match(self):
        self.matcher.add_regex(r"ads\d+\.js")
        blocked, _ = self.matcher.should_block("https://example.com/ads99.js")
        assert blocked is True

    def test_invalid_regex_does_not_crash(self):
        self.matcher.add_regex(r"[invalid")  # malformed regex
        blocked, _ = self.matcher.should_block("https://example.com/safe")
        assert blocked is False


class TestEasyListParser:
    def setup_method(self):
        self.parser = EasyListParser()

    def test_domain_anchor(self):
        rules = self.parser.parse("||ads.example.com^")
        assert len(rules) == 1
        assert rules[0].pattern == "ads.example.com"
        assert not rules[0].is_exception

    def test_exception_rule(self):
        rules = self.parser.parse("@@||good.example.com^")
        assert len(rules) == 1
        assert rules[0].is_exception is True

    def test_cosmetic_rule_parsed(self):
        rules = self.parser.parse("example.com##.ad-banner")
        assert len(rules) == 1
        assert rules[0].is_cosmetic is True

    def test_comment_ignored(self):
        rules = self.parser.parse("! This is a comment")
        assert len(rules) == 0

    def test_header_ignored(self):
        rules = self.parser.parse("[Adblock Plus 2.0]")
        assert len(rules) == 0

    def test_options_parsed(self):
        rules = self.parser.parse("||ads.com^$third-party,script")
        assert "third-party" in rules[0].options or "script" in rules[0].options

    def test_regex_rule(self):
        rules = self.parser.parse("/ads[0-9]+\\.js/")
        assert len(rules) == 1
        assert rules[0].is_regex is True


class TestFilterEngine:
    def test_tracker_detection(self):
        engine = FilterEngine()
        result = engine.check_url("https://analytics.google.com/collect?v=1", enable_ml=False)
        assert result.is_tracker is True

    def test_benign_not_blocked_empty_engine(self):
        engine = FilterEngine()
        result = engine.check_url("https://github.com/user/repo", enable_ml=False)
        assert result.blocked is False
