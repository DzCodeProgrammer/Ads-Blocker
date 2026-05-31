# Panduan Build & Deploy Extension

## Build Extension untuk Chrome / Edge

### 1. Pastikan icons tersedia

```bash
conda activate adblocker
python extension/assets/icons/generate_icons.py
```

### 2. Load di Chrome (Developer Mode)

1. Buka `chrome://extensions/`
2. Aktifkan **Developer mode** (toggle kanan atas)
3. Klik **Load unpacked**
4. Pilih folder: `C:\Users\Extensions and Others Project\Ads-Blocker\extension`
5. Extension muncul di toolbar

### 3. Load di Microsoft Edge

1. Buka `edge://extensions/`
2. Aktifkan **Developer mode**
3. Klik **Load unpacked**
4. Pilih folder yang sama

### 4. Salin Extension ID

Setelah load, catat **Extension ID** (contoh: `abcdefghijklmnopqrstuvwxyz123456`)

Update `.env`:
```
CORS_ORIGINS=chrome-extension://EXTENSION_ID_ANDA
```

Restart backend: `python run.py`

---

## Build Extension untuk Firefox

Firefox menggunakan Manifest V3 (dukungan penuh sejak Firefox 109).

### 1. Buat web-ext (opsional, untuk packaging)

```bash
npm install -g web-ext
cd extension/
web-ext build --source-dir . --artifacts-dir ../dist/firefox/
```

### 2. Load sementara di Firefox

1. Buka `about:debugging`
2. Klik **This Firefox** → **Load Temporary Add-on**
3. Pilih file: `extension/manifest.json`

### 3. Perbedaan Firefox vs Chrome

| Fitur | Chrome/Edge | Firefox |
|-------|-------------|---------|
| Service Worker | `background.js` (module) | Sama |
| `webRequest` blocking | Butuh `declarativeNetRequest` di MV3 | `webRequest` blocking masih didukung |
| Extension ID prefix | `chrome-extension://` | `moz-extension://` |

---

## Packaging untuk Distribusi

### Chrome Web Store

```bash
# Buat ZIP (tanpa folder .git, docs, backend, tests, ml_engine)
cd "C:\Users\Extensions and Others Project\Ads-Blocker"
powershell Compress-Archive -Path extension\* -DestinationPath dist\adblocker-chrome.zip
```

Upload di: https://chrome.google.com/webstore/devconsole

### Firefox Add-ons (AMO)

```bash
web-ext sign --api-key=USER:API_KEY --api-secret=API_SECRET
```

---

## Deployment Backend (Production)

### Sebagai Windows Service (NSSM)

```bash
# Download NSSM: https://nssm.cc/download
nssm install AdBlockerBackend "C:\anaconda3\envs\adblocker\python.exe"
nssm set AdBlockerBackend AppParameters "C:\Users\Extensions and Others Project\Ads-Blocker\run.py"
nssm set AdBlockerBackend AppDirectory "C:\Users\Extensions and Others Project\Ads-Blocker"
nssm start AdBlockerBackend
```

### Environment Variables Production

```
APP_ENV=production
APP_SECRET_KEY=<random-256-bit-key>
LOG_LEVEL=WARNING
```

---

## Update Filter Lists Otomatis

Filter diperbarui otomatis setiap 24 jam (dikonfigurasi via `FILTER_UPDATE_INTERVAL`).
Untuk mengubah interval:
```
# .env
FILTER_UPDATE_INTERVAL=12   # setiap 12 jam
```
