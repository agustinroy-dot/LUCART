
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2026-06-06 - Optimize AppSetting database queries
**Learning:** `AppSetting.get` and `AppSetting.set` access the database for each call, leading to N+1 query patterns when multiple settings are fetched consecutively.
**Action:** Implemented request-level caching with `flask.g` inside `AppSetting.get` and `AppSetting.set` methods using a `get_all` initializer. This reduces multiple individual query calls to a single batch fetch per request.
