# TM-001 — Testing Infrastructure

Version: 1.0

Status: Design

Phase: Technical Infrastructure

---

# Purpose

The Testing Infrastructure provides reusable components for writing clean, consistent and maintainable tests.

Its purpose is to reduce duplicated setup code while keeping production code completely independent from testing concerns.

The Testing Infrastructure belongs exclusively to the test suite.

---

# Objectives

The Testing Infrastructure aims to:

* reduce duplicated test setup;
* improve readability;
* standardize Domain object creation;
* simplify future unit tests;
* preserve production code purity.

---

# Responsibilities

The Testing Infrastructure is responsible for providing reusable builders and testing utilities.

Typical responsibilities include:

* creating valid Domain objects;
* creating valid datasets;
* creating valid Market Descriptions;
* creating valid Research objects;
* exposing a simple public testing API.

---

# Non-Responsibilities

The Testing Infrastructure is not responsible for:

* modifying production code;
* replacing Domain validation;
* mocking business logic;
* executing research workflows;
* testing integration behaviour.

---

# Structure

The initial structure is:

```text
tests/
│
├── builders/
│      __init__.py
│      dataset_builder.py
│      market_description_builder.py
│      domain_builder.py
│
├── helpers.py
│
└── unit/
```

The structure may evolve in future technical milestones.

---

# Public API

Tests should import builders from the package root whenever possible.

Example:

```python
from tests.builders import create_test_experiment
```

Internal module organization should remain transparent to test files.

---

# Builder Principles

Builders must:

* use real Domain constructors;
* create valid Domain objects;
* avoid hidden behaviour;
* remain deterministic;
* expose sensible defaults while allowing future extension.

Builders must never bypass Domain validation.

---

# Design Principles

The Testing Infrastructure follows the same principles as the Foundation.

* Repository First
* Simplicity
* Explicit Construction
* No Production Impact
* Reusability
* Readability

---

# Out of Scope

This milestone does not introduce:

* performance testing;
* benchmark tooling;
* integration fixtures;
* mock frameworks;
* automatic data generation;
* property-based testing.

These capabilities belong to future technical milestones.

---

# Acceptance Criteria

TM-001 is complete when:

* reusable builders exist for the most common Domain objects;
* duplicated setup is reduced in existing unit tests;
* production code remains unchanged;
* all tests continue to pass;
* the Testing Infrastructure is documented and reusable.
