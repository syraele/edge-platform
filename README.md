# EDGE_ENGINE

A Domain-Driven research engine for building, validating, and evolving quantitative knowledge.

---

## Overview

EDGE_ENGINE is a long-term research platform designed to transform historical market data into validated, reproducible, and reusable quantitative knowledge.

The project applies Domain-Driven Design (DDD), Clean Architecture, and a scientific research methodology to support the systematic construction of quantitative knowledge and the discovery of validated trading edges.

EDGE_ENGINE is **not** a trading platform or an automated trading system.

Its primary objective is the construction and preservation of quantitative knowledge.

---

## Core Principles

The project is built around the following principles:

* Domain First
* Scientific Method
* Evidence Before Opinion
* Knowledge Must Accumulate
* Reproducibility by Design
* Evolution Over Perfection
* Clean Boundaries

These principles are formally defined in the Manifesto.

---

## Project Structure

```text
edge-platform/
│
├── FOUNDATION_BLUEPRINT.md
├── PROJECT_BOOTSTRAP.md
├── PROJECT_STATUS.md
├── README.md
│
├── docs/
│   ├── 00_MANIFESTO.md
│   ├── 01_ARCHITECTURE.md
│   ├── 02_RESEARCH_MODEL.md
│   ├── 03_ROADMAP.md
│   ├── 04_DOMAIN_MODEL.md
│   ├── 05_CODING_STANDARD.md
│   ├── 06_TESTING.md
│   ├── 07_GIT_WORKFLOW.md
│   ├── 08_DECISIONS.md
│   ├── 09_GLOSSARY.md
│   ├── 10_PLATFORM_PRINCIPLES.md
│   └── PLATFORM_EVOLUTION_REVIEW.md
│
├── src/
├── tests/
└── ...
```

---

## Documentation

The documentation is organized by responsibility.

| Document | Purpose |
| --- | --- |
| AGENTS.md | Operational guidance for contributors and assistants |
| FOUNDATION_BLUEPRINT.md | Conceptual foundation of the project |
| PROJECT_STATUS.md | Current project status and milestone state |
| PROJECT_BOOTSTRAP.md | Development bootstrap procedure |
| 00_MANIFESTO.md | Project philosophy and principles |
| 01_ARCHITECTURE.md | System architecture |
| 02_RESEARCH_MODEL.md | Research methodology |
| 03_ROADMAP.md | Project evolution |
| 04_DOMAIN_MODEL.md | Business domain model |
| 05_CODING_STANDARD.md | Development standards |
| 06_TESTING.md | Testing strategy |
| 07_GIT_WORKFLOW.md | Development workflow |
| 08_DECISIONS.md | Architecture decision process |
| 09_GLOSSARY.md | Ubiquitous language |
| 10_PLATFORM_PRINCIPLES.md | Long-term architectural principles for platform evolution |
| docs/PLATFORM_EVOLUTION_REVIEW.md | Consolidated review package for Platform Evolution milestones |
| docs/PE-001_EXECUTION_BRIEF.md | Execution-oriented guide for the next PE-001 implementation step |
| docs/PE-001_IMPLEMENTATION_PLAN.md | Structured implementation plan for PE-001 |
| docs/PE-001_DELIVERABLES_CHECKLIST.md | Completion checklist for PE-001 preparation |
| docs/PE-001_REVIEW_SUMMARY.md | Readiness summary for PE-001 review |
| docs/PE-001_APPROVAL_NOTE.md | Approval-oriented summary for PE-001 |
| docs/PLATFORM_EVOLUTION_EXECUTION_PATH.md | Operational execution path for Platform Evolution milestones |
---

## Development Workflow

EDGE_ENGINE follows an incremental development process.

```text
Milestone
      ↓
Repository Review
      ↓
Technical Review
      ↓
Specification Review & Approval
      ↓
Test-First Implementation
      ↓
Regression Testing
      ↓
Documentation Synchronization
      ↓
Commit
```

Every milestone preserves the architectural foundation established during Foundation v2.

For the latest workflow guidance, see:

* AGENTS.md
* docs/DEVELOPMENT_SETUP.md
* docs/DEVELOPMENT_WORKFLOW.md

---

## Current Status

Current Phase:

**Completed**

Current Milestone:

**None – documented roadmap completed**

The documented roadmap is complete through PE-007 Distributed Research Execution and EF-004 Edge Management.

Last completed milestone:

**PE-007 – Distributed Research Execution (Completed)**

Platform Evolution Milestones:

* PE-001 – Plugin System
* PE-002 – Advanced Dataset Providers
* PE-003 – Portfolio Research
* PE-004 – Optimization Engine
* PE-005 – Machine Learning Integration
* PE-006 – Visualization Dashboards
* PE-007 – Distributed Research Execution

Next step:

**Preserve the completed baseline and introduce future work only through a new approved milestone or ADR.**

For the latest project status, see PROJECT_STATUS.md.

---

## Contributing

Every contribution must remain consistent with:

* the Foundation Blueprint;
* the Manifesto;
* the Architecture;
* the Domain Model;
* the Coding Standard.

Architectural changes are introduced only through Architecture Decision Records (ADRs).

# Assistant Working Agreement

During normal development the assistant must:

1. Read PROJECT_STATUS.md.
2. Read FOUNDATION_BLUEPRINT.md.
3. Read only the documentation relevant to the active milestone.
4. Treat Foundation v2 as frozen.
5. Continue implementation from the current milestone.
6. Avoid proposing architectural redesigns unless explicitly requested or required by an accepted ADR.

---

## License

Project license: TBD.
