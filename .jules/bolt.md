
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-14 - Fix N+1 Query in Order View
**Learning:** In Flask/SQLAlchemy applications, using `lazy='dynamic'` on model relationships breaks the ability to use `joinedload` eager-loading optimizations in routes. When templates iterate over these relationships, an O(N) query bottleneck occurs.
**Action:** Change `lazy='dynamic'` to `lazy='select'` to enable `.options(joinedload(...))` optimizations. Additionally, when using `lazy='select'`, update any connected Jinja templates that previously used `.count()` on the relationship query to use the `|length` filter instead.
