# RP-002 — Experiment Runner

Version: 1.1

Status: Design

Phase: Application Layer

---

# Purpose

The Experiment Runner is an Application Layer component responsible for coordinating the execution of a single Experiment.

Its responsibility is orchestration only.

The Experiment Runner does not implement business logic and does not modify Domain behaviour.

---

# Objectives

The Experiment Runner provides a reproducible execution mechanism for one Experiment.

It coordinates the interaction between the Application Layer and the Domain while preserving clean architectural boundaries.

---

# Responsibilities

The Experiment Runner is responsible for:

* receiving a Research Experiment;
* delegating execution to the Domain ExperimentExecutor;
* coordinating Application Layer execution;
* collecting the produced Evidence;
* returning the execution result.

The Experiment Runner does not evaluate the produced Evidence.

---

# Non-Responsibilities

The Experiment Runner is not responsible for:

* generating Research Hypotheses;
* validating Experiments;
* producing Evidence directly;
* evaluating Evidence;
* generating Knowledge;
* creating Edges;
* coordinating complete research pipelines;
* report generation.

Those responsibilities belong to other milestones.

---

# Lifecycle

The Experiment Runner follows a simple execution lifecycle.

```text
Idle
    ↓
Running
    ↓
Completed
```

If execution cannot be completed:

```text
Idle
    ↓
Running
    ↓
Failed
```

The Runner itself is stateless between executions.

---

# Relationships

The Experiment Runner coordinates the following interaction.

```text
ResearchSession
        ↓
ExperimentRunner
        ↓
ExperimentExecutor
        ↓
Evidence
        ↓
ResearchEvaluator
        ↓
Knowledge
```

The Domain performs all business operations.

The Application Layer only coordinates them.

---

# Public Interface

The Runner exposes a minimal execution interface.

Typical operation:

* receive one Experiment;
* delegate execution to the Domain ExperimentExecutor;
* return the produced Evidence.

The Runner never performs Domain computations.

---

# Execution Context

The Experiment Runner executes within an existing Research Session.

It does not own session state.

It receives the required execution context from the caller.

---

# Design Principles

The Experiment Runner follows the Foundation principles.

* Domain First
* Clean Boundaries
* Reproducibility by Design
* Simplicity Over Cleverness
* Evidence Before Opinion

The Runner never replaces Domain behaviour.

---

# Out of Scope

The following capabilities belong to future milestones.

* multiple experiment execution;
* execution scheduling;
* parallel execution;
* pipeline orchestration;
* execution reports;
* persistence;
* retries;
* distributed execution.

---

# Acceptance Criteria

RP-002 is complete when:

* the Application Layer provides an Experiment Runner;
* the Domain provides an ExperimentExecutor;
* the Runner coordinates exactly one Experiment execution;
* the Domain produces the corresponding Evidence;
* Domain responsibilities remain unchanged;
* the Runner remains stateless between executions;
* the implementation introduces no business logic into the Application Layer;
* the implementation prepares the foundation for RP-003 Research Pipeline.
