
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-20 - [Order N+1 Query]
**Learning:** Found an N+1 query issue in the Order view route (`/app/orders/routes.py`) where the template accessed `order.customer`, `order.items`, and `order.materials` inside a loop, triggering a separate query for each item and material. The `lazy='dynamic'` property on relationships prevents `joinedload` eager loading from working.
**Action:** Always inspect Jinja template loops over database models for relationship accesses. If they are `lazy='dynamic'`, refactor to `lazy='select'` to allow `joinedload` eager loading in the route's SQL query. Note that changing `lazy='dynamic'` to `lazy='select'` means the relationship is now a list, so template methods like `.count()` must be replaced with the `|length` filter. Also, always verify changes do not introduce template syntax errors or missing imports.
