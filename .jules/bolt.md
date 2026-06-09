
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-06-09 - [Stream CSV Exports]
**Learning:** Returning large datasets synchronously via `csv.writer` accumulating in a `StringIO` object causes massive memory spikes because all rows are held in memory before the request returns. By replacing `query.all()` with `query.yield_per(100)` and pairing it with a Python generator passed to Flask's `stream_with_context`, we can stream data out in chunks without holding the full dataset in memory.
**Action:** Always stream file exports natively in Flask using generators and `yield_per()` to ensure backend performance scales securely regardless of database table size.
