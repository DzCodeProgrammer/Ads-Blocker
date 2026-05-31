/**
 * Content script — injected into every page at document_start.
 *
 * Responsibilities:
 *   1. Cosmetic filtering (hide ad elements by CSS selector)
 *   2. Script blocking heuristics (remove known ad scripts)
 *   3. Anti-fingerprinting: neutralise canvas/audio fingerprint APIs
 */

(function () {
  'use strict';

  // ── Cosmetic selectors (element-hide) ──────────────────────────────────
  const AD_SELECTORS = [
    '.ad', '.ads', '.ad-banner', '.ad-container', '.ad-wrapper',
    '.advertisement', '.ad-unit', '.advert', '.ad-slot',
    '#ad', '#ads', '#ad-container', '#ad-banner', '#advertisement',
    '[id^="ad-"]', '[id^="ads-"]', '[class*="ad-slot"]', '[class*="adsense"]',
    '[class*="adsbygoogle"]', '[class*="ad_unit"]',
    'ins.adsbygoogle', 'div[data-ad-slot]', 'div[data-ad-unit-id]',
    'iframe[src*="doubleclick"]', 'iframe[src*="googlesyndication"]',
    'iframe[src*="adnxs"]', 'iframe[src*="taboola"]', 'iframe[src*="outbrain"]',
    'div[id*="taboola"]', 'div[id*="outbrain"]',
    '.widget-area .textwidget > a > img',
    'amp-ad', 'amp-embed',
  ];

  // ── Block known ad scripts dynamically ────────────────────────────────
  const BLOCKED_SCRIPT_PATTERNS = [
    'pagead2.googlesyndication.com',
    'adservice.google.com',
    'doubleclick.net',
    'adnxs.com',
    'cdn.taboola.com',
    'widgets.outbrain.com',
    'hotjar.com',
    'connect.facebook.net/en_US/fbevents.js',
  ];

  // ── Cosmetic filter injection ──────────────────────────────────────────
  function injectCosmeticCSS() {
    const style = document.createElement('style');
    style.id = '__adblocker_cosmetic__';
    style.textContent = AD_SELECTORS.map((s) => `${s}{display:none!important}`).join('\n');
    (document.head || document.documentElement).appendChild(style);
  }

  // ── MutationObserver for dynamic ad elements ───────────────────────────
  function observeDynamicAds() {
    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (node.nodeType !== Node.ELEMENT_NODE) continue;
          if (matchesAdSelector(node)) {
            node.style.setProperty('display', 'none', 'important');
          }
          // Check newly added scripts
          if (node.tagName === 'SCRIPT' && node.src) {
            if (isBlockedScript(node.src)) node.remove();
          }
        }
      }
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  function matchesAdSelector(el) {
    return AD_SELECTORS.some((s) => {
      try { return el.matches(s); } catch (_) { return false; }
    });
  }

  function isBlockedScript(src) {
    return BLOCKED_SCRIPT_PATTERNS.some((p) => src.includes(p));
  }

  // ── Anti-fingerprinting ────────────────────────────────────────────────
  function applyAntiFingerprint() {
    // Canvas fingerprint noise
    const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function (...args) {
      const ctx = this.getContext('2d');
      if (ctx) {
        const imgData = ctx.getImageData(0, 0, this.width || 1, this.height || 1);
        // Add imperceptible noise
        for (let i = 0; i < Math.min(imgData.data.length, 40); i += 4) {
          imgData.data[i] = (imgData.data[i] + 1) & 0xff;
        }
        ctx.putImageData(imgData, 0, 0);
      }
      return origToDataURL.apply(this, args);
    };

    // AudioContext fingerprint
    const origGetChannelData = AudioBuffer.prototype.getChannelData;
    AudioBuffer.prototype.getChannelData = function (...args) {
      const data = origGetChannelData.apply(this, args);
      for (let i = 0; i < Math.min(data.length, 10); i++) {
        data[i] += Math.random() * 1e-7;
      }
      return data;
    };
  }

  // ── Bootstrap ──────────────────────────────────────────────────────────
  injectCosmeticCSS();
  observeDynamicAds();
  applyAntiFingerprint();

  // Remove any blocked scripts that are already in the DOM
  document.querySelectorAll('script[src]').forEach((s) => {
    if (isBlockedScript(s.src)) s.remove();
  });
})();
