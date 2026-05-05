
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-18 - [Order/Quote Items N+1 Query]
**Learning:** Rendering SQLAlchemy relationships that are marked `lazy='dynamic'` cannot be eager loaded with `joinedload`. When an order view template loops through `order.items` and `order.materials`, if the models declare them as `lazy='dynamic'`, accessing those loops triggers an N+1 query pattern. To fix, modify the relationships to `lazy='select'`, and then use `.options(joinedload(...))` on queries. Additionally, jinja templates using `.count()` on dynamic relationships must be updated to `|length` on the list when changing to eager load.
**Action:** When a template loops over a model relationship, check if the relationship is `lazy='dynamic'`. If so, it must be changed to `lazy='select'` (and `.count()` refactored to `|length`) to allow `joinedload` eager-loading.
