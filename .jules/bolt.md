## 2024-05-18 - [Quotes N+1 Query]
**Learning:** Found an N+1 query issue in the Quotes index route (`/app/quotes/routes.py`) where the template accessed `quote.customer.name` inside a loop, triggering a separate query for each quote. Fixed by eager-loading with `joinedload(Quote.customer)`.
**Action:** Always inspect Jinja template loops over database models for relationship accesses and ensure those relationships are eager-loaded in the route's SQL query using `joinedload`.

## 2024-05-19 - [AppSetting Cache Initialization Bug]
**Learning:** When adding request-level caching with `flask.g` (e.g., for `AppSetting.get`), updating the cache during a `set()` operation can introduce a bug if the cache hasn't been initialized yet. If you just set `g.app_settings_cache = {key: value}`, subsequent `get` calls will find the cache exists but contains only that single key, leading to incorrect defaults for all other settings.
**Action:** Always ensure full cache initialization before modifying it during an update operation, or clear the cache completely on update.
