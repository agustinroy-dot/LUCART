## 2026-02-13 - [Fixed N+1 Queries in Order View]
**Learning:** `lazy='dynamic'` on SQLAlchemy relationships prevents eager loading (`joinedload`), causing significant N+1 issues when iterating.
**Action:** Remove `lazy='dynamic'` (defaulting to list loading) for small collections like order items/materials to enable eager loading and reduce query count from N+1 to 1-3. Update templates to use `|length` instead of `.count()`.
