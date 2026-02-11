## 2025-02-11 - Fixed N+1 in Order View & Broken Template
**Learning:** Legacy templates might contain broken or duplicated HTML structures (like nested forms) that only become apparent when editing nearby code. When fixing N+1 issues by changing relationships from `dynamic` to `list`, always verify template compatibility (e.g., `count()` vs `length`) and ensure the template structure is valid.
**Action:** Before editing a template, quickly scan it for obvious syntax errors or duplicates, especially if the file has a history of merges.
