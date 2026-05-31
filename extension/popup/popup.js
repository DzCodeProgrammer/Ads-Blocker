'use strict';

// ── DOM helpers ──────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);
const setText = (id, val) => { const el = $(id); if (el) el.textContent = val ?? '—'; };

// ── Tab navigation ───────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach((c) => c.classList.remove('active'));
    btn.classList.add('active');
    $(`tab-${btn.dataset.tab}`).classList.add('active');
  });
});

// ── Dark mode ────────────────────────────────────────────────────────────────
const DARK_KEY = 'adblock_dark';
const initDark = () => {
  const dark = localStorage.getItem(DARK_KEY) === '1';
  document.body.classList.toggle('dark', dark);
  $('darkModeBtn').textContent = dark ? '☀️' : '🌙';
};
$('darkModeBtn').addEventListener('click', () => {
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem(DARK_KEY, isDark ? '1' : '0');
  $('darkModeBtn').textContent = isDark ? '☀️' : '🌙';
  sendToBackground('SET_SETTINGS', { dark_mode: isDark });
});
initDark();

// ── Backend status check ─────────────────────────────────────────────────────
const BACKEND = 'http://127.0.0.1:8765';

async function checkBackend() {
  try {
    const res = await fetch(`${BACKEND}/health`);
    $('footerStatus').textContent = res.ok ? '✓ Backend connected' : '✗ Backend error';
  } catch (_) {
    $('footerStatus').textContent = '✗ Backend offline — start run.py';
    $('footerStatus').style.color = 'var(--danger)';
  }
}

// ── Message to service worker ────────────────────────────────────────────────
function sendToBackground(type, payload = null) {
  return new Promise((resolve) => {
    const msg = { type };
    if (payload !== null) msg.payload = payload;
    chrome.runtime.sendMessage(msg, resolve);
  });
}

// ── Main toggle ──────────────────────────────────────────────────────────────
$('mainToggle').addEventListener('change', async (e) => {
  const enabled = e.target.checked;
  await sendToBackground('SET_SETTINGS', { is_enabled: enabled });
  updateStatusBanner(enabled);
});

function updateStatusBanner(enabled) {
  const banner = $('statusBanner');
  $('statusText').textContent = enabled ? 'Protection Active' : 'Protection Disabled';
  banner.className = `status-banner ${enabled ? 'active' : 'inactive'}`;
}

// ── Load stats ───────────────────────────────────────────────────────────────
async function loadStats() {
  const data = await sendToBackground('GET_STATS');
  if (!data) return;
  setText('totalBlocked', (data.total_blocked ?? 0).toLocaleString());
  setText('blockedToday', (data.blocked_today ?? 0).toLocaleString());
  setText('trackerBlocked', (data.tracker_blocked ?? 0).toLocaleString());
  setText('rulesCount', (data.rules_count ?? 0).toLocaleString());
}

// ── Top domains list ─────────────────────────────────────────────────────────
async function loadTopDomains() {
  try {
    const res = await fetch(`${BACKEND}/api/stats/top-domains?limit=5`);
    const domains = res.ok ? await res.json() : [];
    const list = $('topDomainsList');
    list.innerHTML = '';
    if (!domains.length) {
      list.innerHTML = '<li class="placeholder">No data yet</li>';
      return;
    }
    domains.forEach(({ domain, count }) => {
      const li = document.createElement('li');
      li.innerHTML = `<span>${escHtml(domain)}</span><span class="domain-count">${count}</span>`;
      list.appendChild(li);
    });
  } catch (_) {}
}

// ── Daily chart (canvas bar chart) ───────────────────────────────────────────
async function loadDailyChart() {
  try {
    const res = await fetch(`${BACKEND}/api/stats/daily?days=7`);
    const data = res.ok ? await res.json() : [];
    drawBarChart($('dailyChart'), data);
  } catch (_) {}
}

function drawBarChart(canvas, data) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const isDark = document.body.classList.contains('dark');
  const accentColor = '#3b5bdb';
  const textColor = isDark ? '#8b91a8' : '#6b7280';
  const bgColor = isDark ? '#252840' : '#f0f1f3';

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, W, H);

  if (!data.length) {
    ctx.fillStyle = textColor;
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('No data yet', W / 2, H / 2);
    return;
  }

  const maxVal = Math.max(...data.map((d) => d.count), 1);
  const pad = { l: 10, r: 10, t: 10, b: 24 };
  const barW = (W - pad.l - pad.r) / data.length;
  const chartH = H - pad.t - pad.b;

  data.forEach(({ date, count }, i) => {
    const barH = (count / maxVal) * chartH;
    const x = pad.l + i * barW;
    const y = pad.t + chartH - barH;

    ctx.fillStyle = accentColor + 'cc';
    ctx.beginPath();
    ctx.roundRect(x + 2, y, barW - 4, barH, [4, 4, 0, 0]);
    ctx.fill();

    ctx.fillStyle = textColor;
    ctx.font = '9px sans-serif';
    ctx.textAlign = 'center';
    const label = date.slice(5); // MM-DD
    ctx.fillText(label, x + barW / 2, H - 6);
  });
}

// ── Settings sync ────────────────────────────────────────────────────────────
async function loadSettings() {
  const s = await sendToBackground('GET_SETTINGS');
  if (!s) return;
  $('mainToggle').checked = s.is_enabled ?? true;
  updateStatusBanner(s.is_enabled ?? true);
  $('blockAds').checked = s.block_ads ?? true;
  $('blockTrackers').checked = s.block_trackers ?? true;
  $('enableMl').checked = s.enable_ml ?? true;
}

['blockAds', 'blockTrackers', 'enableMl'].forEach((id) => {
  $(id).addEventListener('change', (e) => {
    const key = id.replace(/([A-Z])/g, '_$1').toLowerCase();
    sendToBackground('SET_SETTINGS', { [key]: e.target.checked });
  });
});

// ── Whitelist ────────────────────────────────────────────────────────────────
async function loadWhitelist() {
  const items = await sendToBackground('GET_WHITELIST');
  const list = $('whitelistList');
  list.innerHTML = '';
  if (!items || !items.length) {
    list.innerHTML = '<li class="placeholder">No whitelisted domains</li>';
    return;
  }
  items.forEach(({ id, domain }) => {
    const li = document.createElement('li');
    li.innerHTML = `<span>${escHtml(domain)}</span>
      <button class="remove-btn" data-id="${id}" title="Remove">✕</button>`;
    list.appendChild(li);
  });
  list.querySelectorAll('.remove-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      await sendToBackground('REMOVE_WHITELIST', { id: parseInt(btn.dataset.id) });
      loadWhitelist();
    });
  });
}

$('addWhitelistBtn').addEventListener('click', async () => {
  const domain = $('whitelistInput').value.trim();
  if (!domain) return;
  const res = await sendToBackground('ADD_WHITELIST', { domain });
  if (res && !res.error) {
    $('whitelistInput').value = '';
    loadWhitelist();
  } else {
    alert(res?.error ?? 'Invalid domain');
  }
});

// ── Update filters ────────────────────────────────────────────────────────────
$('updateFiltersBtn').addEventListener('click', async () => {
  $('updateStatus').textContent = 'Updating…';
  const res = await sendToBackground('TRIGGER_UPDATE');
  $('updateStatus').textContent = res?.total_rules
    ? `✓ ${res.total_rules} rules loaded`
    : '✗ Update failed — is backend running?';
  loadStats();
});

// ── Sanitize output ───────────────────────────────────────────────────────────
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Bootstrap ─────────────────────────────────────────────────────────────────
(async () => {
  await Promise.all([checkBackend(), loadSettings(), loadStats(), loadTopDomains(), loadDailyChart(), loadWhitelist()]);
})();
