<div align="center">

<img src="extension/assets/icons/icon128.png" alt="AdBlocker Pro Logo" width="96" height="96" />

# AdBlocker Pro

**Professional Ad Blocker Browser Extension**  
Python · FastAPI · Machine Learning · Manifest V3

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Manifest V3](https://img.shields.io/badge/Manifest-V3-4285F4?logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/intro/)
[![Chrome](https://img.shields.io/badge/Chrome-88%2B-4285F4?logo=googlechrome&logoColor=white)]()
[![Edge](https://img.shields.io/badge/Edge-88%2B-0078D7?logo=microsoftedge&logoColor=white)]()
[![Firefox](https://img.shields.io/badge/Firefox-109%2B-FF7139?logo=firefox&logoColor=white)]()

---

*Block ads, trackers, cookie banners, popups, and fingerprinting scripts —  
powered by Python ML backend with CNAME uncloaking and 300k+ filter rules.*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Backend](#running-the-backend)
- [Loading the Extension](#loading-the-extension)
- [API Reference](#api-reference)
- [ML Engine](#ml-engine)
- [Filter Lists](#filter-lists)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**AdBlocker Pro** is a full-stack browser extension where **Python is the brain and JavaScript is the hands**. Unlike traditional JavaScript-only ad blockers, this project uses a local **FastAPI backend** to handle heavy lifting: filter list management, machine learning inference, CNAME resolution, behavioral analysis, and statistics aggregation.

The browser extension (Manifest V3) communicates with the backend via REST API, syncing block rules to Chrome's native **declarativeNetRequest** engine for maximum performance.

```
Browser Extension  ←──REST──→  Python FastAPI  ←──→  SQLite DB
  (MV3 + DNR)                  (Port 8765)           Filter Rules
                                    │                 Block Stats
                                    ├──→  ML Engine   Site Settings
                                    ├──→  CNAME DoH   Network Log
                                    └──→  Filter Lists
```

---

## Features

### Core Blocking
| Feature | Description |
|---------|-------------|
| **URL Blacklist** | Block URLs by exact domain, eTLD+1, substring, or regex |
| **EasyList Parser** | Full ABP/EasyList syntax — `\|\|domain^`, `@@`, `##`, `$options` |
| **300k+ Rules** | EasyList, EasyPrivacy, uBlock Filters, uBlock Privacy, Peter Lowe's list |
| **Fanboy's Annoyance** | Block social media share buttons and in-page annoyances |
| **NoCoin** | Block cryptocurrency mining scripts |
| **Custom Rules** | Add/remove rules via popup or API in EasyList syntax |
| **Import / Export** | Backup and restore rules as `.txt` (EasyList format) |

### Privacy & Tracking
| Feature | Description |
|---------|-------------|
| **CNAME Uncloaking** | Detect trackers hiding behind first-party CNAME aliases via DNS-over-HTTPS |
| **URL Tracker Cleaner** | Strip 60+ tracking parameters: `utm_*`, `fbclid`, `gclid`, `msclkid`, `ttclid`, etc. |
| **Anti-Fingerprinting** | Canvas noise injection, AudioContext noise, WebGL protection |
| **WebRTC IP Leak Block** | Prevent IP address leaks via STUN servers |
| **Cookie Referrer Cleaning** | Remove identifying referrer headers |

### Content Blocking
| Feature | Description |
|---------|-------------|
| **Cookie Banner Dismisser** | Auto-reject 40+ Consent Management Platforms (Cookiebot, OneTrust, Quantcast, TrustArc, Usercentrics, Didomi, and more) |
| **Social Widget Blocker** | Replace Facebook, Twitter/X, LinkedIn, Instagram, YouTube, TikTok, Spotify embeds with privacy-respecting placeholders |
| **YouTube Ad Skipper** | Auto-skip pre-roll, mid-roll, overlay, and banner ads on YouTube |
| **Notification Blocker** | Auto-deny Web Push permission prompts (OneSignal, Pushwoosh, etc.) |
| **Popup Blocker** | Block ad popup windows via `webNavigation` interception |
| **Cosmetic Filtering** | CSS element-hiding with 25+ built-in selectors + MutationObserver |

### Advanced
| Feature | Description |
|---------|-------------|
| **Element Picker** | uBlock Origin-style click-to-block: hover → click → create cosmetic rule |
| **Scriptlet Injection** | 14 built-in scriptlets injected into page main world to defeat anti-adblock |
| **Per-Site Modes** | Off / Normal / Aggressive mode per domain |
| **Content-Type Filter** | Block by request type: script, XHR, frame, media, websocket |
| **Filter List Manager** | Subscribe/unsubscribe to filter lists, enable/disable per-list |
| **Network Logger** | Real-time log of all requests with status, type, tracker flag |
| **Dark Mode** | Full light/dark theme support |

### Machine Learning
| Feature | Description |
|---------|-------------|
| **Ad URL Classifier** | Random Forest with 20 URL features (entropy, digit ratio, ad keywords, etc.) |
| **Fingerprint Detector** | Rule + ML based detection of fingerprintjs, WebGL FP, Canvas FP scripts |
| **Behavioral Analyzer** | Sliding-window detection of tracker sync bursts, pixel chains, redirect chains |
| **Auto Training** | `python -m ml_engine.trainer` — generates synthetic data if none available |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BROWSER (Chrome / Edge / Firefox)                │
│                                                                     │
│  ┌──────────────────┐   ┌────────────────────────────────────────┐  │
│  │   popup/         │   │   background/ (Service Worker)         │  │
│  │   popup.html     │   │                                        │  │
│  │   popup.css      │◄─►│   background.js       (orchestrator)  │  │
│  │   popup.js       │   │   request_handler.js  (DNR rules)      │  │
│  │   (5 tabs)       │   │   network_logger.js   (async log)      │  │
│  └──────────────────┘   │   url_cleaner.js      (UTM strip)      │  │
│                         │   popup_blocker.js    (webNavigation)  │  │
│  ┌──────────────────┐   │   per_site.js         (mode cache)     │  │
│  │  content_scripts/│   └──────────────┬─────────────────────────┘  │
│  │  content.js      │                  │ REST API                   │
│  │  cookie_banner   │         ┌────────▼────────┐                  │
│  │  element_picker  │         │  declarativeNet  │                  │
│  │  scriptlet_inj.  │         │  Request (DNR)   │                  │
│  │  social_blocker  │         │  Chrome Engine   │                  │
│  │  youtube_skipper │         └─────────────────┘                  │
│  │  notification_bl │                                              │
│  └──────────────────┘                                              │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTP REST (localhost:8765)
┌───────────────────────────────▼─────────────────────────────────────┐
│                     PYTHON BACKEND (FastAPI)                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                        API Layer                            │   │
│  │  /api/filters   · /api/stats    · /api/settings             │   │
│  │  /api/whitelist · /api/logs     · /api/site-settings        │   │
│  │  /api/lists     · /api/export   · /api/scriptlets           │   │
│  └────────────────────────┬────────────────────────────────────┘   │
│                           │                                         │
│  ┌────────────────────────▼────────────────────────────────────┐   │
│  │                     Service Layer                           │   │
│  │   BlockingService  ·  StatsService  ·  UpdateService        │   │
│  │   (APScheduler — auto-updates filter lists every 24h)       │   │
│  └────────────────────────┬────────────────────────────────────┘   │
│                           │                                         │
│  ┌────────────────────────▼────────────────────────────────────┐   │
│  │                    Filter Engine                            │   │
│  │   EasyListParser  ·  UrlMatcher (O(1) hash set)            │   │
│  │   ContentTypeFilter  ·  CNAMEResolver (DoH)                │   │
│  │   URLCleaner  ·  ScriptletEngine                           │   │
│  └────────────────────────┬────────────────────────────────────┘   │
│                           │                                         │
│  ┌────────────────────────▼────────────────────────────────────┐   │
│  │                      ML Engine                              │   │
│  │   AdClassifier (RandomForest, 20 features)                 │   │
│  │   FingerprintDetector  ·  BehavioralAnalyzer               │   │
│  └────────────────────────┬────────────────────────────────────┘   │
│                           │                                         │
│  ┌────────────────────────▼────────────────────────────────────┐   │
│  │                   Database (SQLite)                         │   │
│  │   FilterRule  ·  BlockedRequest  ·  NetworkLog             │   │
│  │   UserSettings  ·  SiteSetting  ·  FilterList              │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Request Blocking Flow

```
Browser Request
      │
      ▼
Chrome DNR Engine ──── matches rule? ──── YES ──► BLOCKED (0ms)
      │                                            (no JS involved)
      NO
      │
      ▼
webRequest.onBeforeRequest (observe-only, no blocking)
      │
      ├── Is tracker keyword? ──► badge + log
      │
      └── Unknown domain ──► POST /api/filters/check (async)
                                      │
                              FilterEngine.check_url()
                                      │
                              ┌───────┴────────┐
                              │                │
                         UrlMatcher        ML Predictor
                         (O(1) lookup)     (score ≥ 0.75?)
                              │                │
                         CNAME check      FingerprintDetector
                              │                │
                              └───────┬────────┘
                                      │
                              Blocked? ──► add to DNR rules
                                          (blocks NEXT request)
```

---

## Project Structure

```
Ads-Blocker/
│
├── backend/                         # Python FastAPI backend
│   ├── api/
│   │   ├── main.py                  # App factory, lifespan, middleware
│   │   ├── middleware/
│   │   │   ├── rate_limiter.py      # slowapi — 120 req/min
│   │   │   └── security.py          # Security headers (CSP, X-Frame, etc.)
│   │   └── routes/
│   │       ├── filters.py           # POST /check, GET/POST/DELETE rules
│   │       ├── stats.py             # Dashboard statistics
│   │       ├── settings.py          # User preferences
│   │       ├── whitelist.py         # Whitelist management
│   │       ├── logs.py              # Network request log
│   │       ├── site_settings.py     # Per-domain mode (off/normal/aggressive)
│   │       ├── lists.py             # Filter list subscriptions
│   │       ├── export.py            # Import/export EasyList rules
│   │       └── scriptlets.py        # Serve JS scriptlet bundles
│   ├── filters/
│   │   ├── filter_engine.py         # Core engine — integrates all subsystems
│   │   ├── easylist_parser.py       # ABP/EasyList syntax parser
│   │   ├── url_matcher.py           # O(1) domain + suffix matching
│   │   ├── updater.py               # Remote filter list downloader
│   │   ├── cname_resolver.py        # DNS-over-HTTPS CNAME uncloaking
│   │   ├── url_cleaner.py           # Strip 60+ tracking query parameters
│   │   ├── content_filter.py        # Per content-type blocking policy
│   │   └── scriptlet_engine.py      # 14 built-in JS scriptlets
│   ├── models/
│   │   ├── filter_rule.py           # ORM: filter rules (blacklist/whitelist)
│   │   ├── blocked_request.py       # ORM: blocked request statistics
│   │   ├── settings.py              # ORM: user settings
│   │   ├── network_log.py           # ORM: real-time network log
│   │   ├── site_setting.py          # ORM: per-domain mode
│   │   └── filter_list.py           # ORM: filter list subscriptions
│   ├── services/
│   │   ├── blocking_service.py      # Business logic facade
│   │   ├── stats_service.py         # Dashboard aggregation
│   │   └── update_service.py        # APScheduler filter auto-update
│   ├── database/
│   │   ├── db.py                    # SQLAlchemy engine, WAL mode, session
│   │   └── repositories/
│   │       ├── filter_repo.py       # FilterRule CRUD
│   │       ├── stats_repo.py        # BlockedRequest queries
│   │       ├── log_repo.py          # NetworkLog queries
│   │       └── site_repo.py         # SiteSetting CRUD
│   └── config.py                    # Pydantic Settings (env vars)
│
├── extension/                       # Browser Extension (Manifest V3)
│   ├── manifest.json                # Extension manifest
│   ├── popup/
│   │   ├── popup.html               # 5-tab popup UI
│   │   ├── popup.js                 # Popup logic (stats, settings, lists)
│   │   └── popup.css                # Light/dark theme CSS
│   ├── background/
│   │   ├── background.js            # Service worker entry point
│   │   ├── request_handler.js       # DNR rule management + observation
│   │   ├── network_logger.js        # Batched async request logger
│   │   ├── url_cleaner.js           # Client-side UTM param stripper
│   │   ├── popup_blocker.js         # Popup window interception
│   │   └── per_site.js              # Per-domain mode cache
│   ├── content_scripts/
│   │   ├── content.js               # Cosmetic filter + anti-fingerprinting
│   │   ├── cookie_banner.js         # GDPR consent auto-dismisser
│   │   ├── element_picker.js        # Click-to-block element picker
│   │   ├── scriptlet_injector.js    # Main-world scriptlet injection
│   │   ├── social_blocker.js        # Social widget replacement
│   │   ├── youtube_skipper.js       # YouTube ad auto-skipper
│   │   └── notification_blocker.js  # Push notification blocker
│   └── assets/icons/
│       ├── icon16.png
│       ├── icon48.png
│       ├── icon128.png
│       └── generate_icons.py        # Pillow icon generator
│
├── ml_engine/                       # Machine Learning Engine
│   ├── feature_extractor.py         # 20 URL features extraction
│   ├── classifier.py                # RandomForest pipeline + cross-val
│   ├── trainer.py                   # Training script
│   ├── predictor.py                 # Production predictor wrapper
│   ├── fingerprint_detector.py      # Fingerprinting URL detector
│   ├── behavioral_analyzer.py       # Request pattern analysis
│   └── data/
│       ├── training_data.csv        # (auto-generated if missing)
│       └── model.joblib             # (generated after training)
│
├── tests/                           # Test suite
│   ├── conftest.py                  # Shared fixtures (in-memory SQLite)
│   ├── test_api/test_routes.py      # 20+ API integration tests
│   ├── test_filters/test_engine.py  # UrlMatcher + EasyList parser tests
│   ├── test_ml/test_classifier.py   # Feature extractor + classifier tests
│   └── test_database/test_repos.py  # Repository unit tests
│
├── docs/
│   ├── architecture.md              # Architecture diagram
│   ├── installation.md              # Detailed installation guide
│   ├── deployment.md                # Build & deploy for all browsers
│   └── api_reference.md             # REST API reference
│
├── environment.yml                  # Anaconda environment (Python 3.11)
├── setup.py                         # Python package setup
├── run.py                           # Backend entry point
├── setup_and_test.bat               # One-click setup helper (Windows)
├── .env.example                     # Environment variable template
└── LICENSE                          # MIT License
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/DzCodeProgrammer/Ads-Blocker.git
cd Ads-Blocker

# 2. Install dependencies
pip install fastapi "uvicorn[standard]" httpx sqlalchemy pydantic \
    pydantic-settings python-dotenv slowapi tldextract apscheduler \
    aiofiles scikit-learn numpy pandas joblib Pillow requests

# 3. Configure
cp .env.example .env

# 4. Generate icons
python extension/assets/icons/generate_icons.py

# 5. Train ML model (optional but recommended)
python -m ml_engine.trainer

# 6. Start backend
python run.py
# → Running on http://127.0.0.1:8765
# → API docs at http://127.0.0.1:8765/docs

# 7. Load extension in Chrome
# chrome://extensions/ → Developer mode → Load unpacked → select extension/
```

> **Windows users:** Double-click `setup_and_test.bat` to run steps 2–6 automatically.

---

## Installation

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | 3.13 also tested |
| pip | latest | included with Python |
| Chrome / Edge | 88+ | Manifest V3 support |
| Firefox | 109+ | Manifest V3 support |

### With Anaconda (Recommended)

```bash
# Create isolated environment
conda env create -f environment.yml
conda activate adblocker

# Verify
python --version   # Python 3.11.x
```

### With pip (Python 3.11+)

```bash
pip install -r requirements.txt
# or use setup.py
pip install -e ".[dev]"
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8765
APP_SECRET_KEY=your-strong-secret-key-here

DATABASE_URL=sqlite:///./adblocker.db

EASYLIST_URL=https://easylist.to/easylist/easylist.txt
EASYPRIVACY_URL=https://easylist.to/easylist/easyprivacy.txt
UBLOCK_URL=https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt

FILTER_UPDATE_INTERVAL=24
RATE_LIMIT_PER_MINUTE=120
ML_CONFIDENCE_THRESHOLD=0.75
LOG_LEVEL=INFO
```

---

## Running the Backend

```bash
# Development mode (auto-reload on file changes)
APP_ENV=development python run.py

# Production mode
APP_ENV=production python run.py
```

Output:
```
INFO  AdBlocker backend starting up
INFO  Engine loaded 0 rules from DB
INFO  Filter scheduler started — interval=24h
INFO  Uvicorn running on http://127.0.0.1:8765
```

**First run — download filter lists:**
```bash
curl -X POST http://127.0.0.1:8765/api/filters/update
# or via popup → Lists tab → "Update All Lists"
```

**API Documentation:** http://127.0.0.1:8765/docs (development only)

---

## Loading the Extension

### Chrome / Microsoft Edge

1. Open `chrome://extensions/` (or `edge://extensions/`)
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the `extension/` folder
5. Note your **Extension ID** (e.g. `abcdef1234...`)
6. Add it to `.env`:
   ```
   CORS_ORIGINS=chrome-extension://YOUR_EXTENSION_ID_HERE
   ```
7. Restart backend

### Firefox

1. Open `about:debugging` → **This Firefox**
2. Click **Load Temporary Add-on**
3. Select `extension/manifest.json`

> Note: Firefox temporary add-ons are removed on browser restart. For permanent install, sign via `web-ext sign`.

---

## API Reference

Base URL: `http://127.0.0.1:8765`

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Backend health check |
| `POST` | `/api/filters/check` | Check if URL should be blocked |
| `GET` | `/api/filters` | List active filter rules |
| `POST` | `/api/filters` | Add custom rule |
| `DELETE` | `/api/filters/{id}` | Deactivate rule |
| `POST` | `/api/filters/update` | Trigger remote list update |
| `GET` | `/api/stats/summary` | Total blocked, today, trackers, rules count |
| `GET` | `/api/stats/top-domains` | Most-blocked domains |
| `GET` | `/api/stats/daily` | Per-day statistics |
| `GET` | `/api/stats/breakdown` | Rules by filter list |
| `GET` | `/api/settings` | Get user settings |
| `PUT` | `/api/settings` | Update settings |
| `GET` | `/api/whitelist` | List whitelisted domains |
| `POST` | `/api/whitelist` | Add domain to whitelist |
| `DELETE` | `/api/whitelist/{id}` | Remove from whitelist |
| `GET` | `/api/logs` | Recent request log |
| `POST` | `/api/logs/record` | Record a log entry |
| `DELETE` | `/api/logs` | Clear log |
| `GET` | `/api/site-settings` | List per-site settings |
| `PUT` | `/api/site-settings/{domain}` | Set blocking mode for domain |
| `DELETE` | `/api/site-settings/{domain}` | Reset domain to default |
| `GET` | `/api/lists` | List filter list subscriptions |
| `POST` | `/api/lists` | Subscribe to new filter list |
| `PUT` | `/api/lists/{id}` | Enable/disable a list |
| `POST` | `/api/lists/{id}/update` | Update a specific list |
| `GET` | `/api/export/rules` | Export custom rules as EasyList text |
| `POST` | `/api/export/import` | Import EasyList rules |
| `GET` | `/api/scriptlets` | List available scriptlets |
| `POST` | `/api/scriptlets/bundle` | Get scriptlet bundle for a domain |

### Example: Check URL

```bash
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ads.doubleclick.net/pixel.gif", "enable_ml": true}'
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
  "cname_real_domain": null
}
```

---

## ML Engine

The ML engine uses a **Random Forest classifier** trained on 20 URL-derived features:

| Feature Category | Features |
|-----------------|----------|
| **Lexical** | URL length, entropy, domain length, path length, query length |
| **Domain** | Subdomain depth, digit ratio, eTLD type, suspicious TLD |
| **Path** | Path depth, file extension, query param count |
| **Keywords** | Ad/tracker keyword count in domain + path |
| **Signals** | Has IP address, has port, redirect params, hyphen count |

### Training the Model

```bash
# With your own data (CSV with 'url' and 'label' columns):
# label: 1 = ad/tracker, 0 = benign
python -m ml_engine.trainer

# Synthetic data is auto-generated if no CSV exists
# Model saved to: ml_engine/data/model.joblib
```

### Scriptlets Available

| Scriptlet | Purpose |
|-----------|---------|
| `anti-adblock-killer` | Defeat adblock detectors (window.adblock = fake object) |
| `abort-on-property-read` | Prevent scripts from reading specific window properties |
| `abort-on-property-write` | Prevent scripts from writing specific window properties |
| `no-setTimeout-if` | Block specific setTimeout callbacks by content match |
| `no-setInterval-if` | Block specific setInterval callbacks by content match |
| `no-fetch-if` | Block fetch() to URLs matching a pattern |
| `no-xhr-if` | Block XMLHttpRequest to URLs matching a pattern |
| `set-constant` | Force a window property to a constant value |
| `remove-class` | Remove CSS classes added by ad scripts |
| `no-webrtc` | Block WebRTC to prevent IP leaks via STUN |
| `no-notification-if` | Auto-deny Web Push notification requests |
| `cookie-remover` | Remove tracking cookies |
| `noeval` | Neutralize eval() used for adblock detection |
| `youtube-ad-skip` | Auto-skip YouTube ads and remove banners |

---

## Filter Lists

8 built-in filter lists, loaded on first run:

| List | Category | Description |
|------|----------|-------------|
| **EasyList** | Ads | Primary international ad filter — 70k+ rules |
| **EasyPrivacy** | Privacy | Removes all tracking forms — 30k+ rules |
| **uBlock Filters** | Ads | uBlock Origin's own filters |
| **uBlock Privacy** | Privacy | uBlock Origin privacy filters |
| **Peter Lowe's List** | Ads | Ad/tracking server list |
| **Fanboy's Annoyance** | Annoyances | Social media, popups, annoyances |
| **Cookie AutoDelete** | Cookies | Cookie consent banners |
| **NoCoin** | Malware | Cryptominer scripts |

Subscribe to additional lists via popup **Lists** tab or API:

```bash
curl -X POST http://127.0.0.1:8765/api/lists \
  -H "Content-Type: application/json" \
  -d '{"name": "My Custom List", "url": "https://example.com/filters.txt", "category": "custom"}'
```

---

## Configuration

All settings configurable via `.env` or the popup **Options** tab:

| Setting | Default | Description |
|---------|---------|-------------|
| `APP_ENV` | `development` | `development` or `production` |
| `APP_PORT` | `8765` | Backend port |
| `APP_SECRET_KEY` | *(required)* | Change in production |
| `FILTER_UPDATE_INTERVAL` | `24` | Hours between auto-updates |
| `RATE_LIMIT_PER_MINUTE` | `120` | API rate limit |
| `ML_CONFIDENCE_THRESHOLD` | `0.75` | ML block threshold (0–1) |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### Per-Site Blocking Modes

Set via popup **Overview** tab or `PUT /api/site-settings/{domain}`:

| Mode | Behavior |
|------|----------|
| **Normal** | Standard blocking (ad domains + trackers) |
| **Aggressive** | Block all 3rd-party scripts, XHR, and frames |
| **Disabled** | No blocking on this domain |

---

## Testing

```bash
# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=backend --cov=ml_engine --cov-report=html
# Open htmlcov/index.html for full coverage report

# Run specific test file
pytest tests/test_filters/test_engine.py -v
pytest tests/test_api/test_routes.py -v
```

### Test API Manually

```bash
# Health check
curl http://127.0.0.1:8765/health

# Block an ad URL
curl -X POST http://127.0.0.1:8765/api/filters/check \
  -H "Content-Type: application/json" \
  -d '{"url":"https://ads.doubleclick.net/ad.js","enable_ml":false}'

# Get statistics
curl http://127.0.0.1:8765/api/stats/summary

# Get scriptlet bundle for youtube.com
curl -X POST http://127.0.0.1:8765/api/scriptlets/bundle \
  -H "Content-Type: application/json" \
  -d '{"domain":"youtube.com","include_defaults":true}'
```

---

## Security

- **Input validation** — All inputs validated via Pydantic (URL scheme, domain format, pattern characters)
- **Rate limiting** — 120 requests/minute via `slowapi`
- **Security headers** — `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `X-XSS-Protection`
- **CORS** — Only extension origins allowed (configured in `.env`)
- **SQLite WAL mode** — Concurrent reads without write locks
- **No eval/exec** — Extension CSP: `script-src 'self'`
- **Declarative blocking** — No arbitrary JS in request path (MV3 DNR engine)

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Follow PEP8 + type hints for Python, ESLint rules for JavaScript
4. Add tests for new backend functionality
5. Run `pytest tests/ -v` before submitting
6. Open a Pull Request with a clear description

### Code Standards

- **Python**: PEP8, type hints, Black formatting, no bare excepts
- **JavaScript**: ESM modules, `'use strict'`, no inline styles in JS
- **Architecture**: Clean Architecture layers (routes → services → engine → repos)
- **SOLID**: Single responsibility per class, dependency injection via FastAPI `Depends`

---

## Changelog

### v2.1.0 — MV3 Compliance Fix
- **Fix:** Replace `webRequest` blocking with `declarativeNetRequest` (DNR) dynamic rules
- Chrome MV3 no longer allows `['blocking']` flag for regular extensions
- 35 built-in tracker domains always loaded as DNR rules

### v2.0.0 — Major Feature Expansion
- Element Picker (uBlock Origin-style click-to-block)
- Cookie Banner Auto-Dismisser (40+ CMPs)
- Social Widget Blocker (Facebook, Twitter, YouTube, TikTok, etc.)
- YouTube Ad Skipper
- Notification Blocker
- Scriptlet Engine (14 built-in scriptlets)
- CNAME Uncloaking via DNS-over-HTTPS
- URL Tracking Parameter Cleaner (60+ params)
- Network Request Logger (real-time)
- Per-Site Mode (Off/Normal/Aggressive)
- Filter List Manager (8 built-in lists)
- Import/Export custom rules
- Fingerprint Detector (ML)
- Behavioral Analyzer (ML)
- Popup UI redesigned (5 tabs)

### v1.0.0 — Initial Release
- FastAPI backend with SQLite
- EasyList parser + URL matcher
- ML classifier (Random Forest)
- APScheduler auto-updates
- Basic popup with stats dashboard
- Chrome/Edge/Firefox support

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License — Copyright (c) 2026 DzCodeProgrammer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">

Made with Python, FastAPI, and Machine Learning

[GitHub](https://github.com/DzCodeProgrammer/Ads-Blocker) · [Issues](https://github.com/DzCodeProgrammer/Ads-Blocker/issues) · [MIT License](LICENSE)

</div>
