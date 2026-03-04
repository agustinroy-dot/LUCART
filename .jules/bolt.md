## 2024-05-15 - [Refactored CSV Exports to Stream]
**Learning:** `io.StringIO().getvalue()` loads the entire generated CSV into memory before returning it to the user. Using `.yield_per(100)` and a generator function with Flask's `Response(stream_with_context(generate()), mimetype="text/csv")` solves the memory explosion issue with very large tables.
**Action:** Always prefer `yield_per()` combined with streaming responses for data exports that potentially scale with database size.
