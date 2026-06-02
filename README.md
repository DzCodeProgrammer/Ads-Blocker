<div align="center">

<br>

<img src="extension/assets/icons/icon128.png" width="110" alt="AdBlocker Pro"/>

<h1>⚡ AdBlocker Pro</h1>

<p><strong>Browser Extension kelas profesional yang ditenagai Python, Machine Learning, dan FastAPI</strong></p>

<p><em>Blokir iklan, tracker, cookie banner, popup, dan fingerprinting — sekaligus dalam satu ekstensi</em></p>

<br>

<!-- Badges Row 1 -->
<p>
  <img src="https://img.shields.io/badge/Version-2.1.0-3b5bdb?style=for-the-badge&logo=github" alt="version"/>
  <img src="https://img.shields.io/badge/License-MIT-38a169?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="license"/>
  <img src="https://img.shields.io/badge/Manifest-V3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="mv3"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="status"/>
</p>

<!-- Badges Row 2 -->
<p>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="fastapi"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="sqlite"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="sklearn"/>
</p>

<!-- Browser Support -->
<p>
  <img src="https://img.shields.io/badge/Chrome-88%2B-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="chrome"/>
  <img src="https://img.shields.io/badge/Edge-88%2B-0078D7?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="edge"/>
  <img src="https://img.shields.io/badge/Firefox-109%2B-FF7139?style=for-the-badge&logo=firefox&logoColor=white" alt="firefox"/>
</p>

<br>

---

</div>

## 📋 Daftar Isi

<table>
<tr>
<td>

- [🌟 Tentang Proyek](#-tentang-proyek)
- [⚙️ Teknologi](#️-teknologi)
- [✨ Fitur Utama](#-fitur-utama)
- [🏗️ Arsitektur](#️-arsitektur)
- [📁 Struktur Proyek](#-struktur-proyek)

</td>
<td>

- [🚀 Quick Start](#-quick-start)
- [🔧 Instalasi Lengkap](#-instalasi-lengkap)
- [🌐 Load Extension](#-load-extension-di-browser)
- [📡 API Reference](#-api-reference)
- [🤖 ML Engine](#-ml-engine)

</td>
<td>

- [📋 Filter Lists](#-filter-lists)
- [⚙️ Konfigurasi](#️-konfigurasi)
- [🧪 Testing](#-testing)
- [🔒 Keamanan](#-keamanan)
- [📜 Changelog](#-changelog)
- [📄 Lisensi](#-lisensi)

</td>
</tr>
</table>

---

## 🌟 Tentang Proyek

**AdBlocker Pro** bukan sekadar ad blocker biasa. Ini adalah sistem lengkap berbasis **Python sebagai otak utama** dan browser extension sebagai antarmuka. Tidak seperti ad blocker konvensional yang hanya menggunakan JavaScript, proyek ini memiliki backend **FastAPI** yang mengelola kecerdasan pemblokiran secara terpusat.

```
                    🧠 Python Brain
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
🔍 Filter Engine    🤖 ML Engine        📊 Analytics
300k+ rules         RandomForest        Real-time stats
CNAME Detection     Fingerprint Det.    Network Logger
URL Cleaner         Behavioral AI       Dashboard
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
              🌐 Browser Extension (MV3)
              declarativeNetRequest Blocking
```

> **Filosofi:** Python menentukan *apa* yang diblokir. Browser menjalankan *bagaimana* memblokir. Pengguna melihat *hasilnya*.

---

## ⚙️ Teknologi

<div align="center">

### 🐍 Backend Stack

</div>

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python** | 3.11+ | Bahasa utama — seluruh logika bisnis |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) **FastAPI** | 0.111 | REST API backend — async, cepat, auto-docs |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite + SQLAlchemy** | 2.0 | Database lokal — WAL mode, zero-config |
| ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white) **Pydantic** | 2.7 | Validasi input + settings dari env |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-333?style=flat) **Uvicorn** | 0.29 | ASGI server dengan hot-reload |
| ![HTTPX](https://img.shields.io/badge/HTTPX-009688?style=flat) **HTTPX** | 0.27 | HTTP client async — fetch filter lists, DoH |
| ![APScheduler](https://img.shields.io/badge/APScheduler-blue?style=flat) **APScheduler** | 3.10 | Penjadwal update filter otomatis |
| ![slowapi](https://img.shields.io/badge/slowapi-red?style=flat) **slowapi** | 0.1 | Rate limiting — 120 req/menit |

<div align="center">

### 🤖 Machine Learning Stack

</div>

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white) **scikit-learn** | 1.4 | Random Forest classifier — deteksi URL iklan |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) **NumPy** | 1.26 | Operasi array untuk feature extraction |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) **Pandas** | 2.2 | Analisis data training + statistik |
| ![joblib](https://img.shields.io/badge/joblib-gray?style=flat) **joblib** | 1.4 | Serialisasi model ML — load cepat |
| ![tldextract](https://img.shields.io/badge/tldextract-green?style=flat) **tldextract** | 5.1 | Ekstraksi domain + eTLD+1 akurat |

<div align="center">

### 🌐 Browser Extension Stack

</div>

| Teknologi | Fungsi |
|-----------|--------|
| ![JS](https://img.shields.io/badge/JavaScript-ES2022-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript (ESM)** | Service worker, content scripts, popup |
| **Manifest V3** | Standard ekstensi terbaru Chrome/Edge/Firefox |
| **declarativeNetRequest** | Pemblokiran di level engine Chrome (tanpa blocking JS) |
| **webNavigation** | Intercept navigasi untuk URL cleaning + popup blocking |
| **webRequest** | Observasi request untuk logging dan badge counter |

<div align="center">

### 🛠️ Dev Tools

</div>

| Tool | Fungsi |
|------|--------|
| ![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) **pytest** | Unit + integration testing dengan in-memory SQLite |
| ![Pillow](https://img.shields.io/badge/Pillow-gray?style=flat) **Pillow** | Generate icon ekstensi secara programatik |
| ![Alembic](https://img.shields.io/badge/Alembic-6BA539?style=flat) **Alembic** | Migrasi database |
| **Anaconda** | Environment isolation — `environment.yml` disertakan |

---

## ✨ Fitur Utama

<div align="center">

### 🛡️ Pemblokiran Iklan & Tracker

</div>

<table>
<tr>
<td width="50%">

#### 🔵 URL Blocking Engine
- **300.000+ aturan** dari EasyList, EasyPrivacy, uBlock
- Parser penuh sintaks ABP/EasyList (`||domain^`, `@@`, `##`, `$options`)
- Pencocokan O(1) — hash set + eTLD+1 suffix trie
- Regex rules untuk pola kompleks
- Pembaruan otomatis setiap 24 jam (APScheduler)

</td>
<td width="50%">

#### 🔴 Tracker Protection
- **35+ domain tracker bawaan** selalu aktif
- Heuristik keyword: `analytics`, `pixel`, `beacon`, `tracking`, dll
- **CNAME Uncloaking** via DNS-over-HTTPS Cloudflare
- Deteksi tracker tersembunyi di balik subdomain first-party
- Behavioral Analyzer — deteksi tracker sync burst

</td>
</tr>
<tr>
<td>

#### 🟢 ML-Powered Detection
- Random Forest dengan **20 fitur URL** (entropy, digit ratio, keyword count, dll)
- Cross-validation 5-fold saat training
- Threshold confidence yang dapat dikonfigurasi (default: 75%)
- Training otomatis dengan data sintetis jika tidak ada dataset
- Model tersimpan sebagai `.joblib` untuk startup cepat

</td>
<td>

#### 🟡 Fingerprinting Protection
- Deteksi `fingerprintjs`, WebGL FP, Canvas FP scripts
- Noise injection pada Canvas `toDataURL()`
- Noise injection pada AudioContext `getChannelData()`
- Block WebRTC STUN (mencegah IP leak)
- Identifikasi domain fingerprinting via ML + rules

</td>
</tr>
</table>

---

<div align="center">

### 🍪 Cookie & Annoyances

</div>

<table>
<tr>
<td width="33%">

#### Cookie Banner Auto-Dismiss
Otomatis menolak/menutup dialog GDPR dari **40+ CMP**:

- ✅ Cookiebot
- ✅ OneTrust
- ✅ Quantcast
- ✅ TrustArc
- ✅ Usercentrics
- ✅ Didomi
- ✅ ConsentManager
- ✅ Cookie Information
- ✅ OneSignal
- ✅ Funding Choices
- ✅ SourcePoint
- ✅ Axeptio
- ✅ Klaro
- ✅ Dan 27+ lainnya

</td>
<td width="33%">

#### Social Widget Blocker
Ganti widget sosial dengan placeholder privacy-first:

- 🔵 Facebook Like & Share
- 🐦 Twitter/X Share Button
- 💼 LinkedIn Share
- 📸 Instagram Embed
- ▶️ YouTube Embed
- 🎵 TikTok Embed
- 🎧 Spotify Embed

> Klik "Allow Once" pada placeholder untuk memuat widget secara manual

</td>
<td width="33%">

#### Notification Blocker
Auto-deny push notification prompts:

- Override `Notification.requestPermission()`
- Selalu return `'denied'`
- Block custom prompt UI dari OneSignal, Pushwoosh, WisePops
- Sembunyikan overlay notifikasi
- Auto-klik tombol "No Thanks"

</td>
</tr>
</table>

---

<div align="center">

### 🎯 Fitur Canggih (setara uBlock Origin)

</div>

<table>
<tr>
<td width="50%">

#### 🎨 Element Picker
Blokir elemen apapun di halaman — persis seperti uBlock Origin!

1. Klik **Element Picker** di popup
2. Cursor berubah menjadi crosshair 🎯
3. Hover elemen → highlight biru muncul
4. Klik elemen → toolbar muncul di bawah
5. Edit CSS selector jika perlu
6. Preview — lihat berapa elemen yang akan disembunyikan
7. Klik **Add Filter** → aturan tersimpan permanen

```css
/* Contoh aturan yang dihasilkan: */
example.com##.ad-banner-wrapper
```

</td>
<td width="50%">

#### 📜 Scriptlet Engine
14 scriptlet bawaan untuk mengalahkan anti-adblock:

| Scriptlet | Tujuan |
|-----------|--------|
| `anti-adblock-killer` | Palsukan objek `window.adblock` |
| `abort-on-property-read` | Cegah baca properti window |
| `abort-on-property-write` | Cegah tulis properti window |
| `no-fetch-if` | Blokir `fetch()` ke URL tertentu |
| `no-xhr-if` | Blokir `XMLHttpRequest` |
| `no-webrtc` | Blokir WebRTC / IP leak |
| `no-setTimeout-if` | Blokir callback setTimeout |
| `set-constant` | Paksa nilai properti konstan |
| `youtube-ad-skip` | Skip iklan YouTube otomatis |
| `cookie-remover` | Hapus tracking cookies |
| `noeval` | Neutralkan `eval()` anti-adblock |
| `remove-class` | Hapus CSS class iklan |
| `no-notification-if` | Blokir notifikasi push |
| `no-setInterval-if` | Blokir interval callbacks |

</td>
</tr>
<tr>
<td>

#### 📍 Per-Site Mode
Kontrol pemblokiran per domain:

| Mode | Perilaku |
|------|----------|
| 🔴 **Off** | Nonaktifkan semua pemblokiran untuk site ini |
| 🔵 **Normal** | Blokir standar (iklan + tracker) |
| 🔥 **Aggressive** | Blokir semua script/XHR/frame dari 3rd party |

Dapat diatur dari popup → tab **Overview** atau via API.

</td>
<td>

#### 🌐 URL Tracker Cleaner
Strip **60+ parameter pelacak** dari URL navigasi:

```
SEBELUM:
https://shop.com/product?id=123
  &utm_source=facebook
  &utm_campaign=summer_sale
  &fbclid=IwAR3xxxx
  &gclid=CjwKCAiA...

SESUDAH:
https://shop.com/product?id=123
```

Parameter yang dibersihkan:
`utm_*` · `fbclid` · `gclid` · `msclkid` · `ttclid`  
`mc_cid` · `mkt_tok` · `yclid` · `igshid` · `epik`  
`trk` · `twclid` · `ScCid` · `li_fat_id` · dan 45+ lainnya

</td>
</tr>
</table>

---

<div align="center">

### 📊 Dashboard & Analytics

</div>

<table>
<tr>
<td width="25%" align="center">

**📈 Statistics**
- Total iklan diblokir
- Diblokir hari ini
- Total tracker diblokir
- Jumlah aturan aktif
- Breakdown per filter list

</td>
<td width="25%" align="center">

**🌍 Top Domains**
- Domain paling sering diblokir
- Counter per domain
- 5 domain teratas di popup
- Top 50 via API

</td>
<td width="25%" align="center">

**📅 Daily Chart**
- Grafik bar 7 hari terakhir
- Dirender via Canvas API
- Support dark mode
- Tanpa library eksternal

</td>
<td width="25%" align="center">

**🔌 Network Log**
- Log real-time semua request
- Filter: All/Blocked/Allowed/Tracker/CNAME
- Status badge per request
- Content-type label

</td>
</tr>
</table>

---

## 🏗️ Arsitektur

```
╔══════════════════════════════════════════════════════════════════════╗
║                 BROWSER (Chrome / Edge / Firefox)                  ║
║                                                                    ║
║  ┌─────────────────┐   ┌──────────────────────────────────────┐   ║
║  │  POPUP (5 Tab)  │   │     SERVICE WORKER (background.js)   │   ║
║  │                 │   │                                      │   ║
║  │ 📊 Overview     │   │  RequestHandler  ──► DNR Rules       │   ║
║  │ 🌐 Network Log  │◄─►│  NetworkLogger   ──► Backend Log     │   ║
║  │ 🔧 Filters      │   │  URLCleaner      ──► Strip UTM       │   ║
║  │ 📋 Lists        │   │  PopupBlocker    ──► webNavigation   │   ║
║  │ ⚙️  Options     │   │  PerSiteManager  ──► Mode Cache      │   ║
║  └─────────────────┘   └──────────────┬───────────────────────┘   ║
║                                       │ REST API calls             ║
║  ┌──────────────────────────────────┐  │ ┌─────────────────────┐   ║
║  │      CONTENT SCRIPTS             │  │ │  declarativeNet     │   ║
║  │                                  │  │ │  Request Engine     │   ║
║  │  content.js      (cosmetic CSS)  │  │ │  (Chrome DNR)       │   ║
║  │  cookie_banner   (auto-reject)   │  │ │                     │   ║
║  │  element_picker  (click-block)   │  │ │  ✓ 35+ built-in     │   ║
║  │  scriptlet_inj.  (main-world)    │  │ │  ✓ Custom domains   │   ║
║  │  social_blocker  (widget-block)  │  │ │  ✓ From backend     │   ║
║  │  youtube_skipper (ad-skip)       │  │ │  ✓ 0ms latency      │   ║
║  │  notification_bl (push-block)    │  │ └─────────────────────┘   ║
║  └──────────────────────────────────┘  │                           ║
╚═══════════════════════════════════════╪════════════════════════════╝
                                        │ HTTP/REST localhost:8765
╔═══════════════════════════════════════╪════════════════════════════╗
║              PYTHON BACKEND (FastAPI) │                            ║
║                                       ▼                            ║
║  ┌──────────────────────────────────────────────────────────────┐  ║
║  │                       API LAYER                              │  ║
║  │  /filters  /stats  /settings  /whitelist  /logs             │  ║
║  │  /site-settings  /lists  /export  /scriptlets               │  ║
║  │  Middleware: Rate Limit (120/min) · Security Headers · CORS │  ║
║  └──────────────────────┬───────────────────────────────────────┘  ║
║                         │                                          ║
║  ┌──────────────────────▼───────────────────────────────────────┐  ║
║  │                   SERVICE LAYER                              │  ║
║  │   BlockingService  │  StatsService  │  UpdateService         │  ║
║  │                    │               │  (APScheduler 24h)      │  ║
║  └──────────────────────┬───────────────────────────────────────┘  ║
║                         │                                          ║
║  ┌──────────────────────▼───────────────────────────────────────┐  ║
║  │                  FILTER ENGINE                               │  ║
║  │   EasyListParser  ·  UrlMatcher (O1 hash)                   │  ║
║  │   ContentTypeFilter  ·  CNAMEResolver (DoH Cloudflare)      │  ║
║  │   URLCleaner (60+ params)  ·  ScriptletEngine (14 scripts)  │  ║
║  └──────────────────────┬───────────────────────────────────────┘  ║
║                         │                                          ║
║  ┌──────────────────────▼───────────────────────────────────────┐  ║
║  │                   ML ENGINE                                  │  ║
║  │   AdClassifier (RandomForest, 20 URL features, CV F1 ~0.92) │  ║
║  │   FingerprintDetector  ·  BehavioralAnalyzer                │  ║
║  └──────────────────────┬───────────────────────────────────────┘  ║
║                         │                                          ║
║  ┌──────────────────────▼───────────────────────────────────────┐  ║
║  │              DATABASE (SQLite + WAL Mode)                    │  ║
║  │  FilterRule · BlockedRequest · NetworkLog                   │  ║
║  │  UserSettings · SiteSetting · FilterList                    │  ║
║  └──────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Alur Pemblokiran Request

```
🌐 Browser Request
       │
       ▼
┌──────────────────────┐
│ Chrome DNR Engine    │──── Rule Match? ──► YES ──► ❌ BLOCKED (0ms)
│ (native C++ engine)  │                           No JS overhead
└──────────────────────┘
       │ No rule match
       ▼
┌──────────────────────┐
│ webRequest.onBefore  │──── Tracker keyword? ──► YES ──► 🔴 Badge + Log
│ Request (observe)    │                                  + Add DNR rule
└──────────────────────┘
       │ Unknown domain
       ▼
┌──────────────────────┐    ┌─────────────────────────────────────┐
│  Backend async check │───►│  FilterEngine.check_url()           │
│  (non-blocking)      │    │  1. Whitelist check                 │
└──────────────────────┘    │  2. URL pattern match (O1)          │
       │                    │  3. CNAME uncloaking (DoH)          │
       │ Blocked?           │  4. ML prediction (RF classifier)   │
       ▼                    │  5. Fingerprint detection           │
  Add to DNR rules          └─────────────────────────────────────┘
  (blocks NEXT request)
```

---

## 📁 Struktur Proyek

```
📦 Ads-Blocker/
│
├── 🐍 backend/                          Python FastAPI Backend
│   ├── 🌐 api/
│   │   ├── main.py                      App factory + lifespan
│   │   ├── middleware/
│   │   │   ├── rate_limiter.py          120 req/menit (slowapi)
│   │   │   └── security.py              HTTP security headers
│   │   └── routes/
│   │       ├── filters.py               POST /check + CRUD rules
│   │       ├── stats.py                 Dashboard statistics
│   │       ├── settings.py              User preferences
│   │       ├── whitelist.py             Domain whitelist
│   │       ├── logs.py                  Network request log
│   │       ├── site_settings.py         Per-domain mode
│   │       ├── lists.py                 Filter list manager
│   │       ├── export.py                Import/export EasyList
│   │       └── scriptlets.py            JS scriptlet bundle server
│   │
│   ├── 🔍 filters/
│   │   ├── filter_engine.py             Core engine — semua subsystem
│   │   ├── easylist_parser.py           ABP/EasyList syntax parser
│   │   ├── url_matcher.py               O(1) domain + suffix matching
│   │   ├── updater.py                   Remote filter list downloader
│   │   ├── cname_resolver.py            DoH CNAME uncloaking
│   │   ├── url_cleaner.py               Strip 60+ tracking params
│   │   ├── content_filter.py            Per content-type policy
│   │   └── scriptlet_engine.py          14 built-in JS scriptlets
│   │
│   ├── 🗃️ models/
│   │   ├── filter_rule.py               ORM: aturan filter
│   │   ├── blocked_request.py           ORM: statistik blok
│   │   ├── settings.py                  ORM: pengaturan user
│   │   ├── network_log.py               ORM: log jaringan real-time
│   │   ├── site_setting.py              ORM: mode per-domain
│   │   └── filter_list.py               ORM: langganan filter list
│   │
│   ├── 🔧 services/
│   │   ├── blocking_service.py          Business logic facade
│   │   ├── stats_service.py             Agregasi dashboard
│   │   └── update_service.py            APScheduler auto-update
│   │
│   ├── 💾 database/
│   │   ├── db.py                        SQLAlchemy engine + WAL mode
│   │   └── repositories/
│   │       ├── filter_repo.py           FilterRule CRUD
│   │       ├── stats_repo.py            BlockedRequest queries
│   │       ├── log_repo.py              NetworkLog queries
│   │       └── site_repo.py             SiteSetting CRUD
│   │
│   └── config.py                        Pydantic Settings (env vars)
│
├── 🌐 extension/                        Browser Extension (MV3)
│   ├── manifest.json                    Extension manifest v2.1.0
│   ├── 🖼️ popup/
│   │   ├── popup.html                   UI 5 tab
│   │   ├── popup.js                     Logic stats/settings/lists
│   │   └── popup.css                    Tema light/dark
│   ├── ⚙️ background/
│   │   ├── background.js                Service worker orchestrator
│   │   ├── request_handler.js           DNR rules + observe
│   │   ├── network_logger.js            Batched async logger
│   │   ├── url_cleaner.js               Client-side UTM stripper
│   │   ├── popup_blocker.js             Popup window interceptor
│   │   └── per_site.js                  Mode cache per domain
│   ├── 📝 content_scripts/
│   │   ├── content.js                   Cosmetic CSS + anti-FP
│   │   ├── cookie_banner.js             GDPR auto-dismiss
│   │   ├── element_picker.js            Click-to-block (uBO style)
│   │   ├── scriptlet_injector.js        Main-world injection
│   │   ├── social_blocker.js            Widget replacement
│   │   ├── youtube_skipper.js           YouTube ad skip
│   │   └── notification_blocker.js      Push deny
│   └── 🎨 assets/icons/
│       ├── icon16.png  icon48.png  icon128.png
│       └── generate_icons.py            Pillow icon generator
│
├── 🤖 ml_engine/                        Machine Learning
│   ├── feature_extractor.py             20 URL feature extractor
│   ├── classifier.py                    RandomForest + cross-val
│   ├── trainer.py                       Training script
│   ├── predictor.py                     Production wrapper
│   ├── fingerprint_detector.py          FP URL detector
│   ├── behavioral_analyzer.py           Pattern analysis
│   └── data/
│       ├── training_data.csv            (auto-generated)
│       └── model.joblib                 (setelah training)
│
├── 🧪 tests/                            Test Suite (40+ tests)
│   ├── conftest.py                      Fixtures + in-memory SQLite
│   ├── test_api/test_routes.py          20+ API integration tests
│   ├── test_filters/test_engine.py      UrlMatcher + Parser tests
│   ├── test_ml/test_classifier.py       Feature + classifier tests
│   └── test_database/test_repos.py      Repository unit tests
│
├── 📚 docs/
│   ├── architecture.md
│   ├── installation.md
│   ├── deployment.md
│   └── api_reference.md
│
├── 🔧 environment.yml                   Anaconda env (Python 3.11)
├── 🔧 setup.py                          Python package
├── 🚀 run.py                            Backend entry point
├── 🪟 setup_and_test.bat               One-click setup (Windows)
├── 🔒 .env.example                      Template env vars
└── 📄 LICENSE                           MIT License
```

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/DzCodeProgrammer/Ads-Blocker.git
cd Ads-Blocker

# 2. Install Python dependencies
pip install fastapi "uvicorn[standard]" httpx sqlalchemy pydantic \
    pydantic-settings python-dotenv slowapi tldextract apscheduler \
    aiofiles scikit-learn numpy pandas joblib Pillow requests

# 3. Setup konfigurasi
cp .env.example .env

# 4. Generate icon ekstensi
python extension/assets/icons/generate_icons.py

# 5. Train model ML (opsional tapi direkomendasikan)
python -m ml_engine.trainer

# 6. Jalankan backend
python run.py
```

> 💡 **Windows:** Double-click **`setup_and_test.bat`** untuk menjalankan langkah 2–6 sekaligus.

Setelah backend jalan, buka browser:
- **API Docs:** http://127.0.0.1:8765/docs
- **Load Extension:** `chrome://extensions/` → Load unpacked → pilih folder `extension/`

---

## 🔧 Instalasi Lengkap

<details>
<summary><strong>🐍 Menggunakan Anaconda (Direkomendasikan)</strong></summary>

```bash
# Buat environment terisolasi
conda env create -f environment.yml

# Aktifkan
conda activate adblocker

# Verifikasi
python --version   # Python 3.11.x
```

</details>

<details>
<summary><strong>📦 Menggunakan pip</strong></summary>

```bash
# Install semua dependencies
pip install -e ".[dev]"

# Atau manual
pip install fastapi "uvicorn[standard]" httpx requests pandas numpy \
    scikit-learn APScheduler sqlalchemy alembic pydantic pydantic-settings \
    python-dotenv aiofiles slowapi tldextract joblib Pillow
```

</details>

<details>
<summary><strong>⚙️ Konfigurasi .env</strong></summary>

```env
# ── App ──────────────────────────────────────────
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8765
APP_SECRET_KEY=ganti-dengan-key-acak-yang-kuat

# ── Database ──────────────────────────────────────
DATABASE_URL=sqlite:///./adblocker.db

# ── Filter Lists ──────────────────────────────────
EASYLIST_URL=https://easylist.to/easylist/easylist.txt
EASYPRIVACY_URL=https://easylist.to/easylist/easyprivacy.txt
UBLOCK_URL=https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt
FILTER_UPDATE_INTERVAL=24

# ── Rate Limiting ─────────────────────────────────
RATE_LIMIT_PER_MINUTE=120

# ── ML Engine ─────────────────────────────────────
ML_CONFIDENCE_THRESHOLD=0.75

# ── CORS (isi dengan Extension ID Anda) ──────────
CORS_ORIGINS=chrome-extension://ID_EKSTENSI_ANDA
```

</details>

---

## 🌐 Load Extension di Browser

<details>
<summary><strong>🟦 Google Chrome / Microsoft Edge</strong></summary>

1. Buka `chrome://extensions/` atau `edge://extensions/`
2. Aktifkan **Developer mode** *(toggle kanan atas)*
3. Klik **Load unpacked**
4. Pilih folder `extension/` di dalam proyek
5. Catat **Extension ID** yang muncul
6. Tambahkan ke `.env`:
   ```
   CORS_ORIGINS=chrome-extension://EXTENSION_ID_ANDA
   ```
7. Restart backend: `python run.py`

</details>

<details>
<summary><strong>🟠 Mozilla Firefox</strong></summary>

1. Buka `about:debugging`
2. Klik **This Firefox**
3. Klik **Load Temporary Add-on**
4. Pilih file `extension/manifest.json`

> ⚠️ Add-on sementara dihapus saat browser di-restart.  
> Untuk install permanen: `pip install web-ext` lalu `web-ext sign`

</details>

---

## 📡 API Reference

Base URL: `http://127.0.0.1:8765` | Docs: `http://127.0.0.1:8765/docs`

<details>
<summary><strong>🔍 Filter & Blocking</strong></summary>

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/health` | Cek status backend |
| `POST` | `/api/filters/check` | Cek apakah URL harus diblokir |
| `GET` | `/api/filters` | List semua aturan aktif |
| `POST` | `/api/filters` | Tambah aturan kustom |
| `DELETE` | `/api/filters/{id}` | Nonaktifkan aturan |
| `POST` | `/api/filters/update` | Trigger update filter list remote |

```bash
# Contoh: Cek URL
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ads.doubleclick.net/pixel.gif"}'
# → {"blocked": true, "is_tracker": true, "domain": "ads.doubleclick.net"}
```

</details>

<details>
<summary><strong>📊 Statistics</strong></summary>

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/stats/summary` | Total blokir, hari ini, tracker, rules |
| `GET` | `/api/stats/top-domains` | Domain paling sering diblokir |
| `GET` | `/api/stats/daily` | Statistik per hari (N hari terakhir) |
| `GET` | `/api/stats/breakdown` | Jumlah aturan per filter list |

</details>

<details>
<summary><strong>⚙️ Settings & Whitelist</strong></summary>

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/settings` | Ambil pengaturan saat ini |
| `PUT` | `/api/settings` | Update pengaturan |
| `GET` | `/api/whitelist` | List domain di whitelist |
| `POST` | `/api/whitelist` | Tambah domain ke whitelist |
| `DELETE` | `/api/whitelist/{id}` | Hapus dari whitelist |

</details>

<details>
<summary><strong>🌐 Network Log & Site Settings</strong></summary>

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/logs` | Log request real-time (200 terakhir) |
| `POST` | `/api/logs/record` | Catat log entry |
| `DELETE` | `/api/logs` | Hapus semua log |
| `GET` | `/api/site-settings` | List pengaturan per-domain |
| `PUT` | `/api/site-settings/{domain}` | Set mode untuk domain |
| `DELETE` | `/api/site-settings/{domain}` | Reset domain ke default |

</details>

<details>
<summary><strong>📋 Filter Lists & Export</strong></summary>

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/lists` | List semua filter list |
| `POST` | `/api/lists` | Subscribe filter list baru |
| `PUT` | `/api/lists/{id}` | Enable/disable list |
| `DELETE` | `/api/lists/{id}` | Hapus list kustom |
| `POST` | `/api/lists/{id}/update` | Update satu list spesifik |
| `GET` | `/api/export/rules` | Export aturan kustom (EasyList format) |
| `POST` | `/api/export/import` | Import aturan dari teks EasyList |
| `GET` | `/api/scriptlets` | Daftar scriptlet tersedia |
| `POST` | `/api/scriptlets/bundle` | Bundle scriptlet untuk domain |

</details>

---

## 🤖 ML Engine

### Fitur URL yang Diekstrak (20 Fitur)

| # | Nama Fitur | Deskripsi |
|---|-----------|-----------|
| 1 | `url_length` | Panjang total URL |
| 2 | `domain_length` | Panjang nama domain |
| 3 | `path_length` | Panjang path URL |
| 4 | `query_length` | Panjang query string |
| 5 | `subdomain_depth` | Kedalaman subdomain |
| 6 | `path_depth` | Kedalaman path (jumlah `/`) |
| 7 | `query_param_count` | Jumlah parameter query |
| 8 | `digit_ratio_domain` | Rasio angka di domain |
| 9 | `digit_ratio_path` | Rasio angka di path |
| 10 | `url_entropy` | Shannon entropy URL |
| 11 | `domain_entropy` | Shannon entropy domain |
| 12 | `has_ip_address` | URL menggunakan IP langsung |
| 13 | `has_port` | URL mengandung port |
| 14 | `suspicious_tld` | TLD mencurigakan (.xyz, .click, dll) |
| 15 | `ad_keyword_count_domain` | Keyword iklan di domain |
| 16 | `ad_keyword_count_path` | Keyword iklan di path |
| 17 | `has_redirect_param` | Mengandung param redirect |
| 18 | `hyphen_count` | Jumlah tanda `-` di URL |
| 19 | `dot_count_subdomain` | Titik di subdomain |
| 20 | `long_subdomain` | Subdomain panjang (>30 char) |

### Training Model

```bash
# Dengan data sendiri (format CSV):
# kolom: url (str), label (0=aman, 1=iklan/tracker)
python -m ml_engine.trainer

# Model tersimpan di: ml_engine/data/model.joblib
# Cross-validation F1 score biasanya ~0.92
```

---

## 📋 Filter Lists

8 filter list bawaan, otomatis dimuat saat pertama kali update:

| # | Nama | Kategori | Estimasi Rules | Keterangan |
|---|------|----------|----------------|------------|
| 1 | **EasyList** | 🔴 Ads | ~70.000 | Filter iklan internasional utama |
| 2 | **EasyPrivacy** | 🔵 Privacy | ~30.000 | Hapus semua bentuk tracking |
| 3 | **uBlock Filters** | 🔴 Ads | ~25.000 | Filter eksklusif uBlock Origin |
| 4 | **uBlock Privacy** | 🔵 Privacy | ~5.000 | Filter privasi uBlock Origin |
| 5 | **Peter Lowe's List** | 🔴 Ads | ~3.000 | Server iklan & tracker |
| 6 | **Fanboy's Annoyance** | 🟡 Annoyances | ~30.000 | Social, popup, gangguan |
| 7 | **Cookie AutoDelete** | 🍪 Cookies | ~10.000 | Cookie consent banners |
| 8 | **NoCoin** | ⚠️ Malware | ~2.000 | Script cryptominer |

Subscribe list tambahan via popup → tab **Lists** atau API:

```bash
curl -X POST http://127.0.0.1:8765/api/lists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Indonesian List",
    "url": "https://example.com/id-filter.txt",
    "category": "ads"
  }'
```

---

## ⚙️ Konfigurasi

### Environment Variables

| Variable | Default | Keterangan |
|----------|---------|------------|
| `APP_ENV` | `development` | `development` atau `production` |
| `APP_PORT` | `8765` | Port backend |
| `APP_SECRET_KEY` | *(wajib ganti)* | Secret key untuk production |
| `FILTER_UPDATE_INTERVAL` | `24` | Jam antar auto-update filter |
| `RATE_LIMIT_PER_MINUTE` | `120` | Batas request per menit |
| `ML_CONFIDENCE_THRESHOLD` | `0.75` | Ambang batas ML (0.0–1.0) |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

### Mode Pemblokiran Per-Site

| Mode | Icon | Perilaku |
|------|------|----------|
| **Normal** | 🔵 | Blokir standar — domain iklan + tracker terkenal |
| **Aggressive** | 🔥 | Blokir semua script/XHR/frame dari 3rd party |
| **Disabled** | ⚫ | Nonaktifkan semua pemblokiran di site ini |

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov

# Jalankan semua test
pytest tests/ -v

# Dengan coverage report
pytest tests/ -v --cov=backend --cov=ml_engine --cov-report=html
open htmlcov/index.html  # atau buka di browser

# Test file spesifik
pytest tests/test_api/test_routes.py -v
pytest tests/test_filters/test_engine.py -v
pytest tests/test_ml/test_classifier.py -v
pytest tests/test_database/test_repos.py -v
```

### Test Manual via cURL

```bash
# Health check
curl http://127.0.0.1:8765/health

# Blokir URL iklan
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://ads.doubleclick.net/ad.js","enable_ml":true}'

# Lihat statistik
curl http://127.0.0.1:8765/api/stats/summary

# Tambah domain ke whitelist
curl -X POST http://127.0.0.1:8765/api/whitelist \
  -H "Content-Type: application/json" \
  -d '{"domain":"github.com"}'

# Get scriptlet bundle untuk YouTube
curl -X POST http://127.0.0.1:8765/api/scriptlets/bundle \
  -H "Content-Type: application/json" \
  -d '{"domain":"youtube.com","include_defaults":true}'
```

---

## 🔒 Keamanan

| Lapisan | Implementasi |
|---------|-------------|
| **Input Validation** | Semua input divalidasi via Pydantic — URL scheme, format domain, karakter pattern |
| **Rate Limiting** | 120 request/menit per IP via `slowapi` |
| **Security Headers** | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy` |
| **CORS** | Hanya origin ekstensi yang dikonfigurasi di `.env` |
| **SQLite WAL** | Write-Ahead Logging untuk concurrent reads tanpa lock |
| **Extension CSP** | `script-src 'self'` — tidak ada eval atau inline scripts |
| **DNR Blocking** | Pemblokiran via Chrome engine, bukan callback JavaScript |
| **No Telemetry** | Tidak ada data yang dikirim ke server eksternal |

---

## 📊 Perbandingan dengan Ad Blocker Lain

| Fitur | AdBlocker Pro | uBlock Origin | AdBlock Plus | Brave |
|-------|:---:|:---:|:---:|:---:|
| Python Backend | ✅ | ❌ | ❌ | ❌ |
| ML Detection | ✅ | ❌ | ❌ | ✅ |
| CNAME Uncloaking | ✅ | ✅ | ❌ | ✅ |
| Element Picker | ✅ | ✅ | ✅ | ❌ |
| Cookie Auto-Dismiss | ✅ | ✅ | ❌ | ✅ |
| Social Widget Block | ✅ | ✅ | ❌ | ✅ |
| YouTube Ad Skip | ✅ | ✅ | ❌ | ✅ |
| Scriptlet Injection | ✅ | ✅ | ❌ | ❌ |
| Network Log | ✅ | ✅ | ❌ | ❌ |
| Per-Site Mode | ✅ | ✅ | ✅ | ✅ |
| URL Tracker Cleaner | ✅ | ⚠️ | ❌ | ✅ |
| Dashboard Statistik | ✅ | ✅ | ✅ | ✅ |
| REST API | ✅ | ❌ | ❌ | ❌ |
| Import/Export Rules | ✅ | ✅ | ✅ | ❌ |
| Open Source | ✅ | ✅ | ✅ | ✅ |

---

## 📜 Changelog

<details>
<summary><strong>v2.1.0 — MV3 Compliance Fix</strong></summary>

- ✅ **Fix:** Ganti `webRequest ['blocking']` dengan `declarativeNetRequest` dynamic rules
- ✅ Chrome MV3 melarang `webRequestBlocking` untuk regular extensions
- ✅ 35 domain tracker bawaan selalu dimuat sebagai DNR rules
- ✅ Domain baru dari ML/backend otomatis ditambah ke DNR rules
- ✅ `webRequest` tetap digunakan untuk observasi + logging (non-blocking)

</details>

<details>
<summary><strong>v2.0.0 — Major Expansion</strong></summary>

- ✅ Element Picker (uBlock Origin-style)
- ✅ Cookie Banner Auto-Dismisser (40+ CMP)
- ✅ Social Widget Blocker (7 platform)
- ✅ YouTube Ad Skipper
- ✅ Notification Permission Blocker
- ✅ Scriptlet Engine (14 scriptlets)
- ✅ CNAME Uncloaking via DNS-over-HTTPS
- ✅ URL Tracking Parameter Cleaner (60+ params)
- ✅ Network Request Logger (real-time)
- ✅ Per-Site Mode (Off/Normal/Aggressive)
- ✅ Filter List Manager (8 built-in lists)
- ✅ Import/Export custom rules
- ✅ FingerprintDetector (ML)
- ✅ BehavioralAnalyzer (ML)
- ✅ Popup UI redesign (5 tabs)

</details>

<details>
<summary><strong>v1.0.0 — Initial Release</strong></summary>

- ✅ FastAPI backend + SQLite database
- ✅ EasyList parser + URL matcher
- ✅ ML classifier (Random Forest, 20 features)
- ✅ APScheduler auto-update filter lists
- ✅ Popup dashboard dengan statistik
- ✅ Dukungan Chrome, Edge, Firefox

</details>

---

## 🤝 Contributing

Kontribusi sangat disambut! Silakan:

1. **Fork** repository ini
2. **Buat branch** fitur baru: `git checkout -b feature/nama-fitur`
3. **Ikuti standar kode:**
   - Python: PEP8 + type hints + Black formatting
   - JavaScript: ESM modules + `'use strict'`
   - Arsitektur: Clean Architecture (routes → services → engine → repos)
4. **Tambahkan test** untuk fitur backend baru
5. **Jalankan test:** `pytest tests/ -v`
6. **Buat Pull Request** dengan deskripsi yang jelas

---

## 📄 Lisensi

```
MIT License — Copyright (c) 2026 DzCodeProgrammer

Izin diberikan secara gratis kepada siapa pun yang memperoleh salinan
perangkat lunak ini untuk digunakan, disalin, dimodifikasi, digabungkan,
diterbitkan, didistribusikan, disublisensikan, dan/atau dijual tanpa
batasan, dengan ketentuan pemberitahuan hak cipta ini disertakan dalam
semua salinan.
```

Lihat file [LICENSE](LICENSE) untuk teks lengkap.

---

<div align="center">

<br>

**Dibuat dengan ❤️ menggunakan Python, FastAPI, dan Machine Learning**

<br>

[![GitHub](https://img.shields.io/badge/GitHub-DzCodeProgrammer-181717?style=for-the-badge&logo=github)](https://github.com/DzCodeProgrammer/Ads-Blocker)
&nbsp;
[![Issues](https://img.shields.io/badge/Report-Issue-E53E3E?style=for-the-badge&logo=github)](https://github.com/DzCodeProgrammer/Ads-Blocker/issues)
&nbsp;
[![License](https://img.shields.io/badge/License-MIT-38a169?style=for-the-badge)](LICENSE)

<br>

*Jika proyek ini membantu, pertimbangkan untuk memberikan ⭐ di GitHub!*

<br>

</div>
