
## 2024-05-10 - Streaming generator with yield_per for massive CSV exports
**Learning:** Returning large data exports via `.query.all()` into a single `io.StringIO` buffer can cause significant memory pressure (30+ MB vs ~3 MB for generators on 10k rows) and impact concurrent users. Using `.yield_per()` paired with generator yields fixes this.
**Action:** When implementing any data export (CSV, JSON, etc) that spans an arbitrary amount of rows, stream the data in chunks utilizing a generator with SQLAlchemy's `yield_per(N)` to cap memory footprints.
