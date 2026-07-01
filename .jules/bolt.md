
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [AppSetting N+1 Query Cache]
**Learning:** Calling `AppSetting.get()` repeatedly in routes (like the calculator and settings views) executes multiple identical database queries, creating an N+1 query pattern for configuration keys.
**Action:** Implemented a request-level cache using `flask.g` in `AppSetting`. Always pre-warm configuration caches with a single query using methods like `get_all()` at the start of routes that read multiple settings, reducing database hits to zero for subsequent gets within the request.
