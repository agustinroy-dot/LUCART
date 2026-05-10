
## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.
## 2024-05-18 - [AppSetting N+1 Query]
**Learning:** The `AppSetting` model used sequential database queries for each setting access (`AppSetting.get('key')`), causing an N+1 query problem during calculations or form rendering where multiple settings are needed (e.g. `electricity_rate`, `labor_rate`). Fixed by implementing a per-request cache using `flask.g` inside `AppSetting.get_all()` that warms the cache once. We also learned we must NEVER commit the local testing database (`instance/app.db`) to the repository.
**Action:** When working with configuration tables accessed multiple times per request, implement a batch-load caching mechanism using `flask.g` wrapped in `has_app_context()`. Always explicitly verify the `git status` to ensure temporary or local database files like `.db` are not committed to source control.
