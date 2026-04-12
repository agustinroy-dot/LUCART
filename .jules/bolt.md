
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [Order N+1 Query in `view_order` caused by `lazy='dynamic'`]
**Learning:** The `items` and `materials` relationships on the `Order` model used `lazy='dynamic'`. While this allows appending `filter()` or `count()`, it forces those collections to be lazy-loaded, even if you attempt to use eager loading in the query (like `joinedload` or `selectinload`). This caused severe N+1 query bottlenecks in `view_order` since both loops access `order.items` and `order.materials`.
**Action:** Replace `lazy='dynamic'` with default/select loading for relationships that are fully iterated over in templates, enabling `selectinload` optimization. Remember to migrate template calls from `.count()` to `|length` as the relationship returns a list rather than a Query.
