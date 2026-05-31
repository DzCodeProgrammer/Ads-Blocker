"""Integration tests for FastAPI routes."""
import pytest


class TestHealth:
    def test_health_ok(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"


class TestFilterRoutes:
    def test_check_benign_url(self, client):
        res = client.post("/api/filters/check", json={
            "url": "https://github.com/user/repo",
            "enable_ml": False,
        })
        assert res.status_code == 200
        data = res.json()
        assert "blocked" in data
        assert "domain" in data

    def test_check_invalid_url(self, client):
        res = client.post("/api/filters/check", json={"url": "not-a-url"})
        assert res.status_code == 422

    def test_check_url_too_long(self, client):
        res = client.post("/api/filters/check", json={"url": "https://x.com/" + "a" * 4100})
        assert res.status_code == 422

    def test_add_and_list_rule(self, client):
        # Add a custom blacklist rule
        res = client.post("/api/filters", json={
            "pattern": "bad-ads.example.com",
            "rule_type": "blacklist",
        })
        assert res.status_code == 201

        # It should now appear in the list
        res = client.get("/api/filters?rule_type=blacklist")
        assert res.status_code == 200
        patterns = [r["pattern"] for r in res.json()]
        assert "bad-ads.example.com" in patterns

    def test_add_invalid_pattern(self, client):
        res = client.post("/api/filters", json={
            "pattern": "<script>alert(1)</script>",
            "rule_type": "blacklist",
        })
        assert res.status_code == 422

    def test_delete_rule(self, client):
        # Add a rule first
        client.post("/api/filters", json={"pattern": "temp-domain.com", "rule_type": "blacklist"})
        rules = client.get("/api/filters").json()
        rule_id = next(r["id"] for r in rules if r["pattern"] == "temp-domain.com")

        # Delete it
        res = client.delete(f"/api/filters/{rule_id}")
        assert res.status_code == 200

    def test_delete_nonexistent(self, client):
        res = client.delete("/api/filters/99999")
        assert res.status_code == 404


class TestStatsRoutes:
    def test_summary(self, client):
        res = client.get("/api/stats/summary")
        assert res.status_code == 200
        data = res.json()
        assert "total_blocked" in data
        assert "blocked_today" in data

    def test_top_domains(self, client):
        res = client.get("/api/stats/top-domains?limit=5")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_daily_stats(self, client):
        res = client.get("/api/stats/daily?days=7")
        assert res.status_code == 200

    def test_limit_validation(self, client):
        res = client.get("/api/stats/top-domains?limit=200")
        assert res.status_code == 422


class TestSettingsRoutes:
    def test_get_defaults(self, client):
        res = client.get("/api/settings")
        assert res.status_code == 200
        data = res.json()
        assert "is_enabled" in data

    def test_update_setting(self, client):
        res = client.put("/api/settings", json={"dark_mode": True})
        assert res.status_code == 200
        # Verify persisted
        res2 = client.get("/api/settings")
        assert res2.json()["dark_mode"] is True


class TestWhitelistRoutes:
    def test_add_valid_domain(self, client):
        res = client.post("/api/whitelist", json={"domain": "example.com"})
        assert res.status_code == 201

    def test_add_invalid_domain(self, client):
        res = client.post("/api/whitelist", json={"domain": "not a domain!"})
        assert res.status_code == 422

    def test_list_whitelist(self, client):
        client.post("/api/whitelist", json={"domain": "safe.com"})
        res = client.get("/api/whitelist")
        assert res.status_code == 200
        assert any(r["domain"] == "safe.com" for r in res.json())

    def test_remove_whitelist(self, client):
        client.post("/api/whitelist", json={"domain": "toremove.com"})
        wl = client.get("/api/whitelist").json()
        rule_id = next(r["id"] for r in wl if r["domain"] == "toremove.com")
        res = client.delete(f"/api/whitelist/{rule_id}")
        assert res.status_code == 200
