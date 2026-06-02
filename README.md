<div align="center">

<br>

<img src="extension/assets/icons/icon128.png" width="110" alt="AdBlocker Pro"/>

<h1>⚡ AdBlocker Pro</h1>

<p><strong>A production-grade browser extension powered by Python, Machine Learning, and FastAPI</strong></p>

<p><em>Eliminates advertisements, trackers, cookie consent dialogs, popups, and browser fingerprinting scripts<br>through a locally-hosted intelligent backend — no cloud dependency, no telemetry, full control.</em></p>

<br>

<p>
  <img src="https://img.shields.io/badge/Version-2.1.0-3b5bdb?style=for-the-badge&logo=github" alt="version"/>
  <img src="https://img.shields.io/badge/License-MIT-38a169?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="license"/>
  <img src="https://img.shields.io/badge/Manifest-V3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="mv3"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="status"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="fastapi"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="sqlite"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="sklearn"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Chrome-88%2B-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="chrome"/>
  <img src="https://img.shields.io/badge/Edge-88%2B-0078D7?style=for-the-badge&logo=microsoftedge&logoColor=white" alt="edge"/>
  <img src="https://img.shields.io/badge/Firefox-109%2B-FF7139?style=for-the-badge&logo=firefox&logoColor=white" alt="firefox"/>
</p>

<br>

---

</div>

## 📋 Table of Contents

<table>
<tr>
<td valign="top">

- [🌟 About](#-about)
- [⚙️ Technology Stack](#️-technology-stack)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)

</td>
<td valign="top">

- [🚀 Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [🌐 Loading the Extension](#-loading-the-extension)
- [📡 API Reference](#-api-reference)
- [🤖 Machine Learning Engine](#-machine-learning-engine)

</td>
<td valign="top">

- [📋 Filter Lists](#-filter-lists)
- [⚙️ Configuration](#️-configuration)
- [🧪 Testing](#-testing)
- [🔒 Security](#-security)
- [📊 Benchmarks](#-benchmarks)
- [📜 Changelog](#-changelog)
- [📄 License](#-license)

</td>
</tr>
</table>

---

## 🌟 About

**AdBlocker Pro** represents a fundamentally different approach to browser-based content filtering. While conventional ad blockers rely exclusively on JavaScript for all decision-making, this project delegates the cognitive burden — filter parsing, machine learning inference, statistical aggregation, and threat intelligence — to a locally-hosted **Python backend**. The browser extension's sole responsibility is to communicate those decisions to Chrome's native blocking engine.

```
                ┌─────────────────────────────────────────┐
                │         🧠  Python Intelligence Core     │
                │                                         │
                │  ┌───────────┐  ┌───────────────────┐  │
                │  │ FilterEng │  │    ML Engine       │  │
                │  │ 300k rules│  │ Random Forest      │  │
                │  │ CNAME DoH │  │ Fingerprint Det.   │  │
                │  │ URL Clean │  │ Behavioral AI      │  │
                │  └───────────┘  └───────────────────┘  │
                └──────────────────────┬──────────────────┘
                                       │ REST API
                ┌──────────────────────▼──────────────────┐
                │         🌐  Browser Extension (MV3)      │
                │                                         │
                │  declarativeNetRequest  →  0ms blocking  │
                │  Content Scripts        →  DOM surgery   │
                │  Popup UI (5 tabs)      →  Full control  │
                └─────────────────────────────────────────┘
```

**Design Philosophy:** Python determines *what* to block through sophisticated analysis. Chrome's declarative engine enforces the decisions at near-zero latency. The end user observes a faster, cleaner, and more private browsing experience without any perceptible overhead.

> This architecture eliminates the fundamental MV3 constraint: because blocking logic runs in the Python backend rather than a JavaScript service worker callback, we are not subject to the `webRequest` blocking restrictions that plagued the MV2 → MV3 migration.

---

## ⚙️ Technology Stack

<div align="center">

### 🐍 Backend

</div>

| Technology | Version | Role |
|-----------|---------|------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python** | 3.11+ | Primary language — all business logic, ML inference, filter parsing |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) **FastAPI** | 0.111 | Asynchronous REST API — OpenAPI auto-documentation, Pydantic validation |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite + SQLAlchemy** | 2.0 | Embedded relational database — WAL mode, zero configuration |
| ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white) **Pydantic** | 2.7 | Runtime type validation, settings management via environment variables |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-333333?style=flat) **Uvicorn** | 0.29 | ASGI server — production-ready with optional hot-reload |
| ![HTTPX](https://img.shields.io/badge/HTTPX-009688?style=flat) **HTTPX** | 0.27 | Async HTTP client — filter list fetching, DNS-over-HTTPS queries |
| ![APScheduler](https://img.shields.io/badge/APScheduler-2C6FAD?style=flat) **APScheduler** | 3.10 | Background task scheduler — automated 24-hour filter list updates |
| ![slowapi](https://img.shields.io/badge/slowapi-C0392B?style=flat) **slowapi** | 0.1 | Rate limiting middleware — configurable request throttling per IP |

<div align="center">

### 🤖 Machine Learning

</div>

| Technology | Version | Role |
|-----------|---------|------|
| ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white) **scikit-learn** | 1.4 | Random Forest classifier — probabilistic ad URL detection |
| ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) **NumPy** | 1.26 | Vectorized feature matrix operations |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) **Pandas** | 2.2 | Training data ingestion, exploratory analysis, statistics reporting |
| ![joblib](https://img.shields.io/badge/joblib-95A5A6?style=flat) **joblib** | 1.4 | Model serialization — millisecond cold-start loading |
| ![tldextract](https://img.shields.io/badge/tldextract-27AE60?style=flat) **tldextract** | 5.1 | Accurate eTLD+1 extraction using the Public Suffix List |

<div align="center">

### 🌐 Browser Extension

</div>

| Technology | Role |
|-----------|------|
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES2022-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript (ESM)** | Service worker orchestration, content script injection, popup UI |
| **Manifest V3** | Current Chrome/Edge/Firefox extension platform — service worker background |
| **declarativeNetRequest** | Native C++ blocking engine — zero-latency request cancellation |
| **webNavigation** | Navigation lifecycle hooks — URL cleaning, popup interception |
| **webRequest** | Non-blocking request observation — logging, badge counter, async ML checks |

<div align="center">

### 🛠️ Development & Tooling

</div>

| Tool | Role |
|------|------|
| ![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) **pytest + pytest-asyncio** | Test suite — 40+ unit and integration tests with in-memory SQLite |
| **pytest-cov** | Code coverage reporting — HTML and terminal output |
| **Pillow** | Programmatic PNG icon generation for the browser extension |
| **Alembic** | Database schema migration management |
| **Anaconda** | Reproducible Python environment via `environment.yml` |

---

## ✨ Features

<div align="center">

### 🛡️ Core Ad & Tracker Blocking

</div>

<table>
<tr>
<td width="50%">

#### 🔵 URL Blocking Engine
- Over **300,000 filter rules** from EasyList, EasyPrivacy, uBlock Origin
- Complete ABP/EasyList syntax support: `||domain^`, `@@exceptions`, `##cosmetic`, `$type,domain` options
- **O(1) domain lookup** using hash sets and eTLD+1 suffix trie
- Full regex rule support with graceful error handling for malformed patterns
- Automated 24-hour refresh via APScheduler — no manual intervention required
- Bulk import from any EasyList-format URL via `/api/lists`

</td>
<td width="50%">

#### 🔴 Tracker Intelligence
- **35+ high-confidence tracker domains** hardcoded as declarativeNetRequest rules at startup
- Keyword heuristics covering `analytics`, `pixel`, `beacon`, `tracking`, `telemetry`, and 15 others
- **CNAME Uncloaking** via Cloudflare DNS-over-HTTPS — resolves chains up to 5 hops deep
- Detects trackers concealed behind seemingly first-party subdomains (e.g., `stats.yoursite.com → eu.tracker.io`)
- Behavioral Analyzer for detecting tracker synchronization bursts and pixel chain patterns

</td>
</tr>
<tr>
<td>

#### 🟢 Machine Learning Detection
- Random Forest with **5-fold cross-validation**, typically achieving F1 ≥ 0.92
- 20 engineered URL features spanning lexical, domain, path, and keyword dimensions
- Configurable confidence threshold (default: 0.75) — tunable per deployment
- Synthetic training data generated automatically when no labeled dataset is provided
- Incremental learning: newly detected ad domains are immediately persisted to DNR rules

</td>
<td>

#### 🟡 Browser Fingerprinting Defense
- **Canvas API noise injection** — imperceptible pixel-level perturbation of `toDataURL()` output
- **AudioContext noise** — sub-threshold randomization of `getChannelData()` samples
- **WebRTC IP leak prevention** — neutralizes STUN-based IP harvesting via ICE candidate manipulation
- ML + rule-based detection of fingerprinting libraries: `fingerprintjs`, WebGL FP, Canvas FP services
- Identification of 12+ known fingerprinting domains including FingerprintJS.com and ThreatMetrix

</td>
</tr>
</table>

---

<div align="center">

### 🍪 Consent, Annoyances & Social Privacy

</div>

<table>
<tr>
<td width="33%">

#### Cookie Consent Auto-Rejection
Automatically dismisses GDPR/CCPA consent dialogs by interacting with their native APIs and DOM:

**Covered CMPs:**
- ✅ Cookiebot
- ✅ OneTrust
- ✅ Quantcast Choice
- ✅ TrustArc
- ✅ Usercentrics
- ✅ Didomi
- ✅ ConsentManager
- ✅ Cookie Information
- ✅ Funding Choices
- ✅ SourcePoint
- ✅ Axeptio / Klaro
- ✅ OneSignal, Pushwoosh
- ✅ GDPR Cookie Compliance (WP)
- ✅ 26+ additional via generic selectors

**Strategies employed:**
- CSS cosmetic hiding at `document_start`
- Automatic "Reject All" button detection via multilingual regex
- `localStorage` opt-out key injection
- Body scroll restoration after overlay removal

</td>
<td width="33%">

#### Social Widget Replacement
Substitutes privacy-invasive social embeds with interactive placeholders that load the original content only upon explicit user consent:

| Widget | Replacement |
|--------|------------|
| Facebook Like/Share | Blue placeholder |
| Twitter/X Buttons | Blue placeholder |
| LinkedIn Share | Blue placeholder |
| Instagram Embed | Gradient placeholder |
| YouTube Embed | Red placeholder |
| TikTok Embed | Dark placeholder |
| Spotify Player | Green placeholder |

Each placeholder displays the widget name, a privacy notice, and an **"Allow Once"** button that restores the original `<iframe>` on demand — eliminating cross-site tracking without permanently sacrificing functionality.

</td>
<td width="33%">

#### Push Notification Suppression

Silences the browser's Web Push permission prompt at the API level rather than relying on UI interaction:

```js
// Overridden at document_start
// before any page script executes

Notification.requestPermission()
// → always resolves to 'denied'

Notification.permission
// → always reads 'denied'
```

**Additionally:**
- Hides custom push prompt overlays (OneSignal slidedown, Pushwoosh dialog, WisePops)
- Auto-clicks "No Thanks" / "Decline" in overlay prompts
- Covers 10+ known push vendor selectors

</td>
</tr>
</table>

---

<div align="center">

### 🎯 Advanced Capabilities (uBlock Origin Parity)

</div>

<table>
<tr>
<td width="50%">

#### 🎨 Interactive Element Picker
A fully interactive DOM-level element blocker, providing feature parity with uBlock Origin's picker:

1. Click **"🎯 Element Picker"** in the popup
2. The cursor transforms into a crosshair
3. Hovering any element renders a real-time blue highlight overlay
4. Clicking an element opens the toolbar at the bottom of the viewport
5. The toolbar displays:
   - Auto-generated CSS selector (editable)
   - Live match count for the current selector
   - **↑ Wider** / **↓ Narrower** buttons to traverse the DOM hierarchy
   - **Preview** — outlines matching elements in red for 2 seconds
   - **Add Filter** — persists the rule and immediately hides matching elements
   - **✕ Cancel** — exits picker mode
6. Generated rules are saved to the backend and synchronized to the DNR engine

```css
/* Example of an auto-generated cosmetic rule */
news.example.com##div.ad-container > .sticky-banner
```

</td>
<td width="50%">

#### 📜 Scriptlet Injection Engine
Fourteen built-in JavaScript scriptlets are injected into the page's **main world** at `document_start`, before any page script executes — defeating anti-adblock detectors that rely on inspecting the extension's presence:

| Scriptlet | Mechanism |
|-----------|-----------|
| `anti-adblock-killer` | Returns a fake detector object for `window.adblock` and related properties |
| `abort-on-property-read` | Throws `ReferenceError` when a designated window property is read |
| `abort-on-property-write` | Throws `ReferenceError` when a designated window property is written |
| `no-fetch-if` | Intercepts `fetch()` calls matching a URL pattern and rejects the promise |
| `no-xhr-if` | Intercepts `XMLHttpRequest.open()` matching a URL pattern |
| `no-webrtc` | Removes STUN servers from `RTCPeerConnection` configuration |
| `no-setTimeout-if` | Suppresses `setTimeout` callbacks whose source matches a needle string |
| `no-setInterval-if` | Suppresses `setInterval` callbacks matching a needle string |
| `set-constant` | Forces a named window property to a permanent constant value |
| `remove-class` | Removes CSS classes injected by ad scripts via MutationObserver |
| `noeval` | Patches `window.eval` to silently discard anti-adblock evaluation strings |
| `cookie-remover` | Expires tracking cookies across all path and domain scopes |
| `no-notification-if` | Overrides `Notification.requestPermission` to always deny |
| `youtube-ad-skip` | Clicks skip buttons and fast-forwards instream ads on YouTube |

Scriptlets are served as domain-aware bundles by the backend (`POST /api/scriptlets/bundle`), allowing per-domain customization without shipping unnecessary code.

</td>
</tr>
<tr>
<td>

#### 📍 Per-Site Blocking Modes
Granular control over blocking intensity at the domain level, persisted in the backend database and cached in the service worker for latency-free enforcement:

| Mode | Behavior | Use Case |
|------|----------|----------|
| ⚫ **Disabled** | All blocking suspended for this origin | Developer tools, trusted intranet sites |
| 🔵 **Normal** | Standard ad/tracker blocking | General browsing |
| 🔥 **Aggressive** | All third-party `script`, `xmlhttprequest`, and `sub_frame` requests blocked | Maximum privacy mode, high-risk sites |

Modes are configurable from the popup Overview tab or directly via `PUT /api/site-settings/{domain}`.

</td>
<td>

#### 🌐 URL Tracking Parameter Cleaner
Strips over **60 known tracking query parameters** from navigation URLs before they are recorded in browser history, preventing passive cross-site tracking via referral attribution:

```
Before navigation:
https://shop.example.com/product?id=42
  &utm_source=newsletter
  &utm_medium=email
  &utm_campaign=black_friday_2026
  &fbclid=IwAR3xxxxxxxxxxxxxxxx
  &gclid=CjwKCAiAxxxxxxxxxxxxxx
  &msclkid=xxxxxxxxxxxxxxxxxx

After cleaning:
https://shop.example.com/product?id=42
```

**Covered parameter families:**
`utm_*` · `fbclid` · `gclid` · `dclid` · `_ga` · `_gl`
`msclkid` · `ttclid` · `twclid` · `yclid` · `ScCid`
`mc_cid` · `mc_eid` · `mkt_tok` · `igshid` · `epik`
`li_fat_id` · `trk` · `hsa_*` · `bsft_*` · `oly_*`
`irclickid` · `rb_clickid` · `vero_id` · and 35+ more

</td>
</tr>
</table>

---

<div align="center">

### 📊 Real-Time Analytics Dashboard

</div>

<table>
<tr>
<td width="25%" align="center">

**📈 Statistics**

Total requests blocked<br>Blocked today<br>Trackers intercepted<br>Active rule count<br>Per-list breakdown<br>DNR rule count

</td>
<td width="25%" align="center">

**🌍 Top Domains**

Most-blocked domains<br>Per-domain counters<br>Top 5 in popup<br>Top 50 via API endpoint<br>Updated per request

</td>
<td width="25%" align="center">

**📅 Activity Chart**

7-day bar chart<br>Rendered via Canvas 2D<br>Respects dark mode<br>No external chart library<br>Auto-scales to max value

</td>
<td width="25%" align="center">

**🔌 Network Log**

Real-time request feed<br>Filter by status/type<br>Tracker badge indicator<br>CNAME flag indicator<br>Content-type label<br>Clearable log history

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  BROWSER  (Chrome / Edge / Firefox)                    ║
║                                                                        ║
║  ┌─────────────────────┐   ┌────────────────────────────────────────┐  ║
║  │   POPUP  (5 Tabs)   │   │    SERVICE WORKER  (background.js)     │  ║
║  │                     │   │                                        │  ║
║  │  📊 Overview        │   │  RequestHandler  ──►  DNR Rule Sync    │  ║
║  │  🌐 Network Log     │◄─►│  NetworkLogger   ──►  Async Log Queue  │  ║
║  │  🔧 Filters         │   │  URLCleaner      ──►  UTM Stripping    │  ║
║  │  📋 Lists           │   │  PopupBlocker    ──►  Tab Interception │  ║
║  │  ⚙️  Options        │   │  PerSiteManager  ──►  Mode Cache       │  ║
║  └─────────────────────┘   └──────────────────┬─────────────────────┘  ║
║                                               │  REST API Calls        ║
║  ┌──────────────────────────────────────────┐ │ ┌───────────────────┐  ║
║  │         CONTENT SCRIPTS                  │ │ │ declarativeNet    │  ║
║  │                                          │ │ │ Request  Engine   │  ║
║  │  content.js        Cosmetic CSS + anti-FP│ │ │ (Chrome Native)   │  ║
║  │  cookie_banner.js  40+ CMP auto-reject   │ │ │                   │  ║
║  │  element_picker.js uBO-style DOM picker  │ │ │ ✓ 35 built-in     │  ║
║  │  scriptlet_inj.js  Main-world injection  │ │ │ ✓ Backend-synced  │  ║
║  │  social_blocker.js Widget replacement    │ │ │ ✓ ML-detected     │  ║
║  │  youtube_skipper.js Ad auto-skip         │ │ │ ✓ 0ms latency     │  ║
║  │  notification_bl.js Push API override    │ │ └───────────────────┘  ║
║  └──────────────────────────────────────────┘ │                        ║
╚══════════════════════════════════════════════╪═════════════════════════╝
                                               │  HTTP/REST  localhost:8765
╔══════════════════════════════════════════════╪═════════════════════════╗
║           PYTHON BACKEND  (FastAPI)          │                         ║
║                                             ▼                         ║
║  ┌──────────────────────────────────────────────────────────────────┐  ║
║  │                          API  LAYER                              │  ║
║  │                                                                  │  ║
║  │  /api/filters      /api/stats        /api/settings              │  ║
║  │  /api/whitelist    /api/logs         /api/site-settings         │  ║
║  │  /api/lists        /api/export       /api/scriptlets            │  ║
║  │                                                                  │  ║
║  │  Middleware: Rate Limit (120/min) · Security Headers · CORS     │  ║
║  └──────────────────────────────┬───────────────────────────────────┘  ║
║                                 │                                      ║
║  ┌──────────────────────────────▼───────────────────────────────────┐  ║
║  │                       SERVICE  LAYER                             │  ║
║  │                                                                  │  ║
║  │   BlockingService            StatsService                        │  ║
║  │   (check + record)           (aggregation)                       │  ║
║  │                                                                  │  ║
║  │   UpdateService  ──────────────────────────────────────────────► │  ║
║  │   (APScheduler, 24h interval, EasyList + EasyPrivacy + uBlock)  │  ║
║  └──────────────────────────────┬───────────────────────────────────┘  ║
║                                 │                                      ║
║  ┌──────────────────────────────▼───────────────────────────────────┐  ║
║  │                      FILTER  ENGINE                              │  ║
║  │                                                                  │  ║
║  │  EasyListParser    Full ABP syntax — ||domain^, @@, ##, $opts   │  ║
║  │  UrlMatcher        O(1) hash set + eTLD+1 suffix trie           │  ║
║  │  ContentTypeFilter Per-type policy (script/xhr/frame/ws/ping)   │  ║
║  │  CNAMEResolver     Cloudflare DoH, 5-hop chain resolution       │  ║
║  │  URLCleaner        60+ tracking parameter removal               │  ║
║  │  ScriptletEngine   14 built-in scriptlets, domain-aware bundles │  ║
║  └──────────────────────────────┬───────────────────────────────────┘  ║
║                                 │                                      ║
║  ┌──────────────────────────────▼───────────────────────────────────┐  ║
║  │                       ML  ENGINE                                 │  ║
║  │                                                                  │  ║
║  │  AdClassifier       RandomForest · 20 URL features · CV F1~0.92 │  ║
║  │  FingerprintDetector Rule + ML · 12 FP domains · 20 patterns    │  ║
║  │  BehavioralAnalyzer Sliding-window · burst detection · chains   │  ║
║  └──────────────────────────────┬───────────────────────────────────┘  ║
║                                 │                                      ║
║  ┌──────────────────────────────▼───────────────────────────────────┐  ║
║  │                  DATABASE  (SQLite + WAL Mode)                   │  ║
║  │                                                                  │  ║
║  │  FilterRule      BlockedRequest    NetworkLog                    │  ║
║  │  UserSettings    SiteSetting       FilterList                    │  ║
║  └──────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Request Blocking Decision Flow

```
  Incoming Browser Request
          │
          ▼
  ┌─────────────────────────┐
  │   Chrome DNR Engine     │─── DNR Rule Match? ──► YES ──► ❌ BLOCKED
  │   (native C++ layer)    │                               (sub-millisecond,
  └─────────────────────────┘                                no JS involved)
          │ No rule match
          ▼
  ┌─────────────────────────┐
  │  webRequest.onBefore    │─── Tracker keyword? ──► YES ──► 🔴 Badge++
  │  Request  (observe only)│                                Log entry
  └─────────────────────────┘                                Queue DNR add
          │ Unknown domain
          ▼
  ┌─────────────────────────┐    ┌──────────────────────────────────────┐
  │  Async Backend Check    │───►│  FilterEngine.check_url()            │
  │  (non-blocking, fire    │    │                                      │
  │   and forget from the   │    │  1. Whitelist bypass check           │
  │   service worker)       │    │  2. URL pattern matching (O1)        │
  └─────────────────────────┘    │  3. CNAME chain resolution (DoH)     │
          │                      │  4. RandomForest ML inference        │
          │ Result: blocked?     │  5. Fingerprint detector             │
          ▼                      └──────────────────────────────────────┘
  Add domain to DNR rules
  (subsequent requests blocked
   at 0ms with no JS overhead)
```

---

## 📁 Project Structure

```
📦 Ads-Blocker/
│
├── 🐍 backend/                              Python FastAPI Backend
│   │
│   ├── 🌐 api/
│   │   ├── main.py                          Application factory, lifespan hooks, router registration
│   │   ├── middleware/
│   │   │   ├── rate_limiter.py              slowapi integration — 120 req/min per IP
│   │   │   └── security.py                  HTTP security response headers
│   │   └── routes/
│   │       ├── filters.py                   POST /check, GET/POST/DELETE filter rules
│   │       ├── stats.py                     Dashboard statistics aggregation
│   │       ├── settings.py                  User preference persistence
│   │       ├── whitelist.py                 Domain whitelist CRUD
│   │       ├── logs.py                      Real-time network request log
│   │       ├── site_settings.py             Per-domain mode management
│   │       ├── lists.py                     Filter list subscription management
│   │       ├── export.py                    EasyList-format import and export
│   │       └── scriptlets.py                Domain-aware scriptlet bundle server
│   │
│   ├── 🔍 filters/
│   │   ├── filter_engine.py                 Central engine — coordinates all subsystems
│   │   ├── easylist_parser.py               Full ABP/EasyList syntax parser
│   │   ├── url_matcher.py                   O(1) hash set + eTLD+1 suffix matching
│   │   ├── updater.py                       Remote filter list HTTP downloader
│   │   ├── cname_resolver.py                Cloudflare DoH CNAME chain resolver
│   │   ├── url_cleaner.py                   60+ tracking query parameter stripper
│   │   ├── content_filter.py                Per-content-type policy enforcement
│   │   └── scriptlet_engine.py              14 scriptlet templates with placeholder substitution
│   │
│   ├── 🗃️ models/                           SQLAlchemy ORM Definitions
│   │   ├── filter_rule.py                   Blacklist / whitelist / EasyList rules
│   │   ├── blocked_request.py               Per-request block event log
│   │   ├── settings.py                      Global user preference store
│   │   ├── network_log.py                   Real-time network request log entries
│   │   ├── site_setting.py                  Per-domain blocking mode
│   │   └── filter_list.py                   Filter list subscription registry
│   │
│   ├── 🔧 services/
│   │   ├── blocking_service.py              Application-layer blocking facade
│   │   ├── stats_service.py                 Dashboard aggregation service
│   │   └── update_service.py                APScheduler-driven filter update orchestrator
│   │
│   ├── 💾 database/
│   │   ├── db.py                            SQLAlchemy engine, WAL PRAGMA, session factory
│   │   └── repositories/
│   │       ├── filter_repo.py               FilterRule repository — CRUD + bulk insert
│   │       ├── stats_repo.py                BlockedRequest queries — totals, top domains, daily
│   │       ├── log_repo.py                  NetworkLog queries — recency, CNAME incidents
│   │       └── site_repo.py                 SiteSetting — get-or-create, mode update
│   │
│   └── config.py                            Pydantic BaseSettings — typed env var binding
│
├── 🌐 extension/                            Browser Extension (Manifest V3)
│   ├── manifest.json                        Extension manifest — permissions, CSP, content scripts
│   │
│   ├── 🖼️ popup/
│   │   ├── popup.html                       5-tab popup UI — Overview, Network, Filters, Lists, Options
│   │   ├── popup.js                         Tab logic, stats fetch, whitelist, export, settings sync
│   │   └── popup.css                        Full light/dark theme — CSS custom properties
│   │
│   ├── ⚙️ background/
│   │   ├── background.js                    Service worker — module orchestrator, alarm scheduler
│   │   ├── request_handler.js               DNR rule management, non-blocking request observation
│   │   ├── network_logger.js                Batched async request log flusher (2s intervals)
│   │   ├── url_cleaner.js                   Client-side fast-path UTM parameter stripper
│   │   ├── popup_blocker.js                 webNavigation popup interception
│   │   └── per_site.js                      Per-domain mode memory cache with backend sync
│   │
│   ├── 📝 content_scripts/
│   │   ├── content.js                       25+ cosmetic selectors, MutationObserver, anti-FP noise
│   │   ├── cookie_banner.js                 40+ CMP dismissal — CSS hiding, click, localStorage opt-out
│   │   ├── element_picker.js                Full DOM picker — highlight, toolbar, selector refinement
│   │   ├── scriptlet_injector.js            Backend bundle fetch → <script> main-world injection
│   │   ├── social_blocker.js                7 platforms → privacy placeholder replacement
│   │   ├── youtube_skipper.js               Skip button auto-click, ad fast-forward, banner removal
│   │   └── notification_blocker.js          Notification API override + custom prompt hiding
│   │
│   └── 🎨 assets/icons/
│       ├── icon16.png · icon48.png · icon128.png
│       └── generate_icons.py                Pillow-based programmatic icon generation
│
├── 🤖 ml_engine/                            Machine Learning Subsystem
│   ├── feature_extractor.py                 20-dimensional URL feature vector extractor
│   ├── classifier.py                        RandomForest pipeline + StandardScaler + cross-validation
│   ├── trainer.py                           CLI training script with synthetic data fallback
│   ├── predictor.py                         Lazy-loading production inference wrapper
│   ├── fingerprint_detector.py              Rule + heuristic fingerprinting URL classifier
│   ├── behavioral_analyzer.py               Sliding-window request pattern analyzer
│   └── data/
│       ├── training_data.csv                Labeled URL dataset (auto-generated if absent)
│       └── model.joblib                     Serialized trained pipeline (post-training)
│
├── 🧪 tests/                                Test Suite — 40+ tests
│   ├── conftest.py                          Shared fixtures — in-memory SQLite, TestClient factory
│   ├── test_api/test_routes.py              20+ FastAPI integration tests across all routes
│   ├── test_filters/test_engine.py          UrlMatcher, EasyListParser, FilterEngine unit tests
│   ├── test_ml/test_classifier.py           Feature extractor and classifier behavioral tests
│   └── test_database/test_repos.py          Repository layer unit tests
│
├── 📚 docs/
│   ├── architecture.md                      Detailed architecture document
│   ├── installation.md                      Step-by-step installation guide
│   ├── deployment.md                        Browser build and deployment procedures
│   └── api_reference.md                     Complete REST API specification
│
├── environment.yml                          Anaconda environment specification (Python 3.11)
├── setup.py                                 Python package definition with extras
├── run.py                                   Backend entry point with uvicorn configuration
├── setup_and_test.bat                       One-click Windows setup and launch script
├── .env.example                             Environment variable template with documentation
└── LICENSE                                  MIT License
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/DzCodeProgrammer/Ads-Blocker.git
cd Ads-Blocker

# 2. Install Python dependencies
pip install fastapi "uvicorn[standard]" httpx sqlalchemy pydantic \
    pydantic-settings python-dotenv slowapi tldextract apscheduler \
    aiofiles scikit-learn numpy pandas joblib Pillow requests

# 3. Configure the environment
cp .env.example .env
# Edit .env — at minimum, set a strong APP_SECRET_KEY

# 4. Generate extension icons
python extension/assets/icons/generate_icons.py

# 5. Train the ML model (optional but strongly recommended)
python -m ml_engine.trainer

# 6. Start the backend server
python run.py
# → Uvicorn running on http://127.0.0.1:8765
# → Interactive API docs at http://127.0.0.1:8765/docs
```

> 🪟 **Windows shortcut:** Double-click **`setup_and_test.bat`** to execute steps 2–6 automatically in a single terminal window.

Load the extension: `chrome://extensions/` → **Developer mode** → **Load unpacked** → select the `extension/` directory.

---

## 🔧 Installation

<details>
<summary><strong>🐍 Anaconda / Miniconda (Recommended)</strong></summary>

```bash
# Create a reproducible isolated environment
conda env create -f environment.yml

# Activate the environment
conda activate adblocker

# Verify installation
python --version        # Python 3.11.x
uvicorn --version       # 0.29.x
```

</details>

<details>
<summary><strong>📦 Standard pip</strong></summary>

```bash
# Full installation including development tools
pip install -e ".[dev]"

# Or install only production dependencies
pip install fastapi "uvicorn[standard]" httpx requests pandas numpy \
    scikit-learn APScheduler sqlalchemy alembic pydantic pydantic-settings \
    python-dotenv aiofiles slowapi tldextract joblib Pillow
```

</details>

<details>
<summary><strong>⚙️ Environment Configuration</strong></summary>

```env
# ─── Application ─────────────────────────────────────────────────────────────
APP_ENV=development              # 'development' enables /docs and auto-reload
APP_HOST=127.0.0.1               # Bind to loopback only — never expose externally
APP_PORT=8765                    # Port must match extension BACKEND constant
APP_SECRET_KEY=replace-with-a-cryptographically-strong-random-string

# ─── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL=sqlite:///./adblocker.db

# ─── Remote Filter Lists ──────────────────────────────────────────────────────
EASYLIST_URL=https://easylist.to/easylist/easylist.txt
EASYPRIVACY_URL=https://easylist.to/easylist/easyprivacy.txt
UBLOCK_URL=https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt
FILTER_UPDATE_INTERVAL=24        # Hours between automatic filter list refreshes

# ─── Rate Limiting ────────────────────────────────────────────────────────────
RATE_LIMIT_PER_MINUTE=120

# ─── Machine Learning ─────────────────────────────────────────────────────────
ML_MODEL_PATH=./ml_engine/data/model.joblib
ML_CONFIDENCE_THRESHOLD=0.75     # Probability threshold [0.0, 1.0] for ML blocking

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_LEVEL=INFO                   # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FILE=./logs/adblocker.log

# ─── CORS (set to your extension's ID after loading it in Chrome) ─────────────
CORS_ORIGINS=chrome-extension://YOUR_EXTENSION_ID_HERE
```

</details>

---

## 🌐 Loading the Extension

<details>
<summary><strong>🟦 Google Chrome / Microsoft Edge</strong></summary>

1. Navigate to `chrome://extensions/` (or `edge://extensions/`)
2. Enable **Developer mode** via the toggle in the upper-right corner
3. Click **Load unpacked**
4. Select the `extension/` directory within the cloned repository
5. Note the **Extension ID** displayed beneath the extension card
6. Update `.env`:
   ```env
   CORS_ORIGINS=chrome-extension://YOUR_EXTENSION_ID_HERE
   ```
7. Restart the backend: `python run.py`
8. Trigger an initial filter update via the popup **Lists** tab or:
   ```bash
   curl -X POST http://127.0.0.1:8765/api/filters/update
   ```

</details>

<details>
<summary><strong>🟠 Mozilla Firefox</strong></summary>

1. Navigate to `about:debugging`
2. Click **This Firefox** in the left sidebar
3. Click **Load Temporary Add-on...**
4. Select `extension/manifest.json`

> ⚠️ Temporary add-ons are removed when the browser restarts. For a persistent installation, use `web-ext sign` with an AMO developer account, or distribute the signed `.xpi` internally.

**Firefox-specific notes:**
- The origin prefix for CORS is `moz-extension://` rather than `chrome-extension://`
- `webRequest` blocking is still permitted in Firefox MV3, but this implementation uses DNR for cross-browser consistency

</details>

---

## 📡 API Reference

**Base URL:** `http://127.0.0.1:8765`  
**Interactive Documentation:** `http://127.0.0.1:8765/docs` *(development mode only)*

<details>
<summary><strong>🔍 Filter Rules & URL Checking</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Backend health check and version |
| `POST` | `/api/filters/check` | Evaluate whether a URL should be blocked |
| `GET` | `/api/filters` | Retrieve all active filter rules (filterable by type) |
| `POST` | `/api/filters` | Add a custom blacklist or whitelist rule |
| `DELETE` | `/api/filters/{id}` | Deactivate a rule by ID |
| `POST` | `/api/filters/update` | Trigger an immediate remote filter list refresh |

```bash
# Check a URL against the full rule set including ML inference
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ads.doubleclick.net/pixel.gif",
    "tab_url": "https://news.example.com/article",
    "enable_ml": true
  }'
```

```json
{
  "url": "https://ads.doubleclick.net/pixel.gif",
  "domain": "ads.doubleclick.net",
  "blocked": true,
  "matched_rule": "doubleclick.net",
  "is_tracker": true,
  "ml_blocked": false,
  "ml_confidence": null,
  "is_cname_cloaked": false,
  "cname_real_domain": null,
  "tracking_params_removed": []
}
```

</details>

<details>
<summary><strong>📊 Statistics & Analytics</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/stats/summary` | Aggregate totals: blocked, today, trackers, rule count |
| `GET` | `/api/stats/top-domains?limit=10` | Most frequently blocked domains |
| `GET` | `/api/stats/daily?days=7` | Per-day block counts for the last N days |
| `GET` | `/api/stats/breakdown` | Rule count partitioned by filter list type |

</details>

<details>
<summary><strong>⚙️ Settings & Whitelist</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/settings` | Retrieve current user preference state |
| `PUT` | `/api/settings` | Partial update of any preference fields |
| `GET` | `/api/whitelist` | List all whitelisted domains |
| `POST` | `/api/whitelist` | Add a domain to the whitelist |
| `DELETE` | `/api/whitelist/{id}` | Remove a domain from the whitelist |

</details>

<details>
<summary><strong>🌐 Network Log & Per-Site Configuration</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/logs?limit=200` | Retrieve recent request log entries |
| `POST` | `/api/logs/record` | Record a new log entry (called by service worker) |
| `GET` | `/api/logs/cname` | Retrieve only CNAME uncloaking incidents |
| `DELETE` | `/api/logs` | Clear all log entries |
| `GET` | `/api/site-settings` | List all custom per-domain configurations |
| `GET` | `/api/site-settings/{domain}` | Retrieve mode for a specific domain |
| `PUT` | `/api/site-settings/{domain}` | Set blocking mode for a domain |
| `DELETE` | `/api/site-settings/{domain}` | Reset a domain to global default behavior |

</details>

<details>
<summary><strong>📋 Filter Lists, Export & Scriptlets</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/lists` | List all filter list subscriptions |
| `POST` | `/api/lists` | Subscribe to a new filter list URL |
| `PUT` | `/api/lists/{id}` | Enable or disable a specific list |
| `DELETE` | `/api/lists/{id}` | Unsubscribe from a custom list |
| `POST` | `/api/lists/{id}/update` | Force refresh of a single filter list |
| `GET` | `/api/export/rules` | Export custom rules in EasyList `.txt` format |
| `POST` | `/api/export/import` | Import rules from an EasyList-format text body |
| `GET` | `/api/scriptlets` | List all available scriptlets and defaults |
| `POST` | `/api/scriptlets/bundle` | Generate a domain-specific scriptlet bundle |

</details>

---

## 🤖 Machine Learning Engine

### Feature Engineering (20-Dimensional Feature Vector)

| # | Feature Name | Description | Type |
|---|-------------|-------------|------|
| 1 | `url_length` | Total character length of the URL | Numeric |
| 2 | `domain_length` | Character length of the registered domain | Numeric |
| 3 | `path_length` | Character length of the URL path component | Numeric |
| 4 | `query_length` | Character length of the query string | Numeric |
| 5 | `subdomain_depth` | Number of subdomain levels | Numeric |
| 6 | `path_depth` | Number of forward slashes in the path | Numeric |
| 7 | `query_param_count` | Number of distinct query parameters | Numeric |
| 8 | `digit_ratio_domain` | Proportion of numeric characters in domain | Float [0,1] |
| 9 | `digit_ratio_path` | Proportion of numeric characters in path | Float [0,1] |
| 10 | `url_entropy` | Shannon entropy of the entire URL string | Float |
| 11 | `domain_entropy` | Shannon entropy of the domain component | Float |
| 12 | `has_ip_address` | Whether the host is a raw IP address | Binary |
| 13 | `has_port` | Whether an explicit port number is present | Binary |
| 14 | `suspicious_tld` | Whether the TLD is in the high-risk set (.xyz, .click, .download) | Binary |
| 15 | `ad_keyword_count_domain` | Count of ad/tracker keywords in domain | Integer |
| 16 | `ad_keyword_count_path` | Count of ad/tracker keywords in path | Integer |
| 17 | `has_redirect_param` | Presence of redirection parameters (url, goto, redirect) | Binary |
| 18 | `hyphen_count` | Total hyphen count in the URL | Integer |
| 19 | `dot_count_subdomain` | Number of dots in the subdomain component | Integer |
| 20 | `long_subdomain` | Whether the subdomain exceeds 30 characters | Binary |

### Model Training

```bash
# Train with your own labeled dataset
# Required CSV format: columns 'url' (string) and 'label' (0=benign, 1=ad/tracker)
python -m ml_engine.trainer

# If no training_data.csv is found, the trainer generates synthetic data
# from a curated set of known ad domains and benign URLs.

# Typical output:
# Model trained — CV F1: 0.9241 ± 0.0183
# Model saved → ml_engine/data/model.joblib
```

### Fingerprint & Behavioral Detection

The `FingerprintDetector` and `BehavioralAnalyzer` operate independently of the core ML classifier:

- **FingerprintDetector** — Identifies URLs serving fingerprinting libraries using 21 regex patterns and a domain blocklist of 15 known fingerprinting services
- **BehavioralAnalyzer** — Maintains a sliding time window per tab, flagging anomalies such as tracker synchronization bursts (≥5 distinct tracker XHR destinations within 30 seconds), pixel flooding (≥6 distinct image-tracker domains), and redirect chains through ad networks

---

## 📋 Filter Lists

Eight curated filter lists are pre-registered at first run and updated automatically every 24 hours:

| # | Name | Category | Estimated Rules | Description |
|---|------|----------|----------------|-------------|
| 1 | **EasyList** | 🔴 Ads | ~70,000 | The primary international ad filter — removes banner, video, and sponsored content |
| 2 | **EasyPrivacy** | 🔵 Privacy | ~30,000 | Comprehensive tracking removal — analytics, beacons, fingerprinting services |
| 3 | **uBlock Origin Filters** | 🔴 Ads | ~25,000 | uBlock Origin's proprietary filter supplements |
| 4 | **uBlock Privacy** | 🔵 Privacy | ~5,000 | uBlock Origin's curated privacy protection rules |
| 5 | **Peter Lowe's List** | 🔴 Ads | ~3,000 | Curated ad and tracking server hostname list |
| 6 | **Fanboy's Annoyance List** | 🟡 Annoyances | ~30,000 | Social widgets, interstitials, push prompts, cookie notices |
| 7 | **Cookie AutoDelete Supplementary** | 🍪 Cookies | ~10,000 | GDPR consent banners and cookie dialogs |
| 8 | **NoCoin Resource Abuse** | ⚠️ Malware | ~2,000 | Cryptocurrency mining scripts and malicious resource loading |

**Subscribing to additional lists:**

```bash
curl -X POST http://127.0.0.1:8765/api/lists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ABPindo (Indonesian)",
    "url": "https://raw.githubusercontent.com/heradhis/indonesianadblockrules/master/subscriptions/abpindo.txt",
    "category": "ads",
    "description": "Indonesian regional ad filter"
  }'
```

---

## ⚙️ Configuration

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | Set to `production` to disable `/docs` and hot-reload |
| `APP_HOST` | `127.0.0.1` | Bind address — never set to `0.0.0.0` in production |
| `APP_PORT` | `8765` | Must match the `BACKEND` constant in extension JS files |
| `APP_SECRET_KEY` | *(required)* | Replace with a cryptographically random string |
| `DATABASE_URL` | `sqlite:///./adblocker.db` | SQLAlchemy-compatible database connection string |
| `FILTER_UPDATE_INTERVAL` | `24` | Hours between APScheduler filter refresh cycles |
| `RATE_LIMIT_PER_MINUTE` | `120` | Maximum API requests per minute per source IP |
| `ML_CONFIDENCE_THRESHOLD` | `0.75` | Minimum classifier probability [0.0–1.0] to trigger a block |
| `LOG_LEVEL` | `INFO` | Python logging level for the backend process |
| `CORS_ORIGINS` | *(required)* | Comma-separated list of allowed extension origin prefixes |

### Per-Site Blocking Mode Reference

| Mode | Icon | Blocked Request Types | Ideal Use Case |
|------|------|----------------------|---------------|
| **Normal** | 🔵 | Known ad domains + trackers per filter rules | Standard daily browsing |
| **Aggressive** | 🔥 | All of the above + all third-party `script`, `xmlhttprequest`, `sub_frame` | Maximum privacy, high-risk sites |
| **Disabled** | ⚫ | Nothing — full pass-through | Development, trusted intranets, troubleshooting |

---

## 🧪 Testing

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Execute the full test suite
pytest tests/ -v

# Generate HTML coverage report
pytest tests/ -v --cov=backend --cov=ml_engine \
    --cov-report=html --cov-report=term-missing

# Open the coverage report
# Windows: start htmlcov/index.html
# macOS:   open htmlcov/index.html
# Linux:   xdg-open htmlcov/index.html

# Run a specific test module
pytest tests/test_filters/test_engine.py -v
pytest tests/test_api/test_routes.py -v -k "whitelist"
```

### Manual API Verification

```bash
# Confirm backend health
curl http://127.0.0.1:8765/health

# Verify ad URL detection
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js","enable_ml":true}'

# Confirm safe URL passes through
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com/user/repository","enable_ml":false}'

# Retrieve aggregated statistics
curl http://127.0.0.1:8765/api/stats/summary | python -m json.tool

# Fetch a scriptlet bundle for youtube.com
curl -X POST http://127.0.0.1:8765/api/scriptlets/bundle \
  -H "Content-Type: application/json" \
  -d '{"domain":"youtube.com","include_defaults":true}' | python -m json.tool

# Export custom rules in EasyList format
curl http://127.0.0.1:8765/api/export/rules
```

---

## 🔒 Security

Security has been a first-class consideration throughout the design of this project:

| Layer | Implementation |
|-------|---------------|
| **Input Validation** | Every API endpoint validates inputs through Pydantic models — URL scheme enforcement, domain format regex, pattern character allowlisting, maximum length enforcement |
| **Rate Limiting** | `slowapi` enforces 120 requests per minute per source IP address, protecting against enumeration and DoS attempts |
| **HTTP Security Headers** | All responses include `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, `Cache-Control: no-store` |
| **CORS Enforcement** | Only explicitly configured extension origins (e.g., `chrome-extension://abc123`) are permitted — wildcard origins are never acceptable in production |
| **SQLite WAL Mode** | Write-Ahead Logging enables concurrent reads without blocking writes, and foreign key constraints are enforced via PRAGMA |
| **Content Security Policy** | Extension pages enforce `script-src 'self'` — prohibiting inline scripts, eval, and external script loading |
| **Declarative Blocking** | Request blocking occurs in Chrome's native C++ DNR engine — no arbitrary JavaScript executes in the request path |
| **Local-Only Backend** | The backend binds exclusively to `127.0.0.1` by default — it is not accessible from the network under any standard configuration |
| **No External Telemetry** | Zero data is transmitted to any external server beyond the filter list downloads from public CDNs |
| **Sanitized Output** | All user-controlled strings rendered in popup HTML are escaped through a dedicated `escHtml()` function, preventing XSS in the extension UI |

---

## 📊 Benchmarks

Comparison against leading ad-blocking solutions:

| Capability | AdBlocker Pro | uBlock Origin | AdBlock Plus | Brave Shield |
|-----------|:---:|:---:|:---:|:---:|
| Python/native backend | ✅ | ❌ | ❌ | ✅ |
| Machine learning detection | ✅ | ❌ | ❌ | ✅ |
| CNAME uncloaking | ✅ | ✅ | ❌ | ✅ |
| URL parameter cleaning | ✅ | ⚠️ partial | ❌ | ✅ |
| Element picker | ✅ | ✅ | ✅ | ❌ |
| Scriptlet injection | ✅ | ✅ | ❌ | ❌ |
| Cookie banner auto-dismiss | ✅ | ✅ | ❌ | ✅ |
| Social widget replacement | ✅ | ✅ | ❌ | ✅ |
| YouTube ad skip | ✅ | ✅ | ❌ | ✅ |
| Push notification block | ✅ | ✅ | ❌ | ✅ |
| Popup window block | ✅ | ✅ | ✅ | ✅ |
| Per-site blocking modes | ✅ | ✅ | ✅ | ✅ |
| Real-time network log | ✅ | ✅ | ❌ | ❌ |
| REST API | ✅ | ❌ | ❌ | ❌ |
| Filter list management UI | ✅ | ✅ | ✅ | ❌ |
| EasyList import/export | ✅ | ✅ | ✅ | ❌ |
| Fingerprinting defense | ✅ | ✅ | ❌ | ✅ |
| Behavioral analysis | ✅ | ❌ | ❌ | ❌ |
| Open source | ✅ | ✅ | ✅ | ✅ |

---

## 📜 Changelog

<details>
<summary><strong>v2.1.0 — Manifest V3 Compliance (Current)</strong></summary>

- **Fixed:** Removed `webRequest` blocking flag (`['blocking']`) which is prohibited for regular extensions in Chrome MV3; replaced with `declarativeNetRequest` dynamic rule synchronization
- **Added:** 35 hardcoded high-confidence tracker domains loaded as DNR rules at service worker startup
- **Added:** `_addDNRRuleForDomain()` — dynamically extends DNR rules when ML or backend detects a previously unknown threat
- **Improved:** `webRequest.onBeforeRequest` now serves exclusively as a non-blocking observation layer for logging and badge updates
- **Fixed:** `onRuleMatchedDebug` listener for accurate block event tracking in unpacked extension mode

</details>

<details>
<summary><strong>v2.0.0 — Major Feature Expansion</strong></summary>

- **Added:** Element Picker — full uBlock Origin-style click-to-block with DOM traversal, selector refinement, preview mode
- **Added:** Cookie Banner Auto-Dismisser — covers 40+ CMPs, multilingual reject button detection, localStorage opt-out
- **Added:** Social Widget Blocker — 7 platforms with privacy placeholders and "Allow Once" restoration
- **Added:** YouTube Ad Skipper — pre-roll, mid-roll, overlay, and banner ad elimination
- **Added:** Notification Permission Blocker — Notification API override + custom prompt UI hiding
- **Added:** Scriptlet Engine — 14 scriptlets with domain-aware bundle delivery from backend
- **Added:** CNAME Uncloaking — Cloudflare DoH queries with 5-hop chain resolution
- **Added:** URL Tracking Parameter Cleaner — 60+ parameter families stripped pre-navigation
- **Added:** Network Request Logger — real-time batched log with filter chip UI
- **Added:** Per-Site Blocking Modes — Off / Normal / Aggressive with backend persistence
- **Added:** Filter List Manager — 8 built-in lists, custom URL subscription, per-list toggle
- **Added:** EasyList Import/Export — full round-trip custom rule backup and restore
- **Added:** FingerprintDetector ML module — pattern + domain-based fingerprinting identification
- **Added:** BehavioralAnalyzer ML module — sliding-window threat burst detection
- **Redesigned:** Popup UI — five-tab layout (Overview, Network, Filters, Lists, Options)
- **Added:** 5 new API route modules: `/api/logs`, `/api/site-settings`, `/api/lists`, `/api/export`, `/api/scriptlets`
- **Added:** 3 new database models: `NetworkLog`, `SiteSetting`, `FilterList`

</details>

<details>
<summary><strong>v1.0.0 — Initial Release</strong></summary>

- **Added:** FastAPI backend with SQLite persistence and WAL mode
- **Added:** EasyList/ABP filter syntax parser
- **Added:** O(1) URL matcher — hash set + eTLD+1 suffix trie
- **Added:** Random Forest ML classifier with 20-dimensional feature extraction
- **Added:** APScheduler-driven 24-hour filter auto-update pipeline
- **Added:** Popup dashboard with statistics, top domains, daily bar chart
- **Added:** Whitelist management — add, list, remove
- **Added:** Cosmetic filtering with 25+ CSS selectors and MutationObserver
- **Added:** Basic anti-fingerprinting — Canvas and AudioContext noise injection
- **Added:** Full dark mode support
- **Added:** Chrome, Edge, and Firefox compatibility (Manifest V3)
- **Added:** 40+ unit and integration tests with in-memory SQLite fixtures

</details>

---

## 🤝 Contributing

Contributions are welcome and encouraged. Please adhere to the following guidelines:

1. **Fork** the repository and create a feature branch: `git checkout -b feature/descriptive-feature-name`
2. **Follow coding standards:**
   - Python: PEP8 compliance, full type annotations, Black formatting, no bare `except` clauses
   - JavaScript: ES2022 module syntax, `'use strict'` directive, no external runtime dependencies
   - Architecture: strict Clean Architecture layering — routes → services → engine → repositories
3. **Write tests** for all new backend functionality; maintain coverage above 80%
4. **Validate** with `pytest tests/ -v` before submitting
5. **Document** public API changes in `docs/api_reference.md`
6. **Open a Pull Request** with a clear title, problem statement, and solution description

---

## 📄 License

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2026 DzCodeProgrammer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

See the [LICENSE](LICENSE) file for the full text.

---

<div align="center">

<br>

**Built with precision using Python, FastAPI, and Machine Learning**

<br>

[![GitHub](https://img.shields.io/badge/GitHub-DzCodeProgrammer-181717?style=for-the-badge&logo=github)](https://github.com/DzCodeProgrammer/Ads-Blocker)
&nbsp;&nbsp;
[![Issues](https://img.shields.io/badge/Report_Bug-E53E3E?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DzCodeProgrammer/Ads-Blocker/issues)
&nbsp;&nbsp;
[![License](https://img.shields.io/badge/MIT_License-38a169?style=for-the-badge)](LICENSE)

<br>

*If this project has been useful to you, consider leaving a ⭐ — it helps others discover the project.*

<br>

</div>
