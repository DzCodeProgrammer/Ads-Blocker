/**
 * Service Worker — AdBlocker Pro v2.1 (MV3-compliant)
 *
 * MV3 Change: webRequest with ['blocking'] NOT allowed.
 * Blocking is done via declarativeNetRequest (DNR) dynamic rules.
 * webRequest is used ONLY for non-blocking observation (logging, badge).
 */

import { RequestHandler } from './request_handler.js';
import { NetworkLogger } from './network_logger.js';
import { URLCleaner } from './url_cleaner.js';
import { PopupBlocker } from './popup_blocker.js';
import { PerSiteManager } from './per_site.js';

const handler = new RequestHandler();
const logger = new NetworkLogger();
const cleaner = new URLCleaner();
const popupBlocker = new PopupBlocker();
const perSite = new PerSiteManager();

// ── Startup ──────────────────────────────────────────────────────────────────

chrome.runtime.onInstalled.addListener(async ({ reason }) => {
  console.log('[AdBlocker] Installed/updated:', reason);
  await init();
});

chrome.runtime.onStartup.addListener(async () => {
  await init();
});

async function init() {
  await handler.init();   // loads settings + syncs DNR rules
  await perSite.init();
  logger.start();
  popupBlocker.init();
  console.log('[AdBlocker] Ready');
}

// ── Non-blocking webRequest observation ──────────────────────────────────────
// MV3: NO ['blocking'] flag — this is observe-only for logging/badge/async checks

chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    // Skip internal URLs
    if (!details.url || details.url.startsWith('chrome') ||
        details.url.includes('127.0.0.1:8765') ||
        details.url.startsWith('chrome-extension://') ||
        details.url.startsWith('moz-extension://')) {
      return;
    }

    const { isTracker, knownBlocked } = handler.observeRequest(details);
    const domain = extractDomain(details.url);
    const tabDomain = extractDomain(details.documentUrl || details.initiator || '');
    const isThirdParty = !!(tabDomain && domain !== tabDomain &&
                            !domain.endsWith('.' + tabDomain));

    const status = knownBlocked ? 'blocked' : 'allowed';

    // Update badge counter for known blocked requests
    if (knownBlocked || isTracker) {
      sessionBlocked++;
      const label = sessionBlocked > 9999 ? '10k+' :
                    sessionBlocked > 999  ? `${Math.floor(sessionBlocked/1000)}k` :
                    String(sessionBlocked);
      chrome.action.setBadgeText({ text: label });
      chrome.action.setBadgeBackgroundColor({ color: '#E53E3E' });
    }

    // Log to backend (async, non-blocking)
    logger.log({
      url: details.url,
      domain,
      tabUrl: details.documentUrl || details.initiator,
      status,
      contentType: details.type || 'other',
      isThirdParty,
      isTracker,
      ruleMatched: knownBlocked ? domain : null,
    });
  },
  { urls: ['<all_urls>'] }
  // NOTE: No ['blocking'] here — MV3 blocks via DNR, not webRequest callback
);

// ── Track when DNR blocks a request (debug mode only, unpacked extensions) ──
if (chrome.declarativeNetRequest.onRuleMatchedDebug) {
  chrome.declarativeNetRequest.onRuleMatchedDebug.addListener((info) => {
    sessionBlocked++;
    const label = sessionBlocked > 999 ? `${Math.floor(sessionBlocked/1000)}k` : String(sessionBlocked);
    chrome.action.setBadgeText({ text: label });
    chrome.action.setBadgeBackgroundColor({ color: '#E53E3E' });

    logger.log({
      url: info.request.url,
      domain: extractDomain(info.request.url),
      tabUrl: info.request.documentUrl,
      status: 'blocked',
      contentType: info.request.type || 'other',
      isTracker: true,
      ruleMatched: `dnr:rule#${info.rule.ruleId}`,
    });
  });
}

// ── Session block counter ─────────────────────────────────────────────────────
let sessionBlocked = 0;

// ── URL tracking param cleaning ──────────────────────────────────────────────

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  if (details.frameId !== 0) return;
  if (!details.url || details.url.startsWith('chrome')) return;

  const { cleanedUrl, removedParams } = cleaner.clean(details.url);
  if (removedParams.length) {
    console.log(`[AdBlocker] Cleaned: removed ${removedParams.join(', ')}`);
    chrome.scripting.executeScript({
      target: { tabId: details.tabId },
      func: (url) => { try { history.replaceState(null, '', url); } catch (_) {} },
      args: [cleanedUrl],
      world: 'MAIN',
    }).catch(() => {});
  }
});

// ── Alarm: refresh domain cache + re-sync DNR every 5 min ────────────────────

chrome.alarms.create('refreshCache', { periodInMinutes: 5 });
chrome.alarms.onAlarm.addListener(async ({ name }) => {
  if (name === 'refreshCache') {
    await handler.refreshCache(); // also re-syncs DNR rules
  }
});

// ── Message bridge ────────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message, sender).then(sendResponse).catch(err =>
    sendResponse({ error: err.message })
  );
  return true;
});

async function handleMessage(message, sender) {
  switch (message.type) {
    case 'GET_STATS':        return handler.getStats();
    case 'GET_SETTINGS':     return handler.getSettings();
    case 'SET_SETTINGS':     return handler.setSettings(message.payload);
    case 'ADD_WHITELIST':    return handler.addWhitelist(message.domain || message.payload?.domain);
    case 'REMOVE_WHITELIST': return handler.removeWhitelist(message.id || message.payload?.id);
    case 'GET_WHITELIST':    return handler.getWhitelist();
    case 'TRIGGER_UPDATE':   return handler.triggerUpdate();
    case 'ADD_COSMETIC_RULE': return handler.addCosmeticRule(message.rule, message.selector);
    case 'PICKER_CLOSED':    return { status: 'ok' };
    case 'POPUP_BLOCKED':    return { status: 'ok' };
    default: return { error: `Unknown: ${message.type}` };
  }
}

// ── Helper ────────────────────────────────────────────────────────────────────

function extractDomain(url) {
  try { return new URL(url).hostname.replace(/^www\./, ''); }
  catch (_) { return ''; }
}
