"""Unit tests for database repositories."""
import pytest
from datetime import datetime
from backend.models.filter_rule import FilterRule, RuleType
from backend.models.blocked_request import BlockedRequest
from backend.database.repositories.filter_repo import FilterRepository
from backend.database.repositories.stats_repo import StatsRepository


class TestFilterRepository:
    def test_add_and_retrieve(self, db_session):
        repo = FilterRepository(db_session)
        rule = FilterRule(pattern="ads.example.com", rule_type=RuleType.BLACKLIST, source="test")
        saved = repo.add(rule)
        assert saved.id is not None
        retrieved = repo.get_by_id(saved.id)
        assert retrieved.pattern == "ads.example.com"

    def test_get_all_active(self, db_session):
        repo = FilterRepository(db_session)
        repo.add(FilterRule(pattern="a.com", rule_type=RuleType.BLACKLIST, source="t"))
        repo.add(FilterRule(pattern="b.com", rule_type=RuleType.WHITELIST, source="t"))
        all_active = repo.get_all_active()
        assert len(all_active) == 2

    def test_filter_by_type(self, db_session):
        repo = FilterRepository(db_session)
        repo.add(FilterRule(pattern="bl.com", rule_type=RuleType.BLACKLIST, source="t"))
        repo.add(FilterRule(pattern="wl.com", rule_type=RuleType.WHITELIST, source="t"))
        blacklist = repo.get_blacklist()
        assert all(r.rule_type == RuleType.BLACKLIST for r in blacklist)

    def test_deactivate(self, db_session):
        repo = FilterRepository(db_session)
        rule = repo.add(FilterRule(pattern="del.com", rule_type=RuleType.BLACKLIST, source="t"))
        ok = repo.deactivate(rule.id)
        assert ok is True
        active = repo.get_all_active()
        assert all(r.id != rule.id for r in active)

    def test_deactivate_nonexistent(self, db_session):
        repo = FilterRepository(db_session)
        ok = repo.deactivate(99999)
        assert ok is False

    def test_delete_by_source(self, db_session):
        repo = FilterRepository(db_session)
        repo.add(FilterRule(pattern="x.com", rule_type=RuleType.EASYLIST, source="https://easylist.to"))
        repo.add(FilterRule(pattern="y.com", rule_type=RuleType.EASYLIST, source="https://easylist.to"))
        deleted = repo.delete_by_source("https://easylist.to")
        assert deleted == 2

    def test_bulk_insert(self, db_session):
        repo = FilterRepository(db_session)
        rules = [FilterRule(pattern=f"bulk{i}.com", rule_type=RuleType.BLACKLIST, source="bulk") for i in range(5)]
        count = repo.bulk_insert(rules)
        assert count == 5

    def test_count_by_type(self, db_session):
        repo = FilterRepository(db_session)
        repo.add(FilterRule(pattern="c1.com", rule_type=RuleType.BLACKLIST, source="t"))
        repo.add(FilterRule(pattern="c2.com", rule_type=RuleType.WHITELIST, source="t"))
        counts = repo.count_by_type()
        assert counts.get("blacklist", 0) >= 1


class TestStatsRepository:
    def test_record_and_total(self, db_session):
        repo = StatsRepository(db_session)
        repo.record(BlockedRequest(url="https://ad.com/", domain="ad.com"))
        assert repo.total_blocked() >= 1

    def test_blocked_today(self, db_session):
        repo = StatsRepository(db_session)
        repo.record(BlockedRequest(
            url="https://ad.com/pixel",
            domain="ad.com",
            blocked_at=datetime.utcnow(),
        ))
        assert repo.blocked_today() >= 1

    def test_top_domains(self, db_session):
        repo = StatsRepository(db_session)
        for _ in range(3):
            repo.record(BlockedRequest(url="https://x.com/", domain="x.com"))
        for _ in range(1):
            repo.record(BlockedRequest(url="https://y.com/", domain="y.com"))
        top = repo.top_domains(limit=2)
        assert top[0]["domain"] == "x.com"
        assert top[0]["count"] == 3

    def test_tracker_count(self, db_session):
        repo = StatsRepository(db_session)
        repo.record(BlockedRequest(url="https://t.com/", domain="t.com", is_tracker=True))
        repo.record(BlockedRequest(url="https://n.com/", domain="n.com", is_tracker=False))
        assert repo.tracker_count() >= 1
