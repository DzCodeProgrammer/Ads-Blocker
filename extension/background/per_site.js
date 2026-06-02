/**
 * Per-Site Manager — cache and sync per-domain blocking modes.
 *
 * Modes: 'normal' | 'aggressive' | 'disabled'
 * Synced with backend /api/site-settings.
 */

const BACKEND = 'http://127.0.0.1:8765';

export class PerSiteManager {
  constructor() {
    this._cache = new Map(); // domain → { mode, ... }
    this._loaded = false;
  }

  async init() {
    await this._loadAll();
  }

  async _loadAll() {
    try {
      const res = await fetch(`${BACKEND}/api/site-settings`);
      if (!res.ok) return;
      const data = await res.json();
      data.forEach(s => this._cache.set(s.domain, s));
      this._loaded = true;
    } catch (_) {}
  }

  getMode(domain) {
    const setting = this._cache.get(domain);
    return setting ? setting.mode : 'normal';
  }

  isDisabled(domain) {
    return this.getMode(domain) === 'disabled';
  }

  isAggressive(domain) {
    return this.getMode(domain) === 'aggressive';
  }

  async setMode(domain, mode) {
    this._cache.set(domain, { ...(this._cache.get(domain) || {}), domain, mode });
    try {
      await fetch(`${BACKEND}/api/site-settings/${encodeURIComponent(domain)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode }),
      });
    } catch (_) {}
  }

  async resetDomain(domain) {
    this._cache.delete(domain);
    try {
      await fetch(`${BACKEND}/api/site-settings/${encodeURIComponent(domain)}`, {
        method: 'DELETE',
      });
    } catch (_) {}
  }

  async getForDomain(domain) {
    try {
      const res = await fetch(`${BACKEND}/api/site-settings/${encodeURIComponent(domain)}`);
      if (res.ok) {
        const data = await res.json();
        this._cache.set(domain, data);
        return data;
      }
    } catch (_) {}
    return { domain, mode: 'normal' };
  }
}
