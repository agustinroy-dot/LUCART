
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-19 - [Dynamic Relationships and Eager Loading]
**Learning:** Found an N+1 query issue in the `view_order` route for `app/orders/routes.py`. Trying to use `selectinload` or `joinedload` on relationships defined with `lazy='dynamic'` fails because dynamic relationships return queries, not collections. Furthermore, blindly replacing `.count()` with `|length` in Jinja templates after converting a dynamic relationship to a normal one works for lists, but if the relationship is reverted back to `lazy='dynamic'`, it must be changed back to `.count()` or it won't be evaluated correctly.
**Action:** When migrating `lazy='dynamic'` to eager-loaded default relationships to resolve N+1 queries, ensure no other parts of the application rely on the query-builder methods (like `.count()`, `.filter()`, etc.) or revert them and handle them carefully one model at a time.
