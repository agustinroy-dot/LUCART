
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [AppSetting N+1 Query Cache]
**Learning:** Calling `AppSetting.get()` repeatedly in routes (e.g., quotes calculator, settings index) triggers multiple separate database queries for individual keys, creating an N+1 query problem. Implementing request-level caching using `flask.g` allows batching these queries into a single `get_all()` call, improving performance from ~1.9s to ~0.01s for heavy loops.
**Action:** Always consider using request-level caches like `flask.g` when accessing configurations or settings multiple times per request, but remember to wrap accesses in `has_app_context()` to gracefully handle CLI or testing contexts. Ensure to prepopulate cache early in routes making many reads.
