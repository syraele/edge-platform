# EF-001 — Edge Model

Version: 1.0

Status: Approved

Related Documents

- FOUNDATION_BLUEPRINT.md
- 04_DOMAIN_MODEL.md
- KF-001_KNOWLEDGE_MODEL.md
- KF-002_KNOWLEDGE_VALIDATION.md
- KF-003_KNOWLEDGE_COLLECTION.md

---

# Purpose

This document defines the Edge Aggregate Root.

Edge represents validated quantitative knowledge that has demonstrated practical value and can be managed throughout its lifecycle.

---

# Scope

EF-001 introduces only the Edge Aggregate.

It does not introduce:

- execution;
- portfolio management;
- risk management;
- persistence;
- optimization;
- strategy generation.

---

# Responsibilities

Edge:

- originates from validated Knowledge;
- represents actionable quantitative knowledge;
- owns its lifecycle;
- is immutable except for lifecycle evolution handled by future milestones.

---

# Non-Responsibilities

Edge does not:

- execute trades;
- validate experiments;
- generate Knowledge;
- evaluate Evidence;
- manage persistence.

---

# Domain Representation

Edge is an Aggregate Root.

Baseline implementation:

- identifier
- Knowledge
- lifecycle state

---

# Invariants

An Edge:

- must originate from validated Knowledge;
- must always have a valid lifecycle state;
- cannot exist without Knowledge.

---

# Lifecycle

The lifecycle defined by the Domain Model is:

Candidate

↓

Validated

↓

Active

↓

Retired

Lifecycle transitions will be implemented in future milestones.

---

# Relationship with Knowledge

Knowledge represents validated conclusions.

Edge represents validated conclusions that are considered operationally useful.

Not every Knowledge necessarily becomes an Edge.

---

# Future Evolution

Future milestones may introduce:

- activation criteria;
- retirement rules;
- performance tracking;
- edge ranking;
- monitoring.

Those capabilities remain outside EF-001.

---

# Definition of Done

EF-001 is complete when:

- Edge Aggregate exists;
- lifecycle state exists;
- unit tests pass;
- Foundation remains unchanged.

End of Document