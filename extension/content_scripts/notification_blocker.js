/**
 * Notification Blocker — auto-deny Web Push notification permission prompts.
 *
 * Strategy:
 *   1. Override Notification.requestPermission → always return 'denied'
 *   2. Override Notification constructor → swallow notifications
 *   3. Hide custom (non-native) notification prompt overlays via CSS
 *   4. Auto-click "Block", "No Thanks", "Deny" in custom prompts
 */

(function () {
  'use strict';

  // ── Override native Notification API ─────────────────────────────────────
  try {
    Object.defineProperty(Notification, 'permission', {
      get: () => 'denied',
      configurable: false,
    });

    const _origRequest = Notification.requestPermission.bind(Notification);
    Notification.requestPermission = function (callback) {
      const p = Promise.resolve('denied');
      if (typeof callback === 'function') p.then(callback);
      return p;
    };

    // Swallow new Notification() calls
    window.Notification = class SilentNotification {
      constructor() {}
      close() {}
      addEventListener() {}
      removeEventListener() {}
    };
    Object.defineProperty(window.Notification, 'permission', { get: () => 'denied' });
    window.Notification.requestPermission = () => Promise.resolve('denied');
  } catch (_) {}

  // ── Hide custom notification prompt UIs ───────────────────────────────────
  const PROMPT_SELECTORS = [
    '.push-notification-prompt', '.notification-permission-prompt',
    '[class*="push-prompt"]', '[class*="notification-prompt"]',
    '[class*="subscribe-popup"]', '[class*="webpush"]',
    '[id*="push-prompt"]', '[id*="notification-prompt"]',
    '.pn-popup', '.pn-overlay',          // PushOwl / PushEngage
    '.onesignal-slidedown-container',    // OneSignal
    '#onesignal-popover-container',      // OneSignal
    '.pushwoosh-safari-dialog',          // Pushwoosh
    '[class*="wisepops"]',              // Wisepops
  ];

  function hidePrompts() {
    PROMPT_SELECTORS.forEach(sel => {
      document.querySelectorAll(sel).forEach(el =>
        el.style.setProperty('display', 'none', 'important')
      );
    });

    // Click deny buttons in custom prompts
    const denyPatterns = [
      /no,?\s*thanks?/i, /not\s*now/i, /deny/i, /block/i,
      /decline/i, /maybe\s*later/i, /don'?t\s*(allow|show)/i,
    ];
    document.querySelectorAll('button, [role="button"]').forEach(btn => {
      const text = (btn.textContent || '').trim();
      if (denyPatterns.some(p => p.test(text))) {
        // Only click if inside a notification-related container
        const parent = btn.closest(PROMPT_SELECTORS.join(','));
        if (parent) btn.click();
      }
    });
  }

  if (document.readyState !== 'loading') hidePrompts();
  else document.addEventListener('DOMContentLoaded', hidePrompts);

  new MutationObserver(hidePrompts)
    .observe(document.documentElement, { childList: true, subtree: true });
})();
