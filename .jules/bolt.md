
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [AppSetting N+1 Configuration Queries]
**Learning:** Calling `AppSetting.get()` repeatedly within a single request (e.g., in a route calculating multiple rates) triggers a separate database query for each setting.
**Action:** Implement request-level caching using Flask's `g` context object. Cache initialization in `get_all()` should fetch all settings in one query and populate `g`. `set()` operations must mutate the cache to prevent stale reads within the same request lifecycle. Always add comments in the codebase explaining optimizations.
