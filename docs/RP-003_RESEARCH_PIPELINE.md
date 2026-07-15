# RP-003 — Research Pipeline

Version: 1.0

Status: Approved

Phase: Application Layer & Research Pipeline

---

# Purpose

The Research Pipeline is responsible for orchestrating the complete quantitative research workflow.

It coordinates the execution of the existing Application and Domain components without introducing business logic.

The pipeline represents the highest-level orchestration component of the Application Layer.

---

# Objective

Provide a single entry point capable of executing an entire research workflow from an existing Research Session to the generation of validated research results.

The Research Pipeline is responsible for coordination only.

All business decisions remain inside the Domain.

---

# Responsibilities

The Research Pipeline:

* receives an existing Research Session;
* coordinates the research execution;
* invokes the Experiment Runner;
* invokes the Domain services required by the workflow;
* aggregates the produced results;
* returns a complete pipeline execution result.

The pipeline does not interpret market data and does not implement research logic.

---

# Workflow

The pipeline coordinates the following conceptual workflow:

```text
Research Session
        ↓
Experiment Runner
        ↓
Research Evaluation
        ↓
Knowledge Collection
        ↓
Edge Generation
```

Each step delegates work to an existing component.

The Research Pipeline owns the execution flow only.

---

# Relationships

The Research Pipeline collaborates with:

* ResearchSession
* ExperimentRunner
* ResearchEvaluator
* KnowledgeCollection
* Edge

No Domain object depends on the Research Pipeline.

The dependency direction always points from the Application Layer towards the Domain.

---

# Public Interface

The pipeline exposes a single public execution entry point.

A client provides a Research Session.

The pipeline executes the workflow and returns a complete execution result.

---

# Design Principles

The Research Pipeline follows the Foundation principles:

* Application Layer orchestration only.
* No business logic.
* No market interpretation.
* No research evaluation.
* Domain independence.
* Reproducible execution.
* Composition over implementation.

---

# Out of Scope

The Research Pipeline is not responsible for:

* creating Research Sessions;
* executing individual experiments;
* evaluating research quality;
* validating Knowledge;
* managing Edge lifecycle;
* persistence;
* reporting.

Those responsibilities belong to other milestones.

---

# Acceptance Criteria

RP-003 is complete when:

* the complete research workflow is orchestrated by a single component;
* existing Application components are reused;
* Domain responsibilities remain unchanged;
* no business logic is introduced into the Application Layer;
* the implementation is fully covered by integration tests;
* the complete regression suite passes.

---

# Result

After RP-003, EDGE_ENGINE is capable of orchestrating an entire research workflow through a single Application Layer component while preserving the boundaries defined by Foundation v2.
