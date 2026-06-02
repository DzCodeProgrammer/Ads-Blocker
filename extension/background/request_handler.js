/**
 * RequestHandler v2 — core blocking engine for the background service worker.
 *
 * Enhancements over v1:
 *   - Content-type filtering (block XHR/scripts/frames per type)
 *   - Per-site mode awareness (disabled / aggressive)
 *   - CNAME check via async backend call (updates cache)
 *   - Cosmetic rule accumulation
 *   - Callback for badge updates (onBlock)
 */

const BACKEND = 'http://127.0.0.1:8765';
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

export class RequestHandler {
  constructor() {
    this._blockedDomains = new Set();
    this._whitelistedDomains = new Set();
    this._settings = {
      is_enabled: true, block_ads: true, block_trackers: true,
      enable_ml: true, block_cookie_banners: true, block_social: true,
      block_popups: true, block_notifications: true, clean_urls: true,
      enable_cname: true, anti_fingerprint: true,
    };
    this._cosmeticRules = [];
    this._lastCacheUpdate = 0;
    this.onBlock = null; // callback for badge
  }

  // ── Init / Cache ──────────────────────────────────────────────────────────

  async init() {
    await this._loadSettings();
    await this.refreshCache();
    await this._loadWhitelist();
  }

  async refreshCache() {
    try {
      const [blRes, wlRes] = await Promise.all([
        fetch(`${BACKEND}/api/filters?rule_type=blacklist`),
        fetch(`${BACKEND}/api/filters?rule_type=whitelist`),
      ]);
      if (blRes.ok) {
        const rules = await blRes.json();
        this._blockedDomains = new Set(rules.map(r => r.pattern));
      }
      if (wlRes.ok) {
        const wl = await wlRes.json();
        this._whitelistedDomains = new Set(wl.map(r => r.pattern));
      }
      this._lastCacheUpdate = Date.now();
    } catch (_) {}
  }

  async _loadWhitelist() {
    try {
      const res = await fetch(`${BACKEND}/api/whitelist`);
      if (res.ok) {
        const items = await res.json();
        items.forEach(i => this._whitelistedDomains.add(i.domain));
      }
    } catch (_) {}
  }

  // ── Core request check ────────────────────────────────────────────────────

  onBeforeRequest(details, perSite) {
    if (!this._settings.is_enabled) return { cancel: false };

    const url = details.url;
    // Skip extension internals and backend
    if (url.includes('127.0.0.1:8765') || url.startsWith('chrome-extension://') ||
        url.startsWith('moz-extension://') || url.startsWith('ms-browser-extension://')) {
      return { cancel: false };
    }

    const domain = this._extractDomain(url);
    const tabDomain = this._extractDomain(details.documentUrl || details.initiator || '');
    const isThirdParty = tabDomain && domain !== tabDomain && !domain.endsWith('.' + tabDomain);

    // ── Per-site disable check ────────────────────────────────────────────
    if (perSite && tabDomain && perSite.isDisabled(tabDomain)) {
      return { cancel: false };
    }

    // ── Whitelist fast path ───────────────────────────────────────────────
    if (this._isWhitelisted(domain)) return { cancel: false };

    // ── Cache check (fast O(1) domain lookup) ────────────────────────────
    const etld1 = this._getETLD1(domain);
    if (this._blockedDomains.has(domain) || this._blockedDomains.has(etld1)) {
      this._reportBlock(url, domain, details);
      return { cancel: true, matchedRule: domain, isTracker: false };
    }

    // ── Tracker heuristic ─────────────────────────────────────────────────
    if (this._settings.block_trackers && this._isTracker(domain)) {
      this._reportBlock(url, domain, details);
      return { cancel: true, matchedRule: `tracker:${domain}`, isTracker: true };
    }

    // ── Content-type blocking (3rd-party scripts/XHR/frames) ─────────────
    if (isThirdParty && this._shouldBlockByType(details.type, perSite, tabDomain)) {
      this._reportBlock(url, domain, details);
      return { cancel: true, matchedRule: `type:${details.type}`, isTracker: false };
    }

    // ── Async backend check (updates cache for next hit) ─────────────────
    this._checkBackendAsync(url, details.documentUrl, details.type);

    return { cancel: false };
  }

  _shouldBlockByType(type, perSite, siteDomain) {
    if (!type) return false;
    const aggressive = perSite && siteDomain && perSite.isAggressive(siteDomain);
    // In aggressive mode: block all 3rd-party scripts, XHR, frames
    if (aggressive) return ['script', 'xmlhttprequest', 'sub_frame', 'websocket'].includes(type);
    // Normal: block websocket and ping only
    return ['websocket', 'ping'].includes(type);
  }

  async _checkBackendAsync(url, tabUrl, contentType) {
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
        if (typeof this.onBlock === 'function') this.onBlock(data.domain);
      }
    } catch (_) {}
  }

  _reportBlock(url, domain, details) {
    if (typeof this.onBlock === 'function') this.onBlock(domain);
  }

  // ── Settings ──────────────────────────────────────────────────────────────

  async _loadSettings() {
    try {
      const res = await fetch(`${BACKEND}/api/settings`);
      if (res.ok) this._settings = { ...this._settings, ...(await res.json()) };
    } catch (_) {}
  }

  async getSettings() {
    await this._loadSettings();
    return this._settings;
  }

  async setSettings(payload) {
    this._settings = { ...this._settings, ...payload };
    await fetch(`${BACKEND}/api/settings`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).catch(() => {});
    return { status: 'updated' };
  }

  // ── Stats ─────────────────────────────────────────────────────────────────

  async getStats() {
    try {
      const res = await fetch(`${BACKEND}/api/stats/summary`);
      return res.ok ? await res.json() : {};
    } catch (_) { return {}; }
  }

  // ── Whitelist ──────────────────────────────────────────────────────────────

  async getWhitelist() {
    try {
      const res = await fetch(`${BACKEND}/api/whitelist`);
      return res.ok ? await res.json() : [];
    } catch (_) { return []; }
  }

  async addWhitelist(domain) {
    if (!domain) return { error: 'No domain' };
    const res = await fetch(`${BACKEND}/api/whitelist`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ domain }),
    }).catch(() => null);
    if (res?.ok) {
      this._whitelistedDomains.add(domain);
      this._blockedDomains.delete(domain);
      return { status: 'whitelisted' };
    }
    return { error: 'Failed' };
  }

  async removeWhitelist(id) {
    const res = await fetch(`${BACKEND}/api/whitelist/${id}`, { method: 'DELETE' }).catch(() => null);
    await this._loadWhitelist(); // refresh cache
    return res?.ok ? { status: 'removed' } : { error: 'Failed' };
  }

  // ── Cosmetic rules ────────────────────────────────────────────────────────

  async addCosmeticRule(rule, selector) {
    this._cosmeticRules.push({ rule, selector });
    // Also save to backend as custom filter
    await fetch(`${BACKEND}/api/filters`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pattern: selector, rule_type: 'blacklist', comment: `Cosmetic: ${rule}` }),
    }).catch(() => {});
    return { status: 'added' };
  }

  // ── Trigger update ────────────────────────────────────────────────────────

  async triggerUpdate() {
    const res = await fetch(`${BACKEND}/api/filters/update`, { method: 'POST' }).catch(() => null);
    if (res?.ok) {
      await this.refreshCache();
      return await res.json();
    }
    return { error: 'Update failed' };
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  _isWhitelisted(domain) {
    return this._whitelistedDomains.has(domain) ||
      this._whitelistedDomains.has(this._getETLD1(domain));
  }

  _isTracker(domain) {
    const kws = [
      'doubleclick', 'googlesyndication', 'googletagmanager', 'analytics',
      'tracking', 'tracker', 'pixel', 'beacon', 'telemetry', 'hotjar',
      'mixpanel', 'segment.io', 'amplitude', 'fullstory', 'sentry.io',
      'criteo', 'taboola', 'outbrain', 'adnxs', 'quantserve', 'scorecardresearch',
    ];
    const dl = domain.toLowerCase();
    return kws.some(k => dl.includes(k));
  }

  _extractDomain(url) {
    try { return new URL(url).hostname.replace(/^www\./, ''); }
    catch (_) { return ''; }
  }

  _getETLD1(domain) {
    const parts = domain.split('.');
    return parts.length >= 2 ? parts.slice(-2).join('.') : domain;
  }
}
