## 2025-05-23 - Broken Templates Block Performance Verification
**Learning:** Even when focusing on backend performance, frontend templates can be broken in a way that prevents running the test suite.
**Action:** Before running tests to verify an optimization, quickly check if the test suite passes on the base branch. If not, be prepared to fix unrelated blockers (like `TemplateSyntaxError`) to proceed.

## 2025-05-23 - AppSetting N+1 Optimization
**Learning:** `AppSetting.get()` was performing a DB query on every call. In request contexts where multiple settings are accessed (e.g., forms, quotes), this causes N+1 issues.
**Action:** Implemented request-level caching using `flask.g`. Fetch all settings in one query on first access within a request, then serve from cache. This reduced queries from N to 1.
