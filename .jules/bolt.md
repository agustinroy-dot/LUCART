
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-19 - [Order Relationships N+1 Query]
**Learning:** Eager loading (`joinedload`) with relationships that have `lazy='dynamic'` doesn't work out of the box in SQLAlchemy 1.4/2.0 without changing them to standard loading (list-like). But removing `lazy='dynamic'` breaks existing uses of `.count()` on that relationship in Jinja templates (since the relationship becomes a list, not a query).
**Action:** When removing `lazy='dynamic'` to optimize queries with `joinedload`, always audit the codebase for uses of `.count()`, `.filter()`, etc., on those relationships and change them appropriately (e.g., `.count()` -> `|length` in Jinja).
