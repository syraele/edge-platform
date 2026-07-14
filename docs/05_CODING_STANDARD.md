# EDGE_ENGINE Coding Standard

---
**Document ID:** CODE-001
**Version:** 1.0.0
**Status:** Approved
**Owner:** EDGE_ENGINE Project
**Last Updated:** 2026-07-14

**Related Documents**

- 00_MANIFESTO.md
- 01_ARCHITECTURE.md
- 04_DOMAIN_MODEL.md
---

# 1. Purpose

This document defines the official coding standards for EDGE_ENGINE.

The objective is to produce code that is readable, maintainable, testable and aligned with the project architecture.

---

# 2. Core Principles

- Readability over cleverness.
- Simplicity over complexity.
- Explicit is better than implicit.
- Domain first.
- Infrastructure second.
- Small, focused classes.
- Deterministic behavior.

---

# 3. Project Rules

- Never bypass the Domain.
- Business rules belong only to the Domain.
- Infrastructure never contains business logic.
- Every public class has one responsibility.
- Prefer composition over inheritance.

---

# 4. Naming

Classes:
- PascalCase

Functions:
- snake_case

Variables:
- snake_case

Constants:
- UPPER_CASE

Modules:
- snake_case.py

Names must express business meaning.

---

# 5. Type Hints

All public functions must use type hints.

Example:

```python
def load_dataset(path: str) -> HistoricalDataset:
    ...
```

---

# 6. Documentation

Every public module should contain a short docstring.

Complex business rules must be documented.

Comments should explain *why*, not *what*.

---

# 7. Error Handling

- Fail fast.
- Raise meaningful exceptions.
- Never silently ignore errors.
- Validate inputs at boundaries.

---

# 8. Testing Expectations

New business logic requires tests.

Bug fixes should include regression tests.

Code is considered complete only when tests pass.

---

# 9. Review Checklist

Before committing:

- Architecture respected
- Domain unchanged unless intended
- Tests passing
- Type hints present
- Naming consistent
- No duplicated logic
- Documentation updated if required

---

# 10. Conclusion

The coding standard exists to preserve long-term quality.

Every implementation should make EDGE_ENGINE easier to evolve, test and understand.

End of Document
