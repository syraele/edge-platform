# RP-001 — Research Session

Version: 1.0

Status: Design

Phase: Application Layer

---

# Purpose

The Research Session represents a complete execution of a quantitative research workflow.

It is an Application Layer component responsible for coordinating the execution of a single research process while preserving the independence of the Domain.

The Research Session contains no business logic.

---

# Objectives

The session provides a consistent execution context for:

* one HistoricalDataset;
* one Market Description generation;
* one or more Research Hypotheses;
* one or more Experiments;
* Evidence collection;
* Knowledge generation;
* Edge generation.

The session coordinates these activities without implementing domain behaviour.

---

# Responsibilities

The Research Session is responsible for:

* maintaining the execution context;
* tracking execution status;
* exposing produced artifacts;
* coordinating Application Layer services;
* collecting execution metadata.

The Research Session is **not** responsible for:

* building Market Descriptions;
* evaluating hypotheses;
* executing experiments;
* validating Evidence;
* validating Knowledge;
* managing Edge lifecycle.

Those responsibilities remain inside their respective Domain components.

---

# Session Lifecycle

A Research Session follows the lifecycle below.

```text
Created
    ↓
Running
    ↓
Completed
```

If execution cannot continue:

```text
Created
    ↓
Running
    ↓
Failed
```

A completed session is immutable.

---

# Session State

Each Research Session maintains:

* session identifier;
* creation timestamp;
* current status;
* associated HistoricalDataset;
* produced Market Description;
* generated Research Hypotheses;
* executed Experiments;
* collected Evidence;
* generated Knowledge;
* generated Edges.

These objects are owned by the Domain.

The session only references them.

---

# Relationships

The Research Session coordinates the following conceptual workflow.

```text
HistoricalDataset
        ↓
MarketDescriptionBuilder
        ↓
MarketDescription
        ↓
ResearchHypothesis
        ↓
Experiment
        ↓
Evidence
        ↓
Knowledge
        ↓
Edge
```

Every transformation is delegated to existing Domain or Application services.

---

# Public Interface

The Research Session exposes operations required by the Application Layer.

Typical responsibilities include:

* starting execution;
* updating execution status;
* exposing generated artifacts;
* marking completion;
* reporting failure.

No domain calculations are performed directly.

---

# Execution Metadata

The session records execution metadata such as:

* execution timestamps;
* elapsed duration;
* execution status;
* optional execution messages.

Metadata supports reproducibility and diagnostics without affecting Domain behaviour.

---

# Design Principles

The Research Session follows the Foundation principles.

* Domain First
* Clean Boundaries
* Reproducibility by Design
* Evidence Before Opinion
* Simplicity Over Cleverness

The session acts exclusively as an orchestration component.

---

# Out of Scope

The following responsibilities belong to later milestones.

* experiment scheduling;
* pipeline orchestration;
* report generation;
* distributed execution;
* retries and recovery;
* persistence.

---

# Acceptance Criteria

RP-001 is complete when:

* a Research Session represents one complete research execution;
* no business logic is introduced;
* Domain independence is preserved;
* the session maintains execution state;
* produced artifacts are exposed through the session;
* the implementation satisfies the Application Layer architecture defined in RP-000.
