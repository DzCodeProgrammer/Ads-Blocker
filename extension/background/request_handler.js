/**
 * RequestHandler v3 — MV3-compliant blocking via declarativeNetRequest (DNR).
 *
 * MV3 Chrome no longer allows webRequest with ['blocking'].
 * Actual request blocking is done by Chrome's declarativeNetRequest engine.
 * webRequest is used only for non-blocking observation (logging, badge).
 *
 * Architecture:
 *   1. Blocked domains → converted to DNR dynamic rules (blocks in Chrome engine)
 *   2. webRequest.onBeforeRequest (no 'blocking') → observe all requests for logging
 *   3. Backend ML/CNAME check → async, adds new DNR rules when threats detected
 */

const BACKEND = 'http://127.0.0.1:8765';
const DNR_RULE_ID_START = 1;
const MAX_DNR_RULES = 29_000;

// Well-known tracker keywords for heuristic fast-path
const TRACKER_KEYWORDS = [
  'doubleclick', 'googlesyndication', 'googletagmanager', 'analytics',
  'tracking', 'tracker', 'pixel', 'beacon', 'hotjar', 'mixpanel',
  'segment.io', 'amplitude', 'fullstory', 'sentry.io', 'criteo',
  'taboola', 'outbrain', 'adnxs', 'quantserve', 'scorecardresearch',
];

// Built-in tracker domains (always blocked even without filter lists)
const BUILTIN_BLOCK_DOMAINS = [
  'doubleclick.net', 'googlesyndication.com', 'googletagservices.com',
  'googletagmanager.com', 'adservice.google.com', 'adservice.google.co.uk',
  'ads.youtube.com', 'pagead2.googlesyndication.com',
  'connect.facebook.net', 'an.facebook.com', 'pixel.facebook.com',
  'bat.bing.com', 'ads.twitter.com', 'static.ads-twitter.com',
  'trc.taboola.com', 'cdn.taboola.com', 'widgets.outbrain.com',
  'amplify.outbrain.com', 'log.outbrain.com',
  'adnxs.com', 'ads.yahoo.com', 'ats.yahoo.com',
  'scorecardresearch.com', 'quantserve.com',
  'hotjar.com', 'static.hotjar.com', 'script.hotjar.com',
  'mixpanel.com', 'cdn.mxpnl.com',
  'amplitude.com', 'api.amplitude.com', 'api2.amplitude.com',
  'fullstory.com', 'rs.fullstory.com', 'edge.fullstory.com',
  'mouseflow.com', 'cdn.mouseflow.com',
  'crazyegg.com', 'script.crazyegg.com',
  'criteo.com', 'dis.criteo.com', 'static.criteo.net',
  'moatads.com', 'px.moatads.com',
  'doubleverify.com', 'cdn.doubleverify.com',
  'adsrvr.org', 'insight.adsrvr.org',
  'rubiconproject.com', 'fastlane.rubiconproject.com',
  'pubmatic.com', 'ads.pubmatic.com', 'image6.pubmatic.com',
  'openx.net', 'u.openx.net', 'ads.openx.net',
  'casalemedia.com', 'ssum-sec.casalemedia.com',
  'adsystem.com', 'adserver.com',
  'chartbeat.com', 'static.chartbeat.com',
  'newrelic.com', 'js-agent.newrelic.com', 'bam.nr-data.net',
  'sentry.io', 'ingest.sentry.io',
  'segment.io', 'api.segment.io', 'cdn.segment.com',
  'yieldmanager.com', 'adtech.com',
  'advertising.com', 'pixel.advertising.com',
  'exoclick.com', 'server.js.exoclick.com',
  'popads.net', 'popcash.net', 'adcash.com',
  'trafficjunky.net', 'juicyads.com',
];

export class RequestHandler {
  constructor() {
    this._blockedDomains = new Set(BUILTIN_BLOCK_DOMAINS);
    this._whitelistedDomains = new Set();
    this._settings = {
      is_enabled: true, block_ads: true, block_trackers: true,
      enable_ml: true, block_cookie_banners: true, block_social: true,
      block_popups: true, block_notifications: true, clean_urls: true,
      enable_cname: true, anti_fingerprint: true,
    };
    this.onBlock = null;
    this._dnrRuleCount = 0;
  }

  // ── Init ──────────────────────────────────────────────────────────────────

  async init() {
    await this._loadSettings();
    await this._loadWhitelist();
    await this.refreshCache();          // loads blocked domains from backend
    await this._syncDNRRules();         // push rules to Chrome DNR engine
  }

  // ── DNR Rule Management ───────────────────────────────────────────────────

  async _syncDNRRules() {
    if (!this._settings.is_enabled) {
      await this._clearDNRRules();
      return;
    }

    const domains = [...this._blockedDomains]
      .filter(d => !this._whitelistedDomains.has(d))
      .slice(0, MAX_DNR_RULES);

    const newRules = domains.map((domain, i) => ({
      id: DNR_RULE_ID_START + i,
      priority: 1,
      action: { type: 'block' },
      condition: {
        urlFilter: `||${domain}^`,
        resourceTypes: [
          'script', 'image', 'xmlhttprequest', 'sub_frame',
          'media', 'font', 'websocket', 'ping', 'other',
        ],
      },
    }));

    try {
      const existing = await chrome.declarativeNetRequest.getDynamicRules();
      await chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: existing.map(r => r.id),
        addRules: newRules,
      });
      this._dnrRuleCount = newRules.length;
      console.log(`[AdBlocker] DNR: ${newRules.length} rules synced`);
    } catch (err) {
      console.error('[AdBlocker] DNR sync error:', err.message);
    }
  }

  async _clearDNRRules() {
    try {
      const existing = await chrome.declarativeNetRequest.getDynamicRules();
      await chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: existing.map(r => r.id),
        addRules: [],
      });
    } catch (_) {}
  }

  async _addDNRRuleForDomain(domain) {
    const existing = await chrome.declarativeNetRequest.getDynamicRules();
    const nextId = existing.length > 0
      ? Math.max(...existing.map(r => r.id)) + 1
      : DNR_RULE_ID_START;

    const alreadyExists = existing.some(r =>
      r.condition?.urlFilter === `||${domain}^`
    );
    if (alreadyExists) return;

    await chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: [],
      addRules: [{
        id: nextId,
        priority: 1,
        action: { type: 'block' },
        condition: {
          urlFilter: `||${domain}^`,
          resourceTypes: ['script', 'image', 'xmlhttprequest', 'sub_frame',
                          'media', 'font', 'websocket', 'ping', 'other'],
        },
      }],
    });
  }

  // ── Observation (non-blocking) ────────────────────────────────────────────
  // Called from background.js webRequest.onBeforeRequest (no 'blocking' flag)

  observeRequest(details) {
    const url = details.url;
    if (url.includes('127.0.0.1:8765') ||
        url.startsWith('chrome-extension://') ||
        url.startsWith('moz-extension://') ||
        url.startsWith('data:') ||
        url.startsWith('chrome:')) {
      return { isTracker: false, knownBlocked: false };
    }

    const domain = this._extractDomain(url);
    const isTracker = this._isTracker(domain);

    // Check if domain is in our block set (will be/was blocked by DNR)
    const knownBlocked = this._blockedDomains.has(domain) ||
                         this._blockedDomains.has(this._getETLD1(domain));

    // Async: check backend for unknown domains, add to DNR if threat found
    if (!knownBlocked && !this._isWhitelisted(domain)) {
      this._checkBackendAsync(url, details.documentUrl, details.type);
    }

    // Fire badge callback for known blocked domains
    if (knownBlocked || isTracker) {
      if (typeof this.onBlock === 'function') this.onBlock(domain);
    }

    return { isTracker, knownBlocked };
  }

  async _checkBackendAsync(url, tabUrl, contentType) {
    try {
      const res = await fetch(`${BACKEND}/api/filters/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url, tab_url: tabUrl,
          enable_ml: this._settings.enable_ml,
        }),
      });
      if (!res.ok) return;
      const data = await res.json();
      if (data.blocked && data.domain) {
        if (!this._blockedDomains.has(data.domain)) {
          this._blockedDomains.add(data.domain);
          await this._addDNRRuleForDomain(data.domain);
        }
      }
    } catch (_) {}
  }

  // ── Cache refresh ─────────────────────────────────────────────────────────

  async refreshCache() {
    try {
      const [blRes, wlRes] = await Promise.all([
        fetch(`${BACKEND}/api/filters?rule_type=blacklist`).catch(() => null),
        fetch(`${BACKEND}/api/filters?rule_type=whitelist`).catch(() => null),
      ]);
      if (blRes?.ok) {
        const rules = await blRes.json();
        rules.forEach(r => this._blockedDomains.add(r.pattern));
      }
      if (wlRes?.ok) {
        const wl = await wlRes.json();
        wl.forEach(r => this._whitelistedDomains.add(r.pattern));
      }
    } catch (_) {}

    // Always add built-ins
    BUILTIN_BLOCK_DOMAINS.forEach(d => this._blockedDomains.add(d));
    await this._syncDNRRules();
  }

  async _loadWhitelist() {
    try {
      const res = await fetch(`${BACKEND}/api/whitelist`).catch(() => null);
      if (res?.ok) {
        const items = await res.json();
        items.forEach(i => this._whitelistedDomains.add(i.domain));
      }
    } catch (_) {}
  }

  // ── Settings ──────────────────────────────────────────────────────────────

  async _loadSettings() {
    try {
      const res = await fetch(`${BACKEND}/api/settings`).catch(() => null);
      if (res?.ok) this._settings = { ...this._settings, ...(await res.json()) };
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

    // If toggling main switch, sync DNR rules
    if ('is_enabled' in payload) await this._syncDNRRules();
    return { status: 'updated' };
  }

  // ── Stats ─────────────────────────────────────────────────────────────────

  async getStats() {
    try {
      const res = await fetch(`${BACKEND}/api/stats/summary`).catch(() => null);
      const data = res?.ok ? await res.json() : {};
      return { ...data, dnr_rules: this._dnrRuleCount };
    } catch (_) { return { dnr_rules: this._dnrRuleCount }; }
  }

  // ── Whitelist ──────────────────────────────────────────────────────────────

  async getWhitelist() {
    try {
      const res = await fetch(`${BACKEND}/api/whitelist`).catch(() => null);
      return res?.ok ? await res.json() : [];
    } catch (_) { return []; }
  }

  async addWhitelist(domain) {
    if (!domain) return { error: 'No domain' };
    try {
      const res = await fetch(`${BACKEND}/api/whitelist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain }),
      });
      if (res?.ok) {
        this._whitelistedDomains.add(domain);
        this._blockedDomains.delete(domain);
        await this._syncDNRRules();
        return { status: 'whitelisted' };
      }
    } catch (_) {}
    return { error: 'Failed' };
  }

  async removeWhitelist(id) {
    try {
      await fetch(`${BACKEND}/api/whitelist/${id}`, { method: 'DELETE' });
      await this._loadWhitelist();
      await this._syncDNRRules();
      return { status: 'removed' };
    } catch (_) { return { error: 'Failed' }; }
  }

  // ── Cosmetic rules ────────────────────────────────────────────────────────

  async addCosmeticRule(rule, selector) {
    await fetch(`${BACKEND}/api/filters`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pattern: selector, rule_type: 'blacklist',
        comment: `Cosmetic: ${rule}`,
      }),
    }).catch(() => {});
    return { status: 'added' };
  }

  // ── Trigger update ────────────────────────────────────────────────────────

  async triggerUpdate() {
    try {
      const res = await fetch(`${BACKEND}/api/filters/update`, { method: 'POST' });
      const data = res?.ok ? await res.json() : { error: 'Failed' };
      if (data.total_rules) {
        await this.refreshCache(); // also re-syncs DNR rules
      }
      return data;
    } catch (_) { return { error: 'Update failed' }; }
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  _isWhitelisted(domain) {
    return this._whitelistedDomains.has(domain) ||
      this._whitelistedDomains.has(this._getETLD1(domain));
  }

  _isTracker(domain) {
    const dl = domain.toLowerCase();
    return TRACKER_KEYWORDS.some(k => dl.includes(k));
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
