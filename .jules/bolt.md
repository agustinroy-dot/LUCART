## 2024-05-14 - AppSetting Request-Level Caching
**Learning:** The `AppSetting` model is queried multiple times per request in some routes (e.g., `app/quotes/routes.py` and `app/settings/routes.py`). Each call to `AppSetting.get()` executes a separate database query.
**Action:** Implement a request-level cache (using `flask.g`) in `AppSetting.get()` and `AppSetting.set()` to load all settings at once and prevent multiple identical or unnecessary queries during a single request lifecycle.
