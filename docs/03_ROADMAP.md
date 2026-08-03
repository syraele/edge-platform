# EDGE_ENGINE Roadmap

## Current Status

The Foundation / Research phase is now complete and verified. The repository is stable, documented, and ready to serve as the baseline for the next Intelligence phase.

---

## Completed Milestones

### Foundation

**COMPLETE**

The architectural foundation, documentation structure, and domain boundaries are present and stable.

### Dataset Layer

**COMPLETE**

The repository includes a manifest-backed local dataset registry and a filesystem CSV provider for reproducible local research execution.

### Research Pipeline

**COMPLETE**

The application layer orchestrates dataset loading, hypothesis execution, evidence collection, validation, and report generation.

### Discovery Engine

**COMPLETE**

The current implementation includes:

* Primitive Catalog
* Primitive Discovery Engine
* Combination Engine Level 1
* Compound Hypothesis Evaluation
* Edge Scoring
* Human Discovery Report
* Candidate-edge selection reporting aligned with Knowledge-based selection results

### CLI

**COMPLETE**

The CLI entrypoint is operational and can run the official local benchmark:

```powershell
.\.venv\Scripts\python.exe -m edge research --provider filesystem-csv --symbol EURUSD --timeframe M1 --from 2024-01-01T00:00:00 --to 2024-01-01T01:00:00 --validation-from 2024-01-01T00:00:00 --validation-to 2024-01-01T01:00:00
```

---

## Foundation / Research Milestones

### STEP-001 — Architectural Principles Frozen

**COMPLETE**

This milestone freezes the enduring architectural principles that govern future evolution of the platform.

### STEP-001B — Development Workflow Frozen

**COMPLETE**

This milestone freezes the official development workflow for all future milestones.

### STEP-002 — Core Domain Language

**COMPLETE**

This milestone establishes the official domain language that governs future domain modeling.

### STEP-003 — Knowledge Lifecycle

**COMPLETE**

This milestone defines the official lifecycle of Knowledge within the platform.

### STEP-004 — Knowledge Aggregate Specification

**COMPLETE**

This milestone defines the official domain specification for the Knowledge Aggregate.

### STEP-005 — Knowledge Value Objects

**COMPLETE**

This milestone defines the official domain specification for the Value Objects belonging to the Knowledge Aggregate.

### STEP-006 — Knowledge Repository Contract

**COMPLETE**

This milestone defines the official domain contract for the Knowledge Repository.

### STEP-006 — Domain Map

**COMPLETE**

This milestone defines the official domain map and aggregate boundaries for EDGE_ENGINE.

---

## Current Milestone Status

### Foundation / Research

**COMPLETED**

The repository now represents a stable Foundation / Research baseline with verified documentation and regression coverage.

### KF-004 — Knowledge Consolidation

**PLANNED**

The next milestone will introduce knowledge-consolidation capabilities that:

* group redundant Knowledge items;
* identify representative canonical knowledge;
* preserve variants as metadata;
* enable candidate-edge qualification from compact knowledge clusters;
* do not modify the Domain Model or Foundation v2.

The Intelligence phase will begin only after the Foundation / Research baseline remains stable and documented.
