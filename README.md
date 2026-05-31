# AdBlocker Pro

Professional Ad Blocker Browser Extension — Python/Anaconda Backend + Manifest V3 Extension.

## Fitur

| Kategori | Fitur |
|----------|-------|
| **Blocking** | URL blacklist, EasyList, EasyPrivacy, uBlock filters |
| **Tracking** | 20+ tracker keyword heuristics |
| **ML** | Random Forest classifier (20 URL features) |
| **Cosmetic** | 25+ CSS selectors, MutationObserver untuk dynamic ads |
| **Anti-Fingerprint** | Canvas noise, AudioContext noise |
| **Dashboard** | Stats harian/mingguan, top domains, grafik bar |
| **Whitelist** | Per-domain whitelist management |
| **Dark Mode** | UI tema gelap/terang |
| **Auto Update** | Filter lists diperbarui otomatis (APScheduler) |
| **Multi-browser** | Chrome, Edge, Firefox (Manifest V3) |

---

## Quick Start

```bash
# 1. Setup environment
conda env create -f environment.yml
conda activate adblocker

# 2. Konfigurasi
cp .env.example .env
# Edit APP_SECRET_KEY di .env

# 3. Train ML model
python -m ml_engine.trainer

# 4. Generate icons
pip install Pillow
python extension/assets/icons/generate_icons.py

# 5. Jalankan backend
python run.py

# 6. Load extension di browser
#    Chrome/Edge: chrome://extensions/ → Load unpacked → pilih folder extension/
#    Firefox:     about:debugging → Load Temporary Add-on → pilih extension/manifest.json
```

---

## Struktur Proyek

```
Ads-Blocker/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app factory
│   │   ├── routes/
│   │   │   ├── filters.py       # /api/filters — check URL, CRUD rules
│   │   │   ├── stats.py         # /api/stats — dashboard data
│   │   │   ├── settings.py      # /api/settings — user preferences
│   │   │   └── whitelist.py     # /api/whitelist — whitelist management
│   │   └── middleware/
│   │       ├── rate_limiter.py  # slowapi rate limiting
│   │       └── security.py      # HTTP security headers
│   ├── filters/
│   │   ├── filter_engine.py     # Core engine, bridges DB + ML
│   │   ├── easylist_parser.py   # ABP/EasyList syntax parser
│   │   ├── url_matcher.py       # O(1) domain + suffix matching
│   │   └── updater.py           # Remote filter list downloader
│   ├── models/
│   │   ├── filter_rule.py       # ORM: FilterRule (blacklist/whitelist)
│   │   ├── blocked_request.py   # ORM: BlockedRequest (stats log)
│   │   └── settings.py          # ORM: UserSettings
│   ├── services/
│   │   ├── blocking_service.py  # Facade: check + record blocked requests
│   │   ├── stats_service.py     # Dashboard aggregation
│   │   └── update_service.py    # APScheduler wrapper
│   ├── database/
│   │   ├── db.py                # SQLAlchemy engine, session, init_db
│   │   └── repositories/
│   │       ├── filter_repo.py   # FilterRule DB operations
│   │       └── stats_repo.py    # BlockedRequest DB operations
│   └── config.py                # Pydantic Settings (env vars)
│
├── extension/                   # Manifest V3 Browser Extension
│   ├── manifest.json
│   ├── popup/
│   │   ├── popup.html           # Extension popup UI
│   │   ├── popup.js             # Stats, settings, whitelist UI logic
│   │   └── popup.css            # Light/dark theme CSS
│   ├── background/
│   │   ├── background.js        # Service worker entry point
│   │   └── request_handler.js   # webRequest interception + API calls
│   ├── content_scripts/
│   │   ├── content.js           # Cosmetic filter + anti-fingerprint
│   │   └── cosmetic_filter.js   # EasyList element-hide helper
│   └── assets/
│       └── icons/
│           └── generate_icons.py  # Icon generator (Pillow)
│
├── ml_engine/
│   ├── feature_extractor.py     # 20 URL features extraction
│   ├── classifier.py            # RandomForest pipeline + cross-val
│   ├── trainer.py               # Train script (python -m ml_engine.trainer)
│   ├── predictor.py             # Production predictor wrapper
│   └── data/
│       ├── training_data.csv    # (auto-generated if missing)
│       └── model.joblib         # (generated after training)
│
├── tests/
│   ├── conftest.py              # Shared fixtures (in-memory SQLite)
│   ├── test_api/test_routes.py  # FastAPI route integration tests
│   ├── test_filters/test_engine.py  # UrlMatcher + EasyListParser tests
│   ├── test_ml/test_classifier.py   # Feature extractor + classifier tests
│   └── test_database/test_repos.py  # Repository unit tests
│
├── docs/
│   ├── architecture.md          # Diagram arsitektur
│   ├── installation.md          # Panduan instalasi lengkap
│   ├── deployment.md            # Build extension & deployment
│   └── api_reference.md         # REST API reference
│
├── environment.yml              # Anaconda environment spec
├── .env.example                 # Environment variable template
├── setup.py                     # Python package setup
├── run.py                       # Entry point — start backend
└── README.md                    # File ini
```

---

## Dokumentasi Lengkap

- [Instalasi](docs/installation.md)
- [Arsitektur](docs/architecture.md)
- [Build & Deploy Extension](docs/deployment.md)
- [API Reference](docs/api_reference.md)

---

## Menjalankan Tests

```bash
conda activate adblocker
pytest tests/ -v --cov=backend --cov=ml_engine
```

---

## Keamanan

- Semua input divalidasi via Pydantic (pattern regex, URL scheme, domain format)
- Rate limiting 120 req/menit (dikonfigurasi via `RATE_LIMIT_PER_MINUTE`)
- Security headers: X-Frame-Options, X-Content-Type-Options, CSP
- CORS hanya izinkan origin extension yang valid
- SQLite dengan WAL mode + foreign keys enabled
- Tidak ada eval/exec — JavaScript CSP `script-src 'self'`

---

## License

MIT — Bebas digunakan dan dimodifikasi.
