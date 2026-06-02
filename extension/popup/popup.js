'use strict';

const BACKEND = 'http://127.0.0.1:8765';
const $ = id => document.getElementById(id);
const setText = (id, v) => { const el = $(id); if (el) el.textContent = v ?? '—'; };
const escHtml = s => String(s).replace(/[&<>"']/g, c =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// ── Tab navigation ───────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn =>
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    $(`tab-${btn.dataset.tab}`).classList.add('active');
    if (btn.dataset.tab === 'netlog') loadNetLog();
    if (btn.dataset.tab === 'lists') loadFilterLists();
    if (btn.dataset.tab === 'options') loadBreakdown();
  })
);

// ── Dark mode ────────────────────────────────────────────────────────────────
const DARK_KEY = 'adblock_dark';
const applyDark = () => {
  const dark = localStorage.getItem(DARK_KEY) === '1';
  document.body.classList.toggle('dark', dark);
  $('darkModeBtn').textContent = dark ? '☀️' : '🌙';
};
$('darkModeBtn').addEventListener('click', () => {
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem(DARK_KEY, isDark ? '1' : '0');
  $('darkModeBtn').textContent = isDark ? '☀️' : '🌙';
  sendBg('SET_SETTINGS', { dark_mode: isDark });
});
applyDark();

// ── Current tab info ──────────────────────────────────────────────────────────
let currentDomain = '';
async function loadCurrentTab() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab?.url) {
      const url = new URL(tab.url);
      currentDomain = url.hostname.replace(/^www\./, '');
      const siteEl = $('siteDomain');
      if (siteEl) siteEl.textContent = currentDomain;
      $('currentSite').textContent = currentDomain;
      await loadSiteMode(currentDomain);
    }
  } catch (_) {}
}

// ── Backend health ────────────────────────────────────────────────────────────
async function checkBackend() {
  try {
    const r = await fetch(`${BACKEND}/health`);
    if (r.ok) {
      $('footerStatus').textContent = '✓ Backend online';
    } else {
      $('footerStatus').textContent = '⚠ Backend error';
      $('footerStatus').style.color = 'var(--warn)';
    }
  } catch (_) {
    $('footerStatus').textContent = '✗ Start python run.py';
    $('footerStatus').style.color = 'var(--danger)';
  }
}

// ── Message to background ─────────────────────────────────────────────────────
function sendBg(type, payload = null) {
  return new Promise(resolve => {
    const msg = { type };
    if (payload !== null) msg.payload = payload;
    chrome.runtime.sendMessage(msg, r => resolve(r));
  });
}

// ── Main toggle ───────────────────────────────────────────────────────────────
$('mainToggle').addEventListener('change', async e => {
  await sendBg('SET_SETTINGS', { is_enabled: e.target.checked });
  updateStatusBanner(e.target.checked);
});

function updateStatusBanner(enabled) {
  const b = $('statusBanner');
  $('statusText').textContent = enabled ? 'Protection Active' : 'Protection Disabled';
  b.className = `status-banner ${enabled ? 'active' : 'inactive'}`;
}

// ── Stats ─────────────────────────────────────────────────────────────────────
async function loadStats() {
  try {
    const r = await fetch(`${BACKEND}/api/stats/summary`);
    if (!r.ok) return;
    const d = await r.json();
    setText('totalBlocked', (d.total_blocked ?? 0).toLocaleString());
    setText('blockedToday', (d.blocked_today ?? 0).toLocaleString());
    setText('trackerBlocked', (d.tracker_blocked ?? 0).toLocaleString());
    setText('rulesCount', (d.rules_count ?? 0).toLocaleString());
  } catch (_) {}
}

async function loadTopDomains() {
  try {
    const r = await fetch(`${BACKEND}/api/stats/top-domains?limit=5`);
    const data = r.ok ? await r.json() : [];
    const list = $('topDomainsList');
    list.innerHTML = data.length
      ? data.map(({ domain, count }) =>
          `<li><span>${escHtml(domain)}</span><span class="domain-count">${count}</span></li>`
        ).join('')
      : '<li class="placeholder">No data yet</li>';
  } catch (_) {}
}

async function loadDailyChart() {
  try {
    const r = await fetch(`${BACKEND}/api/stats/daily?days=7`);
    const data = r.ok ? await r.json() : [];
    drawChart($('dailyChart'), data);
  } catch (_) {}
}

function drawChart(canvas, data) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const dark = document.body.classList.contains('dark');
  const ac = '#3b5bdb', tc = dark ? '#8b91a8' : '#6b7280', bg = dark ? '#21253a' : '#f0f1f3';
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
  if (!data.length) {
    ctx.fillStyle = tc; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('No data', W / 2, H / 2); return;
  }
  const max = Math.max(...data.map(d => d.count), 1);
  const pad = { l: 8, r: 8, t: 8, b: 20 };
  const bw = (W - pad.l - pad.r) / data.length, ch = H - pad.t - pad.b;
  data.forEach(({ date, count }, i) => {
    const bh = (count / max) * ch, x = pad.l + i * bw, y = pad.t + ch - bh;
    ctx.fillStyle = ac + 'bb';
    ctx.beginPath(); ctx.roundRect(x + 2, y, bw - 4, bh, [3, 3, 0, 0]); ctx.fill();
    ctx.fillStyle = tc; ctx.font = '8px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText(date.slice(5), x + bw / 2, H - 5);
  });
}

// ── Per-site mode ──────────────────────────────────────────────────────────────
async function loadSiteMode(domain) {
  if (!domain) return;
  try {
    const r = await fetch(`${BACKEND}/api/site-settings/${encodeURIComponent(domain)}`);
    const data = r.ok ? await r.json() : { mode: 'normal' };
    setActiveModeBtn(data.mode);
  } catch (_) { setActiveModeBtn('normal'); }
}

function setActiveModeBtn(mode) {
  document.querySelectorAll('.mode-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.mode === mode);
  });
  const badge = $('siteMode');
  badge.textContent = { normal: 'Normal', aggressive: '🔥 Aggressive', disabled: 'Off' }[mode] || mode;
  badge.className = `site-mode-badge ${mode}`;
}

document.querySelectorAll('.mode-btn').forEach(btn =>
  btn.addEventListener('click', async () => {
    const mode = btn.dataset.mode;
    if (!currentDomain) return;
    setActiveModeBtn(mode);
    try {
      await fetch(`${BACKEND}/api/site-settings/${encodeURIComponent(currentDomain)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode }),
      });
    } catch (_) {}
  })
);

// ── Element Picker ─────────────────────────────────────────────────────────────
$('pickerBtn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab?.id) {
    chrome.tabs.sendMessage(tab.id, { type: 'ACTIVATE_PICKER' });
    window.close();
  }
});

// ── Network Log ────────────────────────────────────────────────────────────────
let logFilter = 'all';
let logData = [];

document.querySelectorAll('.chip').forEach(c =>
  c.addEventListener('click', () => {
    document.querySelectorAll('.chip').forEach(x => x.classList.remove('active'));
    c.classList.add('active');
    logFilter = c.dataset.filter;
    renderLog();
  })
);

$('clearLogBtn').addEventListener('click', async () => {
  await fetch(`${BACKEND}/api/logs`, { method: 'DELETE' });
  logData = [];
  renderLog();
});

async function loadNetLog() {
  try {
    const r = await fetch(`${BACKEND}/api/logs?limit=200`);
    logData = r.ok ? await r.json() : [];
    renderLog();
  } catch (_) {}
}

function renderLog() {
  const container = $('netlogList');
  const filtered = logData.filter(e => {
    if (logFilter === 'all') return true;
    if (logFilter === 'blocked') return e.status === 'blocked';
    if (logFilter === 'allowed') return e.status === 'allowed';
    if (logFilter === 'tracker') return e.is_tracker;
    if (logFilter === 'cname') return e.is_cname_cloaked;
    return true;
  });
  if (!filtered.length) {
    container.innerHTML = '<div class="placeholder">No entries</div>'; return;
  }
  container.innerHTML = filtered.slice(0, 150).map(e => `
    <div class="log-entry" title="${escHtml(e.url)}">
      <span class="log-status ${e.status}">${e.status.slice(0, 2).toUpperCase()}</span>
      <span class="log-domain">${escHtml(e.domain)}${e.is_tracker ? ' <span class="log-tracker-badge">T</span>' : ''}${e.is_cname_cloaked ? ' <span class="log-tracker-badge">C</span>' : ''}</span>
      <span class="log-type">${e.content_type}</span>
    </div>`).join('');
}

// ── Whitelist ─────────────────────────────────────────────────────────────────
async function loadWhitelist() {
  const r = await sendBg('GET_WHITELIST');
  const list = $('whitelistList');
  if (!r || !r.length) {
    list.innerHTML = '<li class="placeholder">No whitelisted domains</li>'; return;
  }
  list.innerHTML = r.map(({ id, domain }) =>
    `<li><span>${escHtml(domain)}</span>
     <button class="remove-btn" data-id="${id}">✕</button></li>`
  ).join('');
  list.querySelectorAll('.remove-btn').forEach(btn =>
    btn.addEventListener('click', async () => {
      await sendBg('REMOVE_WHITELIST', { id: +btn.dataset.id });
      loadWhitelist();
    })
  );
}

$('addWhitelistBtn').addEventListener('click', async () => {
  const domain = $('whitelistInput').value.trim();
  if (!domain) return;
  const r = await sendBg('ADD_WHITELIST', { domain });
  if (!r?.error) { $('whitelistInput').value = ''; loadWhitelist(); }
  else alert(r.error);
});

// ── Custom Filters Editor ──────────────────────────────────────────────────────
async function loadCustomFilters() {
  try {
    const r = await fetch(`${BACKEND}/api/export/rules`);
    if (r.ok) {
      const text = await r.text();
      $('customFiltersEditor').value = text
        .split('\n').filter(l => !l.startsWith('!')).join('\n').trim();
    }
  } catch (_) {}
}

$('saveFiltersBtn').addEventListener('click', async () => {
  const text = $('customFiltersEditor').value;
  try {
    const r = await fetch(`${BACKEND}/api/export/import`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, overwrite: true }),
    });
    const d = await r.json();
    $('filtersSaveStatus').textContent = `✓ ${d.count} rules saved`;
    setTimeout(() => $('filtersSaveStatus').textContent = '', 3000);
  } catch (_) { $('filtersSaveStatus').textContent = '✗ Save failed'; }
});

$('exportFiltersBtn').addEventListener('click', async () => {
  try {
    const r = await fetch(`${BACKEND}/api/export/rules`);
    const text = await r.text();
    const blob = new Blob([text], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'adblocker-custom-filters.txt';
    a.click();
  } catch (_) {}
});

$('importFiltersBtn').addEventListener('click', () => {
  const input = document.createElement('input');
  input.type = 'file'; input.accept = '.txt';
  input.onchange = async () => {
    const text = await input.files[0].text();
    $('customFiltersEditor').value = text;
  };
  input.click();
});

// ── Filter Lists ────────────────────────────────────────────────────────────
async function loadFilterLists() {
  try {
    const r = await fetch(`${BACKEND}/api/lists`);
    const lists = r.ok ? await r.json() : [];
    const ul = $('filterListsList');
    ul.innerHTML = lists.map(fl => `
      <li class="filter-list-item" data-id="${fl.id}">
        <div class="filter-list-info">
          <div class="filter-list-name">${escHtml(fl.name)}</div>
          <div class="filter-list-meta">
            <span class="filter-category ${fl.category}">${fl.category}</span>
            <span class="filter-list-count">${fl.rule_count ? fl.rule_count.toLocaleString() + ' rules' : 'Not fetched'}</span>
          </div>
        </div>
        <label class="toggle-switch" title="${fl.is_enabled ? 'Enabled' : 'Disabled'}">
          <input type="checkbox" class="list-toggle" data-id="${fl.id}" ${fl.is_enabled ? 'checked' : ''} />
          <span class="slider"></span>
        </label>
      </li>`).join('') || '<li class="placeholder">No lists</li>';

    ul.querySelectorAll('.list-toggle').forEach(cb =>
      cb.addEventListener('change', async () => {
        await fetch(`${BACKEND}/api/lists/${cb.dataset.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ is_enabled: cb.checked }),
        });
      })
    );
  } catch (_) {}
}

$('updateAllListsBtn').addEventListener('click', async () => {
  $('listsUpdateStatus').textContent = 'Updating all lists…';
  try {
    const r = await fetch(`${BACKEND}/api/filters/update`, { method: 'POST' });
    const d = await r.json();
    $('listsUpdateStatus').textContent = `✓ ${d.total_rules?.toLocaleString() ?? 0} rules loaded`;
    loadFilterLists();
    loadStats();
  } catch (_) { $('listsUpdateStatus').textContent = '✗ Update failed'; }
});

$('addListBtn').addEventListener('click', async () => {
  const url = $('listUrlInput').value.trim();
  if (!url) return;
  try {
    const r = await fetch(`${BACKEND}/api/lists`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: url.split('/').pop().replace('.txt', ''), url }),
    });
    const d = await r.json();
    if (d.id) { $('listUrlInput').value = ''; $('addListStatus').textContent = '✓ Subscribed'; loadFilterLists(); }
    else $('addListStatus').textContent = '✗ ' + (d.detail || 'Failed');
  } catch (_) { $('addListStatus').textContent = '✗ Error'; }
});

// ── Settings (options tab) ────────────────────────────────────────────────────
async function loadSettings() {
  const s = await sendBg('GET_SETTINGS');
  if (!s) return;
  $('mainToggle').checked = s.is_enabled ?? true;
  updateStatusBanner(s.is_enabled ?? true);
  const map = {
    blockAds: 'block_ads',
    blockTrackers: 'block_trackers',
    blockCookieBanners: 'block_cookie_banners',
    blockSocial: 'block_social',
    blockPopups: 'block_popups',
    blockNotifications: 'block_notifications',
    cleanUrls: 'clean_urls',
    enableCname: 'enable_cname',
    enableMl: 'enable_ml',
    antiFp: 'anti_fingerprint',
  };
  Object.entries(map).forEach(([elId, key]) => {
    const el = $(elId);
    if (el && s[key] !== undefined) el.checked = s[key];
  });
}

const SETTINGS_MAP = {
  blockAds: 'block_ads', blockTrackers: 'block_trackers',
  blockCookieBanners: 'block_cookie_banners', blockSocial: 'block_social',
  blockPopups: 'block_popups', blockNotifications: 'block_notifications',
  cleanUrls: 'clean_urls', enableCname: 'enable_cname',
  enableMl: 'enable_ml', antiFp: 'anti_fingerprint',
};

Object.keys(SETTINGS_MAP).forEach(id => {
  const el = $(id);
  if (el) el.addEventListener('change', e =>
    sendBg('SET_SETTINGS', { [SETTINGS_MAP[id]]: e.target.checked })
  );
});

// ── Breakdown ─────────────────────────────────────────────────────────────────
async function loadBreakdown() {
  try {
    const r = await fetch(`${BACKEND}/api/stats/breakdown`);
    const data = r.ok ? await r.json() : {};
    const total = Object.values(data).reduce((a, b) => a + b, 0) || 1;
    const container = $('rulesBreakdown');
    container.innerHTML = Object.entries(data)
      .sort(([, a], [, b]) => b - a)
      .map(([type, count]) => `
        <div class="breakdown-row">
          <span style="width:70px;font-size:10px;color:var(--text-muted)">${type}</span>
          <div class="breakdown-bar-wrap">
            <div class="breakdown-bar" style="width:${(count / total * 100).toFixed(1)}%"></div>
          </div>
          <span class="breakdown-count">${count.toLocaleString()}</span>
        </div>`).join('') || '<span style="color:var(--text-muted);font-size:11px">No rules loaded</span>';
  } catch (_) {}
}

// ── Bootstrap ─────────────────────────────────────────────────────────────────
(async () => {
  await Promise.all([
    checkBackend(),
    loadCurrentTab(),
    loadSettings(),
    loadStats(),
    loadTopDomains(),
    loadDailyChart(),
    loadWhitelist(),
    loadCustomFilters(),
  ]);
})();
