## 2024-05-24 - N+1 Query in Quotes Index
**Learning:** The quotes index route loops over quotes and accesses `quote.customer.name` without eager loading `Quote.customer`, causing an N+1 query problem. This is a common performance bottleneck in SQLAlchemy relationships when rendering templates.
**Action:** Used `joinedload(Quote.customer)` to eagerly load the customer relationship in the `index` route of `app/quotes/routes.py` to fetch all necessary data in a single query.
