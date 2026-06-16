
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-19 - [Cache Route Warming Redundancy]
**Learning:** Explicitly calling `AppSetting.get_all()` inside route handlers to "warm" the cache is redundant if the `AppSetting.get()` method is already designed to initialize the cache transparently on its first invocation.
**Action:** Keep caching logic fully encapsulated within the data model. Avoid bleeding implementation details (like manual cache warming) into route controllers unless absolutely necessary for bulk-fetch optimizations where the getter doesn't inherently handle initialization.
