/**
 * Cosmetic filter helper — parses EasyList element-hide rules and applies them.
 * Loaded as a module from content.js if advanced cosmetic rules are needed.
 */

export class CosmeticFilter {
  constructor() {
    this._rules = new Map(); // hostname → [selectors]
  }

  /**
   * @param {string} rule - EasyList cosmetic rule, e.g. "example.com##.ad"
   */
  addRule(rule) {
    const [hostPart, selector] = rule.split('##');
    const hosts = hostPart ? hostPart.split(',') : ['*'];
    for (const host of hosts) {
      const key = host.trim() || '*';
      if (!this._rules.has(key)) this._rules.set(key, []);
      this._rules.get(key).push(selector.trim());
    }
  }

  applyToDocument(hostname) {
    const selectors = [
      ...(this._rules.get('*') || []),
      ...(this._rules.get(hostname) || []),
    ];
    if (!selectors.length) return;

    const style = document.createElement('style');
    style.id = '__adblocker_cosmetic_rules__';
    style.textContent = selectors.map((s) => `${s}{display:none!important}`).join('\n');
    (document.head || document.documentElement).appendChild(style);
  }
}
