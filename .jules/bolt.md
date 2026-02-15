## 2025-02-27 - [Overuse of lazy='dynamic']
**Learning:** The codebase heavily uses `lazy='dynamic'` for relationships like `Order.items` and `Order.materials`. While useful for filtering large collections, it prevents SQLAlchemy's eager loading strategies (like `joinedload`) and causes severe N+1 query issues in views that simply iterate over these collections.
**Action:** Default to standard lazy loading (select) for collections that are frequently accessed in full (like line items in an order) to enable `joinedload` optimization. Use `dynamic` only when filtering is strictly required.
