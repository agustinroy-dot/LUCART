
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2026-05-27 - [N+1 Optimization on Lazy Dynamic Relationships]
**Learning:** When addressing N+1 query problems by changing `lazy='dynamic'` relationships to `lazy='select'` and using `joinedload`, two critical things must happen:
1. Ensure `joinedload` is imported in the route files using the relationship.
2. Carefully update any Jinja templates using `.count()` on those relationships to use the `|length` filter instead. Failing to replace `.count()` everywhere the relationship is used in templates will lead to application crashes.
**Action:** Always do a codebase-wide search (e.g., `grep -rnw app -e "\.count("`) before making lazy loading relationship changes, and double check imports when adding `joinedload`.
