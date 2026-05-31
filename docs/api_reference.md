# API Reference

Base URL: `http://127.0.0.1:8765`

Dokumentasi interaktif (Swagger): `http://127.0.0.1:8765/docs`

---

## Health

### GET /health
Cek status backend.

**Response:**
```json
{ "status": "ok", "version": "1.0.0" }
```

---

## Filters

### POST /api/filters/check
Cek apakah URL harus diblokir.

**Request:**
```json
{
  "url": "https://ads.doubleclick.net/pixel.gif",
  "tab_url": "https://news.com/article",
  "enable_ml": true
}
```

**Response:**
```json
{
  "url": "https://ads.doubleclick.net/pixel.gif",
  "domain": "ads.doubleclick.net",
  "blocked": true,
  "matched_rule": "doubleclick.net",
  "is_tracker": true,
  "ml_blocked": false,
  "ml_confidence": null
}
```

### GET /api/filters
List semua rule aktif.

Query params: `rule_type` (blacklist | whitelist | easylist | easyprivacy | ublock | ml_detected)

### POST /api/filters
Tambah rule baru.

**Request:**
```json
{ "pattern": "bad-domain.com", "rule_type": "blacklist", "comment": "Manual block" }
```

### DELETE /api/filters/{id}
Nonaktifkan rule.

### POST /api/filters/update
Trigger update filter list dari remote (EasyList, EasyPrivacy, uBlock).

---

## Stats

### GET /api/stats/summary
```json
{
  "total_blocked": 15420,
  "blocked_today": 342,
  "tracker_blocked": 8901,
  "rules_count": 350000
}
```

### GET /api/stats/top-domains?limit=10
```json
[
  { "domain": "doubleclick.net", "count": 4521 },
  { "domain": "googlesyndication.com", "count": 3102 }
]
```

### GET /api/stats/daily?days=7
```json
[
  { "date": "2026-05-25", "count": 512 },
  { "date": "2026-05-26", "count": 489 }
]
```

### GET /api/stats/breakdown
```json
{ "blacklist": 1200, "easylist": 300000, "whitelist": 45 }
```

---

## Settings

### GET /api/settings
```json
{
  "is_enabled": true,
  "block_ads": true,
  "block_trackers": true,
  "block_malware": true,
  "enable_ml": true,
  "dark_mode": false,
  "show_counter": true
}
```

### PUT /api/settings
Partial update — kirim hanya field yang ingin diubah.
```json
{ "dark_mode": true, "enable_ml": false }
```

---

## Whitelist

### GET /api/whitelist
List domain yang di-whitelist.

### POST /api/whitelist
```json
{ "domain": "example.com" }
```

### DELETE /api/whitelist/{id}
Hapus domain dari whitelist.

---

## Error Responses

| Code | Keterangan |
|------|------------|
| 422 | Validasi gagal (URL tidak valid, pattern berbahaya) |
| 404 | Rule tidak ditemukan |
| 429 | Rate limit terlampaui |
| 500 | Server error |
