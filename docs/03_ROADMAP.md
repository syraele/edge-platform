# EDGE_ENGINE Roadmap

## Current Status

The repository is currently in the Discovery Research phase. The implemented workflow is stable and validated on real MT5 data.

---

## Completed Milestones

### Foundation

**COMPLETE**

The architectural foundation, documentation structure, and domain boundaries are present and stable.

### Dataset Layer

**COMPLETE**

The repository includes both an MT5 provider and a filesystem CSV provider.

### Research Pipeline

**COMPLETE**

The application layer orchestrates dataset loading, hypothesis execution, evidence collection, and report generation.

### Discovery Engine

**COMPLETE**

The current implementation includes:

* Primitive Catalog
* Primitive Discovery Engine
* Combination Engine Level 1
* Compound Hypothesis Evaluation
* Edge Scoring
* Human Discovery Report

### CLI

**COMPLETE**

The CLI entrypoint is operational and can run:

```bash
python -m edge research --provider mt5 --symbol XAUUSD --timeframe M1 --from 2026-04-01 --to 2026-04-30
```

---

## Completed Milestones

### STEP-001 — Architectural Principles Frozen

**COMPLETE**

This milestone freezes the enduring architectural principles that govern future evolution of the platform.

### STEP-001B — Development Workflow Frozen

**COMPLETE**

This milestone freezes the official development workflow for all future milestones.

---

## Completed Milestones

### STEP-002 — Core Domain Language

**COMPLETE**

This milestone establishes the official domain language that governs future domain modeling.

---

## Completed Milestones

### STEP-003 — Knowledge Lifecycle

**COMPLETE**

This milestone defines the official lifecycle of Knowledge within the platform.

---

## Completed Milestones

### STEP-004 — Knowledge Aggregate Specification

**COMPLETE**

This milestone defines the official domain specification for the Knowledge Aggregate.

---

## Completed Milestones

### STEP-005 — Knowledge Value Objects

**COMPLETE**

This milestone defines the official domain specification for the Value Objects belonging to the Knowledge Aggregate.

---

## Completed Milestones

### STEP-006 — Knowledge Repository Contract

**COMPLETE**

This milestone defines the official domain contract for the Knowledge Repository.

---

## Completed Milestones

### STEP-006 — Domain Map

**COMPLETE**

This milestone defines the official domain map and aggregate boundaries for EDGE_ENGINE.

---

## Milestone Status

### EDGE-001

**COMPLETED**

Candidate Edge Selection is implemented and integrated into the Discovery Report.

### EDGE-002

**COMPLETED**

The discovery flow now exposes quantitative metrics derived from real trade sequences:

- Win Rate
- Expectancy
- Profit Factor
- Payoff
- Drawdown

### EDGE-003

**CURRENT**

Introduce a multi-criteria ranking system for research evaluation.

### Immediate corrective task

The current implementation must now be corrected so that the final Candidate Edge count is derived from the Knowledge selection result, not from the raw hypothesis rows.
