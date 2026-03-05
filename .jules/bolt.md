
## 2024-05-19 - Generator & yield_per for CSV Exports
**Learning:** Using `Model.query.all()` buffers entire datasets (like thousands of rows) in memory which crashes or heavily impacts memory usage for basic CSV exports.
**Action:** Use a streaming Flask Response combined with a generator function and SQLAlchemy's `db.session.query(Model).yield_per(batch_size)` to fetch and write records iteratively. This streams the CSV and reduces memory overhead to practically O(1). Note that `.yield_per()` works with standard queries and many-to-one `.joinedload()`s, but breaks on one-to-many/many-to-many joined loads.
