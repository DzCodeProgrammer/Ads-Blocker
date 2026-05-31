# Panduan Instalasi AdBlocker Pro

## Prasyarat

- **Anaconda / Miniconda** — [Download](https://www.anaconda.com/download)
- **Python 3.11+**
- **Browser**: Chrome 88+, Edge 88+, atau Firefox 109+
- **OS**: Windows 10/11, macOS 12+, Ubuntu 20.04+

---

## 1. Setup Anaconda Environment

```bash
# Clone / ekstrak project ke folder pilihan
cd "C:\Users\Extensions and Others Project\Ads-Blocker"

# Buat environment dari file
conda env create -f environment.yml

# Aktifkan environment
conda activate adblocker

# Verifikasi Python
python --version   # Harus: Python 3.11.x
```

---

## 2. Konfigurasi Environment Variables

```bash
# Salin template
cp .env.example .env

# Edit sesuai kebutuhan (minimal: APP_SECRET_KEY)
# Windows:
notepad .env
```

Nilai penting di `.env`:

| Key | Default | Keterangan |
|-----|---------|------------|
| `APP_PORT` | `8765` | Port backend (pastikan tidak dipakai) |
| `APP_SECRET_KEY` | (wajib ganti) | Kunci rahasia API |
| `ML_CONFIDENCE_THRESHOLD` | `0.75` | Ambang skor ML (0–1) |

---

## 3. Inisialisasi Database

Database SQLite dibuat otomatis saat pertama kali backend dijalankan.

```bash
conda activate adblocker
python run.py
# Backend akan membuat adblocker.db secara otomatis
```

---

## 4. Train ML Model (Opsional tapi Direkomendasikan)

```bash
conda activate adblocker
python -m ml_engine.trainer
# Model disimpan di: ml_engine/data/model.joblib
# Training data sintetis dibuat otomatis jika tidak ada
```

Untuk menggunakan data training nyata, letakkan file CSV di `ml_engine/data/training_data.csv` dengan format:
```
url,label
https://ads.doubleclick.net/pixel,1
https://github.com/user/repo,0
```

---

## 5. Generate Icons Extension

```bash
conda activate adblocker
pip install Pillow
python extension/assets/icons/generate_icons.py
# Menghasilkan: icon16.png, icon48.png, icon128.png
```

---

## 6. Menjalankan Backend

```bash
conda activate adblocker
python run.py
```

Output yang diharapkan:
```
INFO  AdBlocker backend starting up
INFO  Engine loaded N rules from DB
INFO  Filter scheduler started — interval=24h
INFO  Uvicorn running on http://127.0.0.1:8765
```

API dokumentasi tersedia di: http://127.0.0.1:8765/docs

---

## 7. Update Filter Lists (Pertama Kali)

Setelah backend berjalan, trigger update manual:

```bash
curl -X POST http://127.0.0.1:8765/api/filters/update
```

Atau lewat popup extension → tab Advanced → "Update Filter Lists"

---

## 8. Menjalankan Tests

```bash
conda activate adblocker
pytest tests/ -v --cov=backend --cov=ml_engine --cov-report=html
# Report HTML di: htmlcov/index.html
```

---

## Troubleshooting

**Port 8765 sudah dipakai:**
```bash
# Ganti di .env
APP_PORT=8766
```

**ModuleNotFoundError:**
```bash
# Pastikan environment aktif dan install ulang
conda activate adblocker
pip install -e .
```

**Backend tidak terhubung dari extension:**
- Pastikan `python run.py` berjalan di terminal terpisah
- Cek CORS di `.env`: tambahkan ID extension Chrome Anda ke `CORS_ORIGINS`
- Untuk development: set `CORS_ORIGINS=*` sementara
