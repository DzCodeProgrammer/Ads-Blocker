/**
 * Service Worker — AdBlocker Pro v2.0
 *
 * Integrates:
 *   - RequestHandler   (core URL blocking, CNAME, content-type)
 *   - NetworkLogger    (async log to backend)
 *   - URLCleaner       (strip tracking params)
 *   - PopupBlocker     (block window.open ad popups)
 *   - PerSiteManager   (per-domain disable/aggressive mode)
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
  await handler.init();
  await perSite.init();
  logger.start();
  popupBlocker.init();
  console.log('[AdBlocker] Ready');
}

// ── webRequest intercept ─────────────────────────────────────────────────────

chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    const result = handler.onBeforeRequest(details, perSite);

    // Log every request (blocked or not) to network logger
    if (details.url && !details.url.includes('127.0.0.1:8765')) {
      const domain = extractDomain(details.url);
      const tabDomain = details.documentUrl ? extractDomain(details.documentUrl) : '';
      const isThirdParty = tabDomain && domain !== tabDomain && !domain.endsWith('.' + tabDomain);

      logger.log({
        url: details.url,
        domain,
        tabUrl: details.documentUrl || details.initiator,
        status: result?.cancel ? 'blocked' : 'allowed',
        contentType: details.type || 'other',
        isThirdParty: !!isThirdParty,
        ruleMatched: result?.matchedRule || null,
        isTracker: result?.isTracker || false,
      });
    }

    return result || { cancel: false };
  },
  { urls: ['<all_urls>'] },
  ['blocking']
);

// ── URL tracking param cleaning (navigation URLs) ──────────────────────────

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  if (details.frameId !== 0) return; // top-level only
  if (!details.url || details.url.startsWith('chrome')) return;

  const { cleanedUrl, removedParams } = cleaner.clean(details.url);
  if (removedParams.length) {
    console.log(`[AdBlocker] Cleaned URL: removed ${removedParams.join(', ')}`);
    // Log cleaned URL
    logger.log({
      url: details.url,
      domain: extractDomain(details.url),
      status: 'cleaned',
      cleanedUrl,
    });
    // Redirect to clean URL via declarativeNetRequest would require rules;
    // instead we inject a script to replace history state
    chrome.scripting.executeScript({
      target: { tabId: details.tabId },
      func: (url) => { history.replaceState(null, '', url); },
      args: [cleanedUrl],
      world: 'MAIN',
    }).catch(() => {});
  }
});

// ── Badge update ──────────────────────────────────────────────────────────────

let sessionBlocked = 0;

handler.onBlock = () => {
  sessionBlocked++;
  chrome.action.setBadgeText({ text: sessionBlocked > 999 ? '1k+' : String(sessionBlocked) });
  chrome.action.setBadgeBackgroundColor({ color: '#E53E3E' });
};

// ── Alarm: refresh cache every 5 minutes ─────────────────────────────────────

chrome.alarms.create('refreshCache', { periodInMinutes: 5 });
chrome.alarms.onAlarm.addListener(({ name }) => {
  if (name === 'refreshCache') handler.refreshCache();
});

// ── Message bridge (popup ↔ content scripts ↔ service worker) ────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message, sender).then(sendResponse).catch(err =>
    sendResponse({ error: err.message })
  );
  return true;
});

async function handleMessage(message, sender) {
  switch (message.type) {
    case 'GET_STATS':      return handler.getStats();
    case 'GET_SETTINGS':   return handler.getSettings();
    case 'SET_SETTINGS':   return handler.setSettings(message.payload);
    case 'ADD_WHITELIST':  return handler.addWhitelist(message.domain || message.payload?.domain);
    case 'REMOVE_WHITELIST': return handler.removeWhitelist(message.id || message.payload?.id);
    case 'GET_WHITELIST':  return handler.getWhitelist();
    case 'TRIGGER_UPDATE': return handler.triggerUpdate();
    case 'ADD_COSMETIC_RULE': return handler.addCosmeticRule(message.rule, message.selector);
    case 'PICKER_CLOSED':  return { status: 'ok' };
    case 'POPUP_BLOCKED':  return { status: 'ok' };
    default: return { error: 'Unknown message type: ' + message.type };
  }
}

// ── Helper ────────────────────────────────────────────────────────────────────

function extractDomain(url) {
  try { return new URL(url).hostname.replace(/^www\./, ''); }
  catch (_) { return ''; }
}
