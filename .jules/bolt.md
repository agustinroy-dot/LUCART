
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2026-05-18 - AppSetting Cache Initialization
**Learning:** When implementing request-level caching (like `AppSetting` configuration) using `flask.g`, do not use truthiness (e.g., `if cache:`) to verify cache initialization. If the DB is empty, the cache will evaluate to `False` and bypass the cache check entirely, falling back to N+1 direct DB queries for missing settings.
**Action:** Use `hasattr(g, 'cache_name')` or a dedicated flag in `g` (e.g., `g.app_settings_fully_loaded`) to determine if the cache logic has run.
