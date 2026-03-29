## 2024-05-19 - Request-level Caching for AppSetting

**Learning:** The `AppSetting.get()` method in `app/models.py` queries the database on every call. In routes like `/quotes/calculator`, this is called repeatedly in the same request, leading to N+1 type issues for configuration fetching. Implementing a simple request-level cache using `flask.g` solves this.

**Action:** When seeing repeated identical queries within a request lifecycle, consider `flask.g` for request-level caching. Ensure to clear or update the cache when `AppSetting.set()` is called within the same request.
