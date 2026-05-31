/**
 * Service Worker — Manifest V3 background script.
 *
 * Intercepts all web requests, forwards URLs to the Python backend,
 * and cancels requests that should be blocked.
 */

import { RequestHandler } from './request_handler.js';

const handler = new RequestHandler();

// ── Startup ────────────────────────────────────────────────────────────────

chrome.runtime.onInstalled.addListener(async () => {
  console.log('[AdBlocker] Extension installed');
  await handler.init();
});

chrome.runtime.onStartup.addListener(async () => {
  await handler.init();
});

// ── webRequest intercept ───────────────────────────────────────────────────

chrome.webRequest.onBeforeRequest.addListener(
  (details) => handler.onBeforeRequest(details),
  { urls: ['<all_urls>'] },
  ['blocking']
);

// ── Message bridge (popup ↔ service worker) ────────────────────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message, sender)
    .then(sendResponse)
    .catch((err) => sendResponse({ error: err.message }));
  return true; // keep channel open for async response
});

async function handleMessage(message, sender) {
  switch (message.type) {
    case 'GET_STATS':
      return handler.getStats();
    case 'GET_SETTINGS':
      return handler.getSettings();
    case 'SET_SETTINGS':
      return handler.setSettings(message.payload);
    case 'ADD_WHITELIST':
      return handler.addWhitelist(message.domain);
    case 'REMOVE_WHITELIST':
      return handler.removeWhitelist(message.id);
    case 'GET_WHITELIST':
      return handler.getWhitelist();
    case 'TRIGGER_UPDATE':
      return handler.triggerUpdate();
    default:
      return { error: 'Unknown message type' };
  }
}
