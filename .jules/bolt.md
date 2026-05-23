
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-19 - [AppSetting N+1 Query Fix]
**Learning:** `AppSetting.get` called sequentially inside routes resulted in an N+1 database query scenario because each individual key lookup triggered a new query (e.g. 4 settings = 4 DB queries). By implementing a request-level cache using `flask.g` inside the `AppSetting` model, we can pre-warm the cache with `AppSetting.get_all()` (using `has_app_context()`), reducing the operation to a single query per request.
**Action:** Always consider using `flask.g` for global, request-scoped configurations or settings to prevent redundant database lookups.
