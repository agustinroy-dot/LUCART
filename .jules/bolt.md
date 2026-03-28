## 2024-03-28 - [Fix N+1 query in quotes index view]
**Learning:** Rendering attributes of SQLAlchemy relationships in Jinja loops triggers N+1 query problems if lazy-loaded. For example, `quote.customer.name` within an iteration loop fetched the `Customer` instance dynamically per `Quote`.
**Action:** Explicitly use `.options(joinedload(Model.relationship))` in the route's SQLAlchemy query for any relationships accessed within template loops to eager-load the data and prevent N+1 queries.
