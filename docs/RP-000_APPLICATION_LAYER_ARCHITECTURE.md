# RP-000 — Application Layer Architecture

---

## Objective

Define the Application Layer that orchestrates the Domain without modifying it.

The Foundation remains frozen.

The Domain remains frozen.

The Application Layer coordinates the research workflow.

---

# Architectural Vision

The Application Layer sits above the Domain and is responsible for executing use cases.

It never contains domain rules.

It never replaces the Domain.

It only coordinates Domain objects.

Architecture:

Infrastructure

?

Application Layer

?

Domain

?

Historical Dataset

---

# Responsibilities

## Domain

Responsible for:

- Entities
- Value Objects
- Aggregates
- Domain Services
- Business Rules
- Domain Invariants

The Domain does NOT know:

- workflows
- pipelines
- sessions
- orchestration
- infrastructure

---

## Application Layer

Responsible for:

- coordinating the research workflow
- executing use cases
- creating Domain objects
- invoking Domain services
- collecting results
- managing execution flow

The Application Layer must NOT implement:

- market rules
- quantitative logic
- scoring algorithms
- business invariants

Those belong to the Domain.

---

# Dependency Rules

Application Layer

?

Domain

?

Shared Kernel

The Domain must never depend on the Application Layer.

The Application Layer may depend on the Domain.

Infrastructure supports the Application Layer but never contains business rules.

---

# Initial Research Pipeline

HistoricalDataset

?

MarketDescriptionBuilder

?

ResearchHypothesis

?

Experiment

?

ResearchEvaluator

?

KnowledgeCollection

?

Edge

The pipeline orchestrates existing Domain components.

It does not replace them.

---

# Package Structure

src/

edge/

application/

research/

pipeline/

session/

runner/

report/

The Application Layer is completely separated from the Domain.

---

# Future Milestones

RP-001

Research Session

RP-002

Experiment Runner

RP-003

Research Pipeline

RP-004

Pipeline Report

Each milestone introduces a single responsibility.

---

# Guiding Principles

The Domain owns the business.

The Application owns the workflow.

The Infrastructure owns technical concerns.

Every new feature must preserve this separation.

Foundation v2 remains the authoritative architectural baseline.
