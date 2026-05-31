/**
 * RequestHandler — all communication with the Python FastAPI backend.
 *
 * The backend runs locally at http://127.0.0.1:8765
 * Extension calls it synchronously-ish via blocking webRequest listener.
 *
 * NOTE: MV3 service workers cannot make synchronous XHR.
 * We use a local in-memory domain cache updated by periodic background fetch
 * so the onBeforeRequest handler can make synchronous decisions from cache.
 */

const BACKEND = 'http://127.0.0.1:8765';
const CACHE_TTL_MS = 60_000; // re-check backend every 60 s for hot rules

export class RequestHandler {
  constructor() {
    this._blockedDomains = new Set();  // fast in-memory cache
    this._settings = {
      is_enabled: true,
      block_ads: true,
      block_trackers: true,
      enable_ml: true,
    };
    this._stats = { blocked_today: 0, total_blocked: 0, tracker_blocked: 0 };
    this._lastCacheUpdate = 0;
  }

  // ── Init ────────────────────────────────────────────────────────────────

  async init() {
    await this._loadSettings();
    await this._refreshCache();
    // Periodic refresh
    setInterval(() => this._refreshCache(), CACHE_TTL_MS);
  }

  // ── Core request check ──────────────────────────────────────────────────

  onBeforeRequest(details) {
    if (!this._settings.is_enabled) return { cancel: false };
    if (!this._shouldCheck(details)) return { cancel: false };

    const url = details.url;
    const domain = this._extractDomain(url);

    // Fast-path cache check
    if (this._blockedDomains.has(domain)) {
      this._recordBlock(url, domain, details.documentUrl);
      return { cancel: true };
    }

    // Async backend check (non-blocking, updates cache for next request)
    this._checkBackendAsync(url, details.documentUrl);
    return { cancel: false };
  }

  _shouldCheck(details) {
    // Skip extension-internal and backend requests to avoid loops
    const skip = ['chrome-extension://', 'moz-extension://', '127.0.0.1:8765'];
    return !skip.some((s) => details.url.includes(s));
  }

  async _checkBackendAsync(url, tabUrl) {
    try {
      const res = await fetch(`${BACKEND}/api/filters/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, tab_url: tabUrl, enable_ml: this._settings.enable_ml }),
      });
      if (!res.ok) return;
      const data = await res.json();
      if (data.blocked) {
        this._blockedDomains.add(data.domain);
        // Update badge
        chrome.action.setBadgeText({ text: String(++this._stats.blocked_today) });
        chrome.action.setBadgeBackgroundColor({ color: '#E53E3E' });
      }
    } catch (_) {
      // Backend unreachable — fail open (don't block)
    }
  }

  _recordBlock(url, domain, tabUrl) {
    fetch(`${BACKEND}/api/filters/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, tab_url: tabUrl, enable_ml: false }),
    }).catch(() => {});
    this._stats.blocked_today++;
    chrome.action.setBadgeText({ text: String(this._stats.blocked_today) });
    chrome.action.setBadgeBackgroundColor({ color: '#E53E3E' });
  }

  // ── Cache refresh ───────────────────────────────────────────────────────

  async _refreshCache() {
    try {
      const res = await fetch(`${BACKEND}/api/filters?rule_type=blacklist`);
      if (!res.ok) return;
      const rules = await res.json();
      this._blockedDomains = new Set(rules.map((r) => r.pattern));
      this._lastCacheUpdate = Date.now();
    } catch (_) {}
  }

  // ── Settings ────────────────────────────────────────────────────────────

  async _loadSettings() {
    try {
      const res = await fetch(`${BACKEND}/api/settings`);
      if (res.ok) this._settings = await res.json();
    } catch (_) {}
  }

  async getSettings() {
    await this._loadSettings();
    return this._settings;
  }

  async setSettings(payload) {
    await fetch(`${BACKEND}/api/settings`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    this._settings = { ...this._settings, ...payload };
    return { status: 'updated' };
  }

  // ── Stats ───────────────────────────────────────────────────────────────

  async getStats() {
    try {
      const res = await fetch(`${BACKEND}/api/stats/summary`);
      if (res.ok) return await res.json();
    } catch (_) {}
    return this._stats;
  }

  // ── Whitelist ───────────────────────────────────────────────────────────

  async getWhitelist() {
    const res = await fetch(`${BACKEND}/api/whitelist`);
    return res.ok ? await res.json() : [];
  }

  async addWhitelist(domain) {
    const res = await fetch(`${BACKEND}/api/whitelist`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ domain }),
    });
    if (res.ok) this._blockedDomains.delete(domain);
    return res.ok ? { status: 'whitelisted' } : { error: 'Failed' };
  }

  async removeWhitelist(id) {
    const res = await fetch(`${BACKEND}/api/whitelist/${id}`, { method: 'DELETE' });
    return res.ok ? { status: 'removed' } : { error: 'Failed' };
  }

  // ── Admin ───────────────────────────────────────────────────────────────

  async triggerUpdate() {
    const res = await fetch(`${BACKEND}/api/filters/update`, { method: 'POST' });
    return res.ok ? await res.json() : { error: 'Update failed' };
  }

  // ── Helpers ─────────────────────────────────────────────────────────────

  _extractDomain(url) {
    try {
      return new URL(url).hostname.replace(/^www\./, '');
    } catch (_) {
      return '';
    }
  }
}
