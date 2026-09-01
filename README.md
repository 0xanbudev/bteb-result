# bteb-result

> bteb.anbuinfosec.dev public stats updater.

[![Auto Update](https://img.shields.io/badge/Auto%20Update-Every%2025%20Days-blue)](https://bteb.anbuinfosec.dev)
[![API Status](https://img.shields.io/badge/API-Live-brightgreen)](https://bteb.anbuinfosec.dev/api/stats/public)

---

## 📊 Live Public Stats (Auto Updated Every 25 Days)

<!-- STATS:START -->
| Metric | Value |
|--------|--------|
| Database Connected | Yes |
| Total Students | 225,329 |
| Total Institutes | 915 |
| Total Passed | 123,620 |
| Total Referred | 107,454 |
| Pass Percentage | 54.86% |
| Refer Percentage | 47.69% |
| Last Result Published | 1 September 2026, 02:28 AM BST |
<!-- STATS:END -->

---

## 🔌 Public API Endpoints

<!-- API:START -->
### GET /api/stats/public

Returns aggregated public statistics.

**Response:**

```json
{
  "success": true,
  "data": {
    "connected": true,
    "studentCount": 225329,
    "instituteCount": 915,
    "passCount": 123620,
    "refCount": 107454,
    "passPercentage": 54.86,
    "refPercentage": 47.69,
    "lastResultPublished": "2026-08-31T20:28:38.880Z"
  }
}
```
<!-- API:END -->

---

## 📈 Live Stats Graph

<!-- CHART:START -->
![BTEB Live Stats Graph](chart.svg)
<!-- CHART:END -->

---

## 🕐 Last Updated

<!-- UPDATED:START -->
| Field | Value |
|-------|-------|
| Last Auto-Update | 1 September 2026, 08:39 AM BST |
| Update Frequency | Every 30 minutes |
| Timezone | Asia/Dhaka (BST, UTC+6) |
<!-- UPDATED:END -->

---

> Auto-updated every 30 minutes via GitHub Actions. Powered by [bteb.anbuinfosec.dev](https://bteb.anbuinfosec.dev).
