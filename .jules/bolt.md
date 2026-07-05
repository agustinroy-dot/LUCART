
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-18 - [View Routes N+1 Query]
**Learning:** Found N+1 query issues in view routes (`/app/quotes/routes.py` and `/app/orders/routes.py`) where relationships (like `items`, `materials`, `customer`) were lazy-loaded dynamically and then accessed in templates and loops.
**Action:** Change `lazy='dynamic'` to default (select) on relationships and explicitly eager-load them in the route's SQL query using `joinedload`. Remember to update associated templates (e.g., replacing `.count()` with `|length`).
