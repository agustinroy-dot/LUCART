
## 2024-05-18 - [Fix N+1 query in quotes index]
**Learning:** Found N+1 query problem on quotes index accessing customer relationships inside loop.
**Action:** Adding joinedload for customer on quote listing prevents N+1 query and improves performance heavily.
