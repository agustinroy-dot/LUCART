
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2023-10-27 - [N+1 Query Issue with SQLAlchemy dynamic relationships]
**Learning:** `lazy='dynamic'` on SQLAlchemy relationships prevents eager loading (e.g., using `joinedload`). To solve N+1 query issues in Jinja templates that iterate over relationship items, the relationships must be changed to `lazy='select'` to allow the `joinedload` option to take effect. Further, any template checks utilizing `.count()` on a dynamic relationship must be updated to use the `|length` filter (e.g., `model.items|length > 0`) because `lazy='select'` returns a list rather than a query object.
**Action:** When migrating SQLAlchemy relationships from `lazy='dynamic'` to `lazy='select'` to fix N+1 queries, verify all connected Jinja templates and Python views to replace `.count()` with Python `len()` or Jinja `|length` to prevent breaking changes.
