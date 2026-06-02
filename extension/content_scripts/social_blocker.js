/**
 * Social Widget Blocker — replaces Facebook, Twitter, LinkedIn, Instagram,
 * YouTube embed widgets with privacy-respecting placeholders.
 *
 * Inspired by Privacy Badger's social widget replacement.
 * Widgets are only loaded if the user explicitly clicks the placeholder.
 */

(function () {
  'use strict';

  const WIDGETS = [
    // Facebook
    {
      name: 'Facebook Like',
      selector: 'iframe[src*="facebook.com/plugins"]',
      color: '#1877f2',
    },
    {
      name: 'Facebook Share',
      selector: '.fb-share-button, .fb-like, .fb_iframe_widget',
      color: '#1877f2',
    },
    // Twitter / X
    {
      name: 'X (Twitter)',
      selector: '.twitter-share-button, .twitter-follow-button, iframe[src*="platform.twitter.com"]',
      color: '#1da1f2',
    },
    // LinkedIn
    {
      name: 'LinkedIn Share',
      selector: '.linkedin-share-button, iframe[src*="linkedin.com/in/"]',
      color: '#0a66c2',
    },
    // Instagram
    {
      name: 'Instagram',
      selector: 'iframe[src*="instagram.com/embed"]',
      color: '#c13584',
    },
    // YouTube
    {
      name: 'YouTube',
      selector: 'iframe[src*="youtube.com/embed"], iframe[src*="youtube-nocookie.com"]',
      color: '#ff0000',
    },
    // TikTok
    {
      name: 'TikTok',
      selector: 'iframe[src*="tiktok.com"], blockquote.tiktok-embed',
      color: '#010101',
    },
    // Spotify
    {
      name: 'Spotify',
      selector: 'iframe[src*="open.spotify.com/embed"]',
      color: '#1db954',
    },
  ];

  function createPlaceholder(name, color, originalSrc, width, height) {
    const ph = document.createElement('div');
    ph.dataset.adblockBlocked = '1';
    ph.dataset.originalSrc = originalSrc || '';
    Object.assign(ph.style, {
      display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
      flexDirection: 'column', gap: '8px',
      width: width || '300px', height: height || '100px',
      background: '#1e2130', border: `2px solid ${color}`,
      borderRadius: '8px', cursor: 'pointer', userSelect: 'none',
      fontFamily: 'sans-serif', color: '#e8eaf0',
      boxSizing: 'border-box',
    });
    ph.innerHTML = `
      <span style="font-size:12px;font-weight:600;color:${color};">${name} Widget</span>
      <span style="font-size:10px;color:#8b91a8;text-align:center;padding:0 8px;">
        Blocked by AdBlocker Pro<br>Click to load
      </span>
      <button style="padding:4px 12px;border-radius:6px;border:1px solid ${color};
                     background:transparent;color:${color};font-size:11px;cursor:pointer;">
        Allow Once
      </button>`;

    ph.querySelector('button').addEventListener('click', (e) => {
      e.stopPropagation();
      if (originalSrc) {
        const iframe = document.createElement('iframe');
        iframe.src = originalSrc;
        iframe.width = width || '300';
        iframe.height = height || '200';
        iframe.frameBorder = '0';
        iframe.allowFullscreen = true;
        ph.replaceWith(iframe);
      } else {
        ph.remove();
      }
    });
    return ph;
  }

  function replaceWidgets() {
    WIDGETS.forEach(({ name, selector, color }) => {
      document.querySelectorAll(selector).forEach(el => {
        if (el.dataset.adblockBlocked) return;
        const rect = el.getBoundingClientRect();
        const ph = createPlaceholder(
          name, color, el.src || el.href,
          `${Math.max(rect.width || 300, 120)}px`,
          `${Math.max(rect.height || 100, 60)}px`,
        );
        el.replaceWith(ph);
      });
    });
  }

  // Run on DOM ready and observe for dynamic widgets
  if (document.readyState !== 'loading') replaceWidgets();
  else document.addEventListener('DOMContentLoaded', replaceWidgets);

  new MutationObserver(replaceWidgets)
    .observe(document.documentElement, { childList: true, subtree: true });
})();
