
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [AppSetting Flask.g Request Cache]
**Learning:** When retrieving application settings dynamically during request lifecycles (like in calculators or setting screens), repeated queries to `AppSetting.get()` cause N+1 query patterns. Caching these into a `flask.g` dictionary per-request (warming it once via `get_all()`) eliminates duplicate queries.
**Action:** Implement request-level caching with `flask.g` for repeated global configuration checks within templates or loops, ensuring caching is wrapped safely with `has_app_context()`.
