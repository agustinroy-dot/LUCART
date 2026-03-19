
## 2024-05-15 - [Cache AppSetting with flask.g]
**Learning:** `AppSetting.get()` calls execute a database query on every invocation. Since the app relies on repeated database lookups for configuration values (e.g. `electricity_rate`, `labor_rate`), this creates N+1 query problems within single requests.
**Action:** Implementing request-level caching using `flask.g` ensures subsequent lookups within the same request hit the cache instead of the database, significantly reducing query counts and latency. Always check `flask.has_request_context()` before using `flask.g` to prevent errors during background tasks or test setups.
