/**
 * Element Picker — uBlock Origin-style click-to-block.
 *
 * Activated by the popup (sends 'ACTIVATE_PICKER' message).
 * User hovers to highlight elements → clicks to select → toolbar shows
 * the CSS selector → clicks "Add Filter" to create a cosmetic rule.
 */

(function () {
  'use strict';

  if (window.__adBlockerPicker) return; // already injected
  window.__adBlockerPicker = true;

  // ── State ────────────────────────────────────────────────────────────────
  let active = false;
  let highlighted = null;
  let selectedEl = null;
  let toolbar = null;
  let overlay = null;

  // ── Utilities ─────────────────────────────────────────────────────────────
  function buildSelector(el) {
    if (!el || el === document.body) return 'body';
    const parts = [];
    let cur = el;
    while (cur && cur !== document.body && parts.length < 5) {
      let selector = cur.tagName.toLowerCase();
      if (cur.id) {
        selector = `#${CSS.escape(cur.id)}`;
        parts.unshift(selector);
        break; // ID is unique
      }
      if (cur.classList.length) {
        const classes = [...cur.classList]
          .filter(c => !/^(active|open|selected|current|js-)/.test(c))
          .slice(0, 3)
          .map(c => `.${CSS.escape(c)}`)
          .join('');
        if (classes) selector += classes;
      }
      parts.unshift(selector);
      cur = cur.parentElement;
    }
    return parts.join(' > ');
  }

  function countMatches(selector) {
    try {
      return document.querySelectorAll(selector).length;
    } catch (_) {
      return 0;
    }
  }

  function escHtml(s) {
    return String(s).replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
    );
  }

  // ── Overlay highlight ─────────────────────────────────────────────────────
  function showHighlight(el) {
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = '__adblock_overlay__';
      Object.assign(overlay.style, {
        position: 'fixed', zIndex: '2147483646', pointerEvents: 'none',
        background: 'rgba(59,91,219,.25)', border: '2px solid #3b5bdb',
        borderRadius: '3px', transition: 'all .1s', boxSizing: 'border-box',
      });
      document.documentElement.appendChild(overlay);
    }
    const r = el.getBoundingClientRect();
    Object.assign(overlay.style, {
      top: `${r.top}px`, left: `${r.left}px`,
      width: `${r.width}px`, height: `${r.height}px`,
      display: 'block',
    });
  }

  function hideHighlight() {
    if (overlay) overlay.style.display = 'none';
  }

  // ── Toolbar ───────────────────────────────────────────────────────────────
  function createToolbar(selector) {
    removeToolbar();
    toolbar = document.createElement('div');
    toolbar.id = '__adblock_picker_toolbar__';
    const matches = countMatches(selector);
    toolbar.innerHTML = `
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <span style="font-weight:600;color:#e8eaf0;">Element Picker</span>
        <input id="__abp_sel_input__" value="${escHtml(selector)}"
          style="flex:1;min-width:200px;padding:5px 8px;border-radius:6px;
                 border:1px solid #3b5bdb;background:#252840;color:#e8eaf0;
                 font-family:monospace;font-size:12px;outline:none;" />
        <span style="color:#8b91a8;font-size:11px;">${matches} element${matches !== 1 ? 's' : ''}</span>
        <button id="__abp_wider__" title="Wider selector">↑</button>
        <button id="__abp_narrower__" title="Narrower selector">↓</button>
        <button id="__abp_preview__">Preview</button>
        <button id="__abp_add__" style="background:#3b5bdb;color:#fff;">Add Filter</button>
        <button id="__abp_cancel__">✕</button>
      </div>`;
    Object.assign(toolbar.style, {
      position: 'fixed', bottom: '0', left: '0', right: '0', zIndex: '2147483647',
      background: '#1e2130', borderTop: '2px solid #3b5bdb',
      padding: '10px 16px', fontFamily: 'sans-serif', fontSize: '13px',
      boxShadow: '0 -4px 20px rgba(0,0,0,.5)',
    });

    const btnStyle = {
      padding: '5px 10px', borderRadius: '6px', border: '1px solid #3b4270',
      background: '#252840', color: '#e8eaf0', cursor: 'pointer', fontSize: '12px',
    };
    toolbar.querySelectorAll('button').forEach(b => Object.assign(b.style, btnStyle));
    const addBtn = toolbar.querySelector('#__abp_add__');
    Object.assign(addBtn.style, { background: '#3b5bdb', border: 'none' });

    document.documentElement.appendChild(toolbar);

    // Wire events
    toolbar.querySelector('#__abp_cancel__').onclick = deactivate;
    toolbar.querySelector('#__abp_add__').onclick = () => addFilter(
      toolbar.querySelector('#__abp_sel_input__').value
    );
    toolbar.querySelector('#__abp_preview__').onclick = () => previewFilter(
      toolbar.querySelector('#__abp_sel_input__').value
    );
    toolbar.querySelector('#__abp_wider__').onclick = () => {
      if (selectedEl && selectedEl.parentElement) {
        selectedEl = selectedEl.parentElement;
        updateToolbarSelector(buildSelector(selectedEl));
      }
    };
    toolbar.querySelector('#__abp_narrower__').onclick = () => {
      const firstChild = selectedEl && selectedEl.firstElementChild;
      if (firstChild) { selectedEl = firstChild; updateToolbarSelector(buildSelector(selectedEl)); }
    };
  }

  function updateToolbarSelector(selector) {
    if (!toolbar) return;
    const input = toolbar.querySelector('#__abp_sel_input__');
    if (input) input.value = selector;
    const matches = countMatches(selector);
    const span = toolbar.querySelector('span:nth-child(3)');
    if (span) span.textContent = `${matches} element${matches !== 1 ? 's' : ''}`;
  }

  function removeToolbar() {
    if (toolbar) { toolbar.remove(); toolbar = null; }
  }

  function previewFilter(selector) {
    try {
      document.querySelectorAll(selector).forEach(el =>
        el.style.setProperty('outline', '3px dashed #e53e3e', 'important')
      );
      setTimeout(() => {
        document.querySelectorAll(selector).forEach(el => el.style.removeProperty('outline'));
      }, 2000);
    } catch (_) {}
  }

  async function addFilter(selector) {
    const rule = `${location.hostname}##${selector}`;
    try {
      await chrome.runtime.sendMessage({ type: 'ADD_COSMETIC_RULE', rule, selector });
      // Hide matched elements immediately
      document.querySelectorAll(selector).forEach(el =>
        el.style.setProperty('display', 'none', 'important')
      );
      showNotification(`Filter added: ${selector.slice(0, 60)}`);
    } catch (e) {
      showNotification('Failed to add filter', true);
    }
    deactivate();
  }

  function showNotification(msg, isError = false) {
    const n = document.createElement('div');
    n.textContent = msg;
    Object.assign(n.style, {
      position: 'fixed', top: '20px', right: '20px', zIndex: '2147483647',
      background: isError ? '#9b2c2c' : '#276749', color: '#fff',
      padding: '10px 16px', borderRadius: '8px', fontSize: '13px',
      fontFamily: 'sans-serif', boxShadow: '0 4px 12px rgba(0,0,0,.4)',
      transition: 'opacity .3s',
    });
    document.documentElement.appendChild(n);
    setTimeout(() => { n.style.opacity = '0'; setTimeout(() => n.remove(), 300); }, 2500);
  }

  // ── Picker activation/deactivation ───────────────────────────────────────
  function activate() {
    if (active) return;
    active = true;
    document.addEventListener('mouseover', onMouseover, true);
    document.addEventListener('mouseout', onMouseout, true);
    document.addEventListener('click', onClick, true);
    document.addEventListener('keydown', onKeydown, true);
    document.body.style.cursor = 'crosshair';
    showNotification('Element Picker active — click any element to block it');
  }

  function deactivate() {
    active = false;
    document.removeEventListener('mouseover', onMouseover, true);
    document.removeEventListener('mouseout', onMouseout, true);
    document.removeEventListener('click', onClick, true);
    document.removeEventListener('keydown', onKeydown, true);
    document.body.style.cursor = '';
    hideHighlight();
    removeToolbar();
    highlighted = null;
    selectedEl = null;
    if (overlay) { overlay.remove(); overlay = null; }
    chrome.runtime.sendMessage({ type: 'PICKER_CLOSED' });
  }

  // ── Event handlers ────────────────────────────────────────────────────────
  function onMouseover(e) {
    if (!active) return;
    const el = e.target;
    if (el === toolbar || toolbar?.contains(el)) return;
    highlighted = el;
    showHighlight(el);
  }

  function onMouseout(e) {
    if (!active) return;
    if (!e.relatedTarget || !toolbar?.contains(e.relatedTarget)) hideHighlight();
  }

  function onClick(e) {
    if (!active) return;
    if (toolbar?.contains(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    selectedEl = e.target;
    createToolbar(buildSelector(selectedEl));
  }

  function onKeydown(e) {
    if (e.key === 'Escape') deactivate();
  }

  // ── Message listener ──────────────────────────────────────────────────────
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === 'ACTIVATE_PICKER') activate();
    if (msg.type === 'DEACTIVATE_PICKER') deactivate();
  });
})();
