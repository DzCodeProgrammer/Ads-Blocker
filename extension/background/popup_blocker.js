/**
 * Popup Blocker — block window.open() and tab-opening ad popups.
 *
 * MV3 approach: intercept window creation via webNavigation + heuristics.
 * Also injects content script override for window.open in the main world.
 */

export class PopupBlocker {
  constructor() {
    this._allowedHosts = new Set(); // temporary allow per-tab
  }

  init() {
    // Block new windows opened from ad domains
    chrome.webNavigation.onCreatedNavigationTarget.addListener(
      (details) => this._onCreatedTarget(details)
    );
  }

  _onCreatedTarget(details) {
    const { sourceTabId, url, tabId } = details;
    if (!url || url === 'about:blank') return;

    // Allow user-initiated new tabs (sourceTabId same as opener, sourceFrameId=0)
    if (details.sourceFrameId === 0) return; // top-level navigation — likely user intent

    const hostname = this._extractHost(url);
    if (!hostname) return;

    // Block popups from known ad/tracker domains
    if (this._isAdDomain(hostname)) {
      chrome.tabs.remove(tabId).catch(() => {});
      console.log(`[AdBlocker] Popup blocked: ${url}`);
      this._notifyBlocked(sourceTabId, url);
    }
  }

  _isAdDomain(hostname) {
    const ad_keywords = [
      'doubleclick', 'adnxs', 'adsystem', 'googlesyndication',
      'adclick', 'ad-click', 'popup', 'popunder', 'pop-under',
      'popads', 'popcash', 'adcash', 'propellerads',
      'trafficjunky', 'juicyads', 'exoclick', 'traffic-media',
    ];
    const h = hostname.toLowerCase();
    return ad_keywords.some(kw => h.includes(kw));
  }

  _notifyBlocked(tabId, url) {
    chrome.tabs.sendMessage(tabId, {
      type: 'POPUP_BLOCKED',
      url,
    }).catch(() => {});
  }

  _extractHost(url) {
    try { return new URL(url).hostname; } catch (_) { return ''; }
  }

  allowPopupsFrom(host) {
    this._allowedHosts.add(host);
    setTimeout(() => this._allowedHosts.delete(host), 30_000);
  }
}
