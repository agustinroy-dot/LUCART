
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2026-04-01 - Request-Level Settings Caching
**Learning:** Application settings fetched individually in a loop or multiple times per request create N+1 query patterns. Caching them using `flask.g` within the application context eliminates redundant DB hits. However, ensure `has_app_context()` is checked before accessing `flask.g` so that the model doesn't crash during CLI operations or tests. Additionally, updating `flask.g` requires careful initialization handling (`hasattr`) when setting new values to avoid incomplete caches.
**Action:** When implementing `flask.g` based caching, explicitly wrap logic in `has_app_context()` and verify proper cache population in setter methods if the cache hasn't been instantiated yet.
