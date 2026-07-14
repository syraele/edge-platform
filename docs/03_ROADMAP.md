# EDGE_ENGINE Roadmap

Version: 2.0

Status: Foundation v2

---

# Purpose

This document defines the planned evolution of EDGE_ENGINE.

It describes the major milestones of the project and their objectives.

The Roadmap defines *what* will be built and *when*.

It does not define architecture, domain concepts, or implementation details.

---

# Current Status

Current Phase

**Foundation v2**

Current Status

**Architecture Frozen**

Current Objective

**Begin implementation of the Market Description Framework (MDF-001).**

---

# Development Principles

Project evolution follows these principles:

* Foundation before implementation.
* Design before code.
* Tests before integration.
* Incremental evolution.
* Architecture preserved through ADRs.

---

# Development Lifecycle

Every milestone follows the same workflow.

```text
Milestone
        ↓
Design
        ↓
Implementation
        ↓
Testing
        ↓
Review
        ↓
Commit
        ↓
Next Milestone
```

No milestone is considered complete until every step has been successfully completed.

---

# Roadmap

## Phase 1 — Foundation

Objective

Establish a stable architectural and domain foundation.

Deliverables

* Foundation Blueprint
* Manifesto
* Architecture
* Research Model
* Domain Model
* Development Standards

Status

Completed

---

## Phase 2 — Market Description Framework (MDF)

Objective

Build the framework responsible for transforming historical market data into structured market descriptions.

Expected Deliverables

* MarketDescription Aggregate
* Descriptor infrastructure
* Descriptor registry
* Descriptor validation
* Descriptor tests

Status

Next Milestone

---

## Phase 3 — Research Framework

Objective

Introduce hypothesis management and experiment execution.

Expected Deliverables

* ResearchHypothesis
* Experiment
* Evidence
* ResearchEvaluator

Status

Planned

---

## Phase 4 — Knowledge Framework

Objective

Introduce persistent validated knowledge.

Expected Deliverables

* Knowledge model
* Knowledge validation
* Knowledge persistence
* Knowledge querying

Status

Planned

---

## Phase 5 — Edge Framework

Objective

Transform validated knowledge into operational trading edges.

Expected Deliverables

* Edge Aggregate
* Edge lifecycle
* Edge validation
* Edge management

Status

Planned

---

## Phase 6 — Platform Evolution

Objective

Expand the platform without changing the Core Domain.

Possible areas include:

* AI-assisted research
* Advanced experimentation
* New descriptor families
* Additional data sources
* Visualization
* Plugin ecosystem

Status

Future

---

# Success Criteria

The roadmap is complete when EDGE_ENGINE is capable of:

* describing markets;
* validating research hypotheses;
* accumulating reusable quantitative knowledge;
* managing validated trading edges;
* evolving through extension rather than architectural redesign.

---

# Governance

The Roadmap is a planning document.

Architectural changes are defined by the Architecture and Domain Model.

Implementation details belong to individual milestone specifications.

Progress is tracked through PROJECT_STATUS.md.
