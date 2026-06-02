/**
 * Cookie Banner Auto-Dismisser — automatically rejects / dismisses GDPR consent dialogs.
 *
 * Strategy:
 *   1. CSS cosmetic filter — hide known consent overlay elements
 *   2. Click-to-reject — automatically click "Reject All" / "Decline" buttons
 *   3. Restore scroll — some sites lock scroll while banner is visible
 *
 * Covers: Cookiebot, OneTrust, Quantcast, TrustArc, Usercentrics, Didomi,
 *         ConsentManager, Cookie Information, and 50+ generic selectors.
 */

(function () {
  'use strict';

  // ── CSS selectors to hide immediately ─────────────────────────────────────
  const HIDE_SELECTORS = [
    // Generic cookie overlay containers
    '#cookie-banner', '#cookie-notice', '#cookie-consent', '#cookie-overlay',
    '#cookiebanner', '#cookienotice', '#cookieconsent', '#cookiebar',
    '#gdpr-banner', '#gdpr-notice', '#gdpr-consent', '#gdpr-popup',
    '.cookie-banner', '.cookie-notice', '.cookie-consent', '.cookie-bar',
    '.cookie-overlay', '.cookie-popup', '.cookie-wall', '.cookie-modal',
    '.gdpr-banner', '.gdpr-notice', '.gdpr-consent', '.gdpr-popup',
    '.consent-banner', '.consent-popup', '.consent-overlay',
    // Specific CMPs
    '#CybotCookiebotDialog',          // Cookiebot
    '#onetrust-consent-sdk',          // OneTrust
    '.onetrust-pc-dark-filter',       // OneTrust backdrop
    '#qcCmpUi',                       // Quantcast
    '.qc-cmp2-container',             // Quantcast v2
    '#truste-consent-track',          // TrustArc
    '.truste_overlay',                // TrustArc
    '#usercentrics-root',             // Usercentrics
    '.didomi-popup-container',        // Didomi
    '#didomi-host',                   // Didomi
    '.didomi-notice',                 // Didomi
    '.cm-popup-holder',               // ConsentManager
    '#CookieConsent',                 // Cookie Information
    '.cc-window',                     // Cookie Consent JS
    '.cookieconsent',                 // cookieconsent library
    '#cookie-law-info-bar',           // Cookie Law Info (WP plugin)
    '.pum-overlay',                   // Popup Maker
    '.fc-consent-root',               // Funding Choices
    '.fc-dialog-overlay',             // Funding Choices overlay
    '#sp-cc',                         // SourcePoint
    '.sp_choice_type_ACCEPT_ALL',     // SourcePoint
    '[id^="sp_message"]',             // SourcePoint generic
    '.evidon-banner',                 // Evidon
    '.ot-sdk-container',              // OneTrust SDK
    '#ot-sdk-btn-floating',           // OneTrust floating button
    'div[aria-label*="cookie"]',      // Aria-labelled cookie dialogs
    'div[aria-label*="consent"]',
    'div[aria-label*="privacy"]',
    'div[role="dialog"][class*="cookie"]',
    'div[role="alertdialog"][class*="cookie"]',
    // Site-specific
    '.snigel-cmp-framework',          // Snigel
    '#axeptio_overlay',               // Axeptio
    '.axeptio_overlay',
    '#klaro',                         // Klaro
    '.klaro',
    '#moove_gdpr_cookie_modal',       // GDPR Cookie Compliance (WP)
    '#moove_gdpr_cookie_info_bar',
    '.cookie-information-popup-v2',   // Cookie Information
    '[data-nosnippet] [class*="cookie"]',
  ];

  // ── Text patterns for "reject/decline" buttons ──────────────────────────
  const REJECT_PATTERNS = [
    /^reject\s*(all)?$/i,
    /^decline(\s*all)?$/i,
    /^no,?\s*thanks?$/i,
    /^no\s*thank/i,
    /^refuse(\s*all)?$/i,
    /^deny(\s*all)?$/i,
    /^disagree$/i,
    /^continue\s*without\s*(accepting|cookies)/i,
    /^manage\s*(preferences|cookies|settings)$/i,
    /^tolak$/i,        // Indonesian
    /^ablehnen$/i,     // German
    /^refuser?$/i,     // French
    /^rechazar?$/i,    // Spanish
    /^rifiuta/i,       // Italian
    /^rejeitar?$/i,    // Portuguese
    /^отклонить/i,     // Russian
  ];

  // ── Inject cosmetic CSS ───────────────────────────────────────────────────
  function injectHideCSS() {
    const style = document.createElement('style');
    style.id = '__adblock_cookie_css__';
    style.textContent = HIDE_SELECTORS
      .map(s => `${s}{display:none!important;visibility:hidden!important}`)
      .join('\n');
    (document.head || document.documentElement).appendChild(style);
  }

  // ── Click reject buttons ─────────────────────────────────────────────────
  function clickRejectButtons() {
    const buttons = document.querySelectorAll(
      'button, a[role="button"], [class*="cookie"] button, [class*="consent"] button, [class*="gdpr"] button'
    );
    for (const btn of buttons) {
      const text = (btn.textContent || btn.innerText || btn.value || '').trim();
      if (REJECT_PATTERNS.some(p => p.test(text))) {
        btn.click();
        return true;
      }
    }
    return false;
  }

  // ── Restore body scroll (some sites lock it) ──────────────────────────────
  function restoreScroll() {
    if (document.body.style.overflow === 'hidden') {
      document.body.style.overflow = '';
    }
    if (document.documentElement.style.overflow === 'hidden') {
      document.documentElement.style.overflow = '';
    }
    // Remove common overlay classes
    document.body.classList.remove('noscroll', 'no-scroll', 'overflow-hidden', 'modal-open');
    document.documentElement.classList.remove('noscroll', 'no-scroll');
  }

  // ── Local storage / cookie opt-outs ──────────────────────────────────────
  function setOptOutStorage() {
    // Common storage keys used by consent managers
    const optOuts = {
      'CookieConsent': '{stamp:%22rejected%22,necessary:true,preferences:false,statistics:false,marketing:false}',
      'cookie_consent': 'rejected',
      'gdpr_consent': '0',
      'cookieconsent_status': 'dismiss',
      'cookies_accepted': 'false',
    };
    try {
      Object.entries(optOuts).forEach(([k, v]) => localStorage.setItem(k, v));
    } catch (_) {}
  }

  // ── Main runner ───────────────────────────────────────────────────────────
  function run() {
    injectHideCSS();
    setOptOutStorage();
    clickRejectButtons();
    restoreScroll();
  }

  // Run immediately and observe DOM for dynamically injected banners
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }

  const obs = new MutationObserver(() => {
    clickRejectButtons();
    restoreScroll();
  });
  obs.observe(document.documentElement, { childList: true, subtree: true });

  // Retry a few times for late-loading CMPs
  [500, 1500, 3000].forEach(ms => setTimeout(run, ms));
})();
