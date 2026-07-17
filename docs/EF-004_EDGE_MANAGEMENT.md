# EF-004 — Edge Management

Version: 1.0

Status: Approved

Related Documents

- FOUNDATION_BLUEPRINT.md
- docs/04_DOMAIN_MODEL.md
- docs/EF-001_EDGE_MODEL.md
- docs/EF-003_EDGE_LIFECYCLE.md

---

# Purpose

This document defines the minimal Domain management model for multiple
validated edges.

The milestone introduces deterministic collection and management behaviour
without turning the Domain into a trading, ranking, or portfolio engine.

---

# Scope

EF-004 introduces:

- an immutable collection of unique `Edge` instances;
- deterministic add, replace, remove, and retrieval behaviour;
- convenience filtering for active edges.

It does not introduce:

- persistence;
- ranking or scoring;
- automated activation criteria;
- portfolio allocation;
- risk management.

---

# Responsibilities

Edge management must:

- preserve unique edge identity within a collection;
- provide deterministic ordering by edge identity;
- support replacement of an existing edge by identity;
- allow explicit removal by identity;
- expose only active edges when requested.

---

# Domain Contract

The implementation may introduce:

- an immutable `EdgeCollection` value object containing managed edges;
- an `EdgeManager` Domain service for collection operations.

The service must reject duplicate registration and removal of an unknown edge.

---

# Definition of Done

EF-004 is complete when:

- `EdgeCollection` exists;
- `EdgeManager` exists;
- deterministic management operations and active-edge filtering are tested;
- Foundation remains unchanged.

End of Document