# EF-003 — Edge Lifecycle

Version: 1.0

Status: Approved

Related Documents

- FOUNDATION_BLUEPRINT.md
- docs/04_DOMAIN_MODEL.md
- docs/EF-001_EDGE_MODEL.md
- docs/EF-002_EDGE_VALIDATION.md

---

# Purpose

This document defines the explicit lifecycle transitions for the `Edge`
Aggregate.

The milestone makes lifecycle progression observable and enforceable without
introducing mutable Domain state, infrastructure dependencies, or business
scoring logic.

---

# Scope

EF-003 introduces only immutable lifecycle evolution for a single `Edge`.

It does not introduce:

- portfolio management;
- persistence;
- execution;
- scheduling;
- performance-based retirement rules.

---

# Responsibilities

The `Edge` Aggregate must:

- expose explicit lifecycle transition methods;
- preserve valid state progression;
- reject invalid lifecycle transitions deterministically;
- remain immutable by returning new `Edge` instances.

---

# Lifecycle Rules

Allowed transitions:

- `candidate` -> `validated`
- `validated` -> `active`
- `active` -> `retired`

Disallowed transitions include:

- self-transitions;
- skipping intermediate states;
- any transition from `retired`.

---

# Definition of Done

EF-003 is complete when:

- lifecycle transition methods exist on `Edge`;
- invalid transitions fail explicitly;
- the Aggregate remains immutable;
- unit tests pass;
- Foundation remains unchanged.

End of Document