# EDGE_ENGINE Git Workflow

---
**Document ID:** GIT-001
**Version:** 1.0.0
**Status:** Approved
**Owner:** EDGE_ENGINE Project
**Last Updated:** 2026-07-14

**Related Documents**

- 03_ROADMAP.md
- 05_CODING_STANDARD.md
- 06_TESTING.md
---

# 1. Purpose

This document defines the official Git workflow for EDGE_ENGINE.

The objective is to keep the repository clean, traceable and reproducible.

---

# 2. Branch Strategy

Current strategy:

- main (or master): stable branch
- Feature development is completed as small, reviewable milestones.

Future branch strategies may evolve as the project grows.

---

# 3. Development Cycle

Every milestone follows the same lifecycle:

Design
→ Review
→ Documentation
→ Implementation
→ Testing
→ Final Review
→ Git Commit

---

# 4. Commit Principles

Every commit must:

- have a single purpose;
- be buildable;
- keep tests passing;
- preserve repository consistency.

Avoid mixing unrelated changes.

---

# 5. Commit Message Convention

Format:

<type>: <summary>

Examples:

- docs: add testing strategy
- feat(domain): add MarketDescriptor entity
- test(core): add runtime tests
- refactor(application): simplify experiment workflow
- fix(data): validate dataset metadata

---

# 6. Recommended Commit Types

- feat
- fix
- refactor
- docs
- test
- chore

---

# 7. Before Every Commit

Checklist:

- Documentation updated (if required)
- Tests passing
- No debug code
- No temporary files
- Meaningful commit message

---

# 8. Milestone Commits

Prefer one commit per completed milestone.

Milestones should represent coherent progress.

---

# 9. Repository History

Git history should tell the story of the project.

Every commit should explain why the repository improved.

---

# 10. Conclusion

Git is the permanent memory of EDGE_ENGINE.

Every commit should leave the project in a better state than before.

End of Document
