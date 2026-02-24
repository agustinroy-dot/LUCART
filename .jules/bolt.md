## 2026-02-24 - Request-Level Caching for AppSettings
**Learning:** `AppSetting.get()` was executing a database query for every call, leading to N+1 issues when multiple settings were accessed in a single request (e.g., in templates or forms).
**Action:** Implemented request-level caching using `flask.g`. The first call fetches all settings (SELECT * FROM app_setting) and subsequent calls use the in-memory cache. This reduced 4 queries to 1 in key routes.
