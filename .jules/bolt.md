
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-14 - Optimize CSV Export Memory Footprint
**Learning:** Returning large datasets via `io.StringIO` and `.all()` loads the entire table into memory before generating the response. This causes substantial peak memory usage and possible Out-Of-Memory exceptions on large datasets.
**Action:** When exporting large data files (like CSV), use Flask's `stream_with_context` with a Python generator that yields chunks, combined with SQLAlchemy's `yield_per()` to load and discard rows iteratively, significantly lowering the memory footprint.
