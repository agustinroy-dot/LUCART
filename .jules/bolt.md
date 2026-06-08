
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [Streaming Large CSV Exports]
**Learning:** Found an OOM vulnerability in `app/settings/routes.py` where `/export/<type>` fetched all records at once (`Query.all()`) into an in-memory `io.StringIO` buffer, crashing on large datasets and consuming ~86MB for 50,000 rows.
**Action:** Replaced `.all()` with a Python generator using `yield_per(1000)` and Flask's `stream_with_context()`. Always use streaming generators for bulk data exports to keep peak memory minimal (~3.5MB peak).
