# EF-002 — Edge Validation

Version: 1.0

Status: Approved

Related Documents

- FOUNDATION_BLUEPRINT.md
- 04_DOMAIN_MODEL.md
- EF-001_EDGE_MODEL.md

---

# Purpose

This document defines the baseline validation process that determines whether validated Knowledge can originate an Edge.

---

# Scope

This milestone introduces the first Edge validation process.

It does not introduce:

- execution;
- trading;
- portfolio management;
- optimization;
- infrastructure.

---

# Responsibilities

Edge validation determines whether validated Knowledge is considered actionable.

---

# Baseline Rule

If valid Knowledge exists:

→ an Edge may be created.

Otherwise:

→ no Edge is produced.

The baseline implementation intentionally avoids introducing business-specific validation rules.

---

# Relationship with Knowledge

Knowledge represents validated conclusions.

Edge represents validated conclusions considered operationally useful.

Knowledge and Edge intentionally model different concepts.

---

# Future Evolution

Future milestones may introduce:

- quantitative thresholds;
- confidence analysis;
- performance evaluation;
- automated edge scoring.

Those capabilities are outside EF-002.

---

# Definition of Done

EF-002 is complete when:

- Edge validation exists;
- unit tests pass;
- Foundation remains unchanged.

End of Document