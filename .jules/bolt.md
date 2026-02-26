## 2025-05-27 - AppSetting Request-Level Caching
**Learning:** `AppSetting.get()` was causing N+1 queries because it fetched from the DB on every call. Simple request-level caching using `flask.g` (and checking `has_app_context()`) is highly effective for configuration data that is read frequently but rarely changes within a request.
**Action:** Always check frequently accessed "static" configuration helpers for potential N+1 issues and implement `flask.g` caching.
