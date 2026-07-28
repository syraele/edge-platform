# EDGE_ENGINE Project Status

Version: v1.1.0-alpha

Status: Stable

Last Updated: 2026-07-28

---

## Current Phase

**Discovery Engine**

## Project State

The repository is currently aligned with the implemented discovery workflow. The core research flow is operational end to end and has been validated on real MT5 data.

## Completed Milestones

* Foundation
* Dataset Layer
* MT5 Integration
* Research Pipeline
* Discovery Pipeline
* CLI
* Primitive Catalog
* Primitive Discovery Engine
* Combination Engine Level 1
* Compound Hypothesis Evaluation
* Edge Scoring
* Human Discovery Report

## Regression

* 153 tests passed

## Validation

* End-to-end discovery execution validated on real MT5 data using:
  `python -m edge research --provider mt5 --symbol XAUUSD --timeframe M1 --from 2026-04-20 --to 2026-04-22`

## Current Objective

**DI-006 — Edge Improvement Analysis**

## Notes

The current implementation preserves the existing domain model and architecture while extending the research workflow with primitive and compound hypothesis evaluation, ranking, and human-readable reporting.

Market Description baseline.

### MDF-002

**Completed**

Descriptor Registry.

### MDF-003

**Completed**

Descriptor Validation.

---

## Phase 3 — Research Framework

### RF-001

**Completed**

ResearchHypothesis Aggregate.

### RF-002

**Completed**

Experiment Aggregate.

### RF-003

**Completed**

Evidence Value Object.

### RF-004

**Completed**

ResearchEvaluator Domain Service.

---

## Phase 4 — Knowledge Framework

### KF-001

**Completed**

Knowledge Value Object.

### KF-002

**Completed**

Knowledge Validation.

### KF-003

**Completed**

KnowledgeCollection Value Object.

---

## Phase 5 — Edge Framework

### EF-001

**Completed**

Edge Aggregate.

### EF-002

**Completed**

Edge Validation.

### EF-003

**Completed**

Edge Lifecycle.

### EF-004

**Completed**

Edge Management.

---

## Phase 6 — Application Layer & Research Pipeline

### RP-000

**Completed**

Application Layer architecture.

### RP-001

**Completed**

Research Session.

### RP-002

**Completed**

Experiment Runner.

### RP-003

**Completed**

Research Pipeline.

### RP-004

**Completed**

Pipeline Report.

---

# Repository Status

## Documentation

**Synchronized**

Latest updates:

* PROJECT_STATUS.md reflects roadmap completion through PE-007 and EF-004.
* PE-007 distributed workload coordination, EF-003 lifecycle transitions, and EF-004 edge management are synchronized with the implementation.
* Python 3.11 is the minimum supported runtime because the codebase uses `datetime.UTC`.
* Historical milestone status labels are synchronized with their completed milestones.

## Testing

Full local regression for roadmap completion: **122 passing tests** with Python 3.14.6.

---

# Current Priorities

1. Preserve Foundation consistency.
2. Treat future feature work as a new approved milestone or ADR-governed extension.

---

# Project Metrics

## Test Suite

Last recorded: **122 passing** after roadmap completion.

## Architecture

Stable

## Foundation

Frozen

## Application Layer

Platform Evolution distributed coordination and Edge lifecycle/management are completed.

Next governance action: open any future work only through a new approved milestone or ADR.

## Documentation

Synchronized with roadmap completion through PE-007 and EF-004.

---

# Development Workflow

Every milestone follows:

```text
Repository Review
        ↓
Technical Review
        ↓
Implementation Plan
        ↓
Milestone Specification Review & Approval
        ↓
Functional Block Implementation
        ↓
Regression Testing
        ↓
Documentation Synchronization
        ↓
Next Milestone Preparation
        ↓
Commit
```

PROJECT_STATUS.md represents the official project checkpoint between conversations.

---

# Architecture Policy

Foundation v2 is the authoritative architectural baseline.

The Domain Model is frozen.

The Application Layer orchestrates the Domain without modifying it.

Architectural changes require:

* a demonstrated defect;
* a business requirement;
* an approved ADR.

---

# Development Principles

* The repository is the single source of truth.
* Documentation drives implementation.
* Every milestone requires an approved Milestone Specification.
* The roadmap is the authoritative implementation guide.
* Implement one milestone at a time.
* Complete each milestone before starting the next.
* Prepare the next milestone before closing the current one.
* Follow the Repository First workflow.
* Study existing technologies for ideas and algorithms while keeping the EDGE_ENGINE Core independent.
* Do not introduce external framework dependencies into the Core.

---

# Next Action

No active implementation milestone. Future repository changes require a new approved milestone or ADR-governed architectural decision.

---

# Assistant Bootstrap

When starting a new conversation:

1. Read PROJECT_STATUS.md.
2. Read PROJECT_BOOTSTRAP.md.
3. Read DEVELOPMENT_WORKFLOW.md.
4. Read FOUNDATION_BLUEPRINT.md.
5. Read 03_ROADMAP.md.
6. Read the active Milestone Specification.
7. Review the affected repository area.
8. Produce an Implementation Plan.
9. Obtain approval.
10. Continue following the documented workflow.

---

# Assistant Policy

Current objective:

Preserve the completed roadmap baseline and open new work only through approved governance.

Continue development following the documented workflow.

Foundation v2 is frozen.

The roadmap is authoritative.

The repository is the single source of truth.

Implementation is not allowed without an approved Milestone Specification.

The repository is the single source of truth.

