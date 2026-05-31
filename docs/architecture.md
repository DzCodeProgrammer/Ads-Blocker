# Arsitektur AdBlocker Pro

## Diagram Komponen

```
┌─────────────────────────────────────────────────────────────────┐
│                     BROWSER (Chrome/Edge/Firefox)               │
│                                                                 │
│  ┌─────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │   popup/    │    │   background/    │    │content_scripts│  │
│  │  popup.html │◄──►│  background.js   │    │  content.js   │  │
│  │  popup.js   │    │  request_handler │    │cosmetic_filter│  │
│  │  popup.css  │    │       .js        │    └───────────────┘  │
│  └─────────────┘    └────────┬─────────┘           │           │
│                              │ HTTP/REST            │ DOM       │
└──────────────────────────────┼──────────────────────┼───────────┘
                               │                      │
                   ┌───────────▼──────────────────────┘
                   │          PYTHON BACKEND
                   │     (FastAPI · Port 8765)
                   │
                   │  ┌─────────────────────────────┐
                   │  │         API Layer            │
                   │  │  /api/filters  (check, CRUD) │
                   │  │  /api/stats    (dashboard)   │
                   │  │  /api/settings (toggle/pref) │
                   │  │  /api/whitelist (domain mgmt)│
                   │  └──────────────┬──────────────┘
                   │                 │
                   │  ┌──────────────▼──────────────┐
                   │  │       Service Layer          │
                   │  │  BlockingService             │
                   │  │  StatsService                │
                   │  │  UpdateService (APScheduler) │
                   │  └──────────────┬──────────────┘
                   │                 │
                   │  ┌──────────────▼──────────────┐
                   │  │      Filter Engine           │
                   │  │  EasyListParser              │
                   │  │  UrlMatcher (O(1) lookup)    │
                   │  │  FilterEngine                │
                   │  └──────────────┬──────────────┘
                   │                 │
                   │  ┌──────────────▼──────────────┐
                   │  │        ML Engine             │
                   │  │  FeatureExtractor            │
                   │  │  AdClassifier (RandomForest) │
                   │  │  AdPredictor                 │
                   │  └──────────────┬──────────────┘
                   │                 │
                   │  ┌──────────────▼──────────────┐
                   │  │    Database Layer (SQLite)   │
                   │  │  FilterRepository            │
                   │  │  StatsRepository             │
                   │  │  Models: FilterRule,         │
                   │  │          BlockedRequest,     │
                   │  │          UserSettings        │
                   │  └─────────────────────────────┘
                   │
                   │  ┌─────────────────────────────┐
                   │  │   External Filter Lists      │
                   │  │  EasyList (easylist.txt)     │
                   │  │  EasyPrivacy                 │
                   │  │  uBlock Origin Filters       │
                   │  └─────────────────────────────┘
                   └───────────────────────────────────
```

---

## Alur Request Blocking

```
Browser request
       │
       ▼
background.js (onBeforeRequest)
       │
       ├── Cache hit? → BLOCK immediately → record to backend async
       │
       └── No cache → POST /api/filters/check
                             │
                             ▼
                    FilterEngine.check_url()
                             │
                    ┌────────┴────────┐
                    │                 │
              UrlMatcher          ML Predictor
              (O(1) domain set    (RandomForest)
               + suffix trie      score ≥ threshold?
               + regex)                │
                    │                 │
                    └────────┬────────┘
                             │
                       blocked? YES
                             │
                    StatsRepository.record()
                             │
                    return { blocked: true }
                             │
                             ▼
                    background.js → { cancel: true }
                             │
                    Add domain to in-memory cache
```

---

## Stack Teknologi

| Lapisan | Teknologi | Alasan |
|---------|-----------|--------|
| Backend | Python 3.11 + FastAPI | Async I/O, type hints, automatic OpenAPI |
| Database | SQLite + SQLAlchemy 2.0 | Zero-config, embedded, cukup untuk local use |
| Scheduler | APScheduler | Battle-tested, async-compatible |
| ML | scikit-learn RandomForest | Interpretable, fast inference, no GPU needed |
| Feature Engineering | tldextract + custom | Domain-aware URL parsing |
| Extension | Manifest V3 | Standard terbaru Chrome/Edge/Firefox |
| Testing | pytest + TestClient | Fast, isolated, no real HTTP server needed |

---

## Prinsip Desain

- **Clean Architecture**: UI → Service → Domain → Infrastructure (satu arah)
- **SOLID**: setiap class satu tanggung jawab; injeksi dependensi via FastAPI Depends
- **Fail Open**: jika backend tidak merespons, request TIDAK diblokir (UX > keamanan di sini)
- **Cache-first**: UrlMatcher di-build sekali di memori — tidak ada DB query per request
- **Type Safety**: semua Python di-annotate, Pydantic models untuk validasi input
