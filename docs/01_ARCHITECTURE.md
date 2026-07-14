
# EDGE_ENGINE Architecture

---
**Document ID:** ARCH-001  
**Version:** 1.0.0  
**Status:** Approved  
**Owner:** EDGE_ENGINE Project  
**Last Updated:** 2026-07-14

**Related Documents**

- 00_MANIFESTO.md
- 02_RESEARCH_MODEL.md
- 03_ROADMAP.md
- 04_DOMAIN_MODEL.md
---

# 1. Purpose

This document defines the official software architecture of EDGE_ENGINE.

Its purpose is to describe how the platform is organized, how its components interact and which architectural rules govern its evolution.

This document is the architectural reference for the entire project.

Whenever implementation conflicts with this document, the architecture defined here takes precedence.

The architecture is intentionally designed to support long-term evolution while preserving stability, maintainability and reproducibility of quantitative research.

# 1.1 Scope

This document defines the software architecture of EDGE_ENGINE.

It specifies the architectural layers, dependency rules, responsibilities and structural principles governing the platform.

This document does not describe:

- the quantitative research methodology;
- the domain model;
- implementation details;
- coding standards;
- testing strategies.

Those topics are covered by dedicated documents.

---

# 2. System Vision

EDGE_ENGINE is a quantitative research platform designed to discover, validate and continuously monitor statistically replicable market edges.

Architecture exists to preserve research integrity.

Every architectural decision is evaluated according to its ability to improve reproducibility, maintainability and long-term evolution of the platform.

The platform does not exist to execute trades.

Its purpose is to transform market data into validated quantitative knowledge through deterministic and reproducible research workflows.

> **The output of EDGE_ENGINE is not a trade.  
> The output of EDGE_ENGINE is a validated edge supported by quantitative evidence.**

---

# 3. Architectural Principles

- Clean Architecture
- Domain-Driven Design (lightweight)
- SOLID
- Separation of Concerns
- Dependency Inversion
- Immutable Domain Artifacts
- Deterministic Research
- Reproducible Experiments
- Incremental Evolution

---

# 4. High-Level Architecture

```text
                +----------------------+
                |     Application      |
                +----------------------+
                          │
                          ▼
                +----------------------+
                |        Domain        |
                +----------------------+
                          │
                          ▼
                +----------------------+
                |         Core         |
                +----------------------+

Infrastructure
(Database, CSV, APIs, Filesystem, External Services...)

            │
            └────────────► Application
```

The architecture follows a strict inward dependency model.

Outer layers provide technical capabilities.

Inner layers define business knowledge.

Business knowledge must never depend on technology.

Research is implemented as Application use cases built on top of the Domain Model.

---

# 5. Layer Responsibilities

## Package Dependencies

```text
src/edge/

infrastructure
        │
        ▼
application
        │
        ▼
domain
        │
        ▼
core
```

## Core

### Owns

- Runtime
- Event Bus
- Logging
- Configuration
- Exceptions

### Does Not Own

- Business logic
- Research
- Trading
- AI
- Infrastructure

## Domain

### Owns

- Entities
- Value Objects
- Business Rules
- Immutable Artifacts

### Does Not Own

- Databases
- APIs
- CSV
- Pandas
- Filesystem

## Application

### Owns

- Use Cases
- Workflow orchestration
- Research pipelines

### Does Not Own

- Business rules
- Persistence

## Infrastructure

### Owns

- Persistence
- External APIs
- CSV Readers
- File Management

### Does Not Own

- Business decisions
- Domain rules

---

# 6. Dependency Rules

```text
Infrastructure
      │
      ▼
Application
      │
      ▼
Domain
      │
      ▼
Core
```

The dependency direction is mandatory.

Any reverse dependency represents an architectural violation.

| Layer | Allowed Dependencies |
|--------|----------------------|
| Core | None |
| Domain | Core |
| Application | Domain, Core |
| Infrastructure | Application, Domain (through abstractions), Core |

---

# 7. Official Research Pipeline

```text
Market Data
    ↓
HistoricalDataset
    ↓
Market Description Framework
    ↓
Market Vocabulary
    ↓
Configuration Generator
    ↓
Backtest Runner
    ↓
Scoring Engine
    ↓
Knowledge Base
    ↓
AI Research
    ↓
Validated Edge
```

---

# 8. Project Structure

```text
edge-platform/

docs/
src/
tests/

src/edge/
    core/
    domain/
    application/
    infrastructure/
    plugins/
```

---

# 9. Extension Strategy

EDGE_ENGINE evolves through extension rather than modification.

Typical extension points include:

- Data providers
- Market descriptors
- Vocabulary generators
- Backtest engines
- Scoring algorithms
- AI modules

---

# 10. Non-Goals

EDGE_ENGINE is not:

- a broker;
- a trading platform;
- an execution engine;
- a charting application;
- a technical indicator library.

Its purpose is quantitative research.

---

# 11. Stability Rules

- The Core is frozen.
- The Domain must remain infrastructure-independent.
- Business logic belongs to the Domain.
- Documentation precedes implementation.
- Every implementation is validated by tests.
- Architectural decisions are documented.

---

# 12. Future Evolution

```text
Core
 ↓
Domain
 ↓
Research Workflows
 ↓
Knowledge Engine
 ↓
AI Research
 ↓
Continuous Edge Discovery
 ↓
Validated Edge Repository
```

---

# 13. Conclusion

EDGE_ENGINE is designed to outlive individual implementations.

The architecture is optimized for correctness, reproducibility and long-term maintainability rather than short-term development speed.

Every future evolution of the platform should preserve these principles.
