# EDGE_ENGINE Development Workflow

Version: 1.1

Status: Active

---

# Purpose

This document defines the official development workflow adopted by EDGE_ENGINE.

Its objective is to guarantee that every milestone is implemented consistently, reviewed systematically and integrated into the repository without compromising architectural integrity.

This document complements:

* PROJECT_BOOTSTRAP.md
* PROJECT_STATUS.md
* 06_TESTING.md
* 07_GIT_WORKFLOW.md

It does not replace them.

---

# Core Principles

The development process follows these principles.

## Repository First

The repository is the single source of truth.

Existing code must always be inspected before modifications are proposed.

Conversations never override the repository.

---

## Documentation First

Every milestone begins by reading the documentation before writing code.

Documentation drives implementation.

Implementation is allowed only after the active milestone specification has been reviewed and approved.

If no approved specification exists, the milestone remains in the **Specification** phase.

---

## Functional Block Development

Milestones are implemented as coherent functional blocks.

Avoid implementing isolated files independently when they belong to the same responsibility.

---

## One Problem at a Time

Solve one technical problem completely before opening another.

Avoid parallel design discussions while implementation is in progress.

---

# Standard Workflow

Every milestone follows the same workflow.

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
Technical Review
        ↓
Commit
```

---

# Repository Review

Before implementation:

1. Read PROJECT_STATUS.md.
2. Read PROJECT_BOOTSTRAP.md.
3. Read FOUNDATION_BLUEPRINT.md.
4. Read 03_ROADMAP.md.
5. Read the active milestone documentation.
6. Inspect the affected repository area.
7. Inspect existing tests.

Implementation never starts before repository review.

---

# Technical Review

The objective of the review is to understand:

* current architecture;
* existing responsibilities;
* dependencies;
* interactions;
* testing impact.

No redesign is introduced unless objectively required.

---

# Implementation Plan

Before writing code, prepare an implementation plan.

The plan identifies:

* responsibilities;
* files to create;
* files to modify;
* expected tests;
* repository impact.

No implementation starts before the plan has been reviewed.

---

# Milestone Specification

Every milestone requires an approved specification before implementation.

The specification defines:

* purpose;
* responsibilities;
* non-responsibilities;
* architecture placement;
* inputs;
* outputs;
* lifecycle;
* public interfaces;
* acceptance criteria;
* testing expectations.

The specification becomes the authoritative reference for implementation.

Implementation must never introduce responsibilities that are not documented in the approved specification.

---

# Functional Block Implementation

Implement the complete milestone as one coherent block.

Avoid switching continuously between unrelated files.

The objective is architectural consistency.

---

# Regression Testing

Every milestone executes the complete regression suite.

A milestone is complete only when all tests pass.

Regression is mandatory before every commit.

---

# Documentation Synchronization

Documentation is part of the implementation.

Before closing a milestone:

* update PROJECT_STATUS.md;
* update milestone documentation if required;
* synchronize process documentation if necessary;
* ensure repository documentation reflects the implemented architecture.

---

# Next Milestone Preparation

A milestone is not considered fully complete until the next milestone has been prepared.

Preparation includes:

* identifying the next active milestone;
* writing its complete Milestone Specification;
* reviewing and approving the specification;
* updating PROJECT_STATUS.md accordingly.

The objective is that every new development conversation starts with a milestone already **Ready to Implement**.

---

# Commit Policy

One milestone corresponds to one coherent commit whenever practical.

Commits should contain only changes directly related to the milestone.

Process documentation may be committed separately when appropriate.

---

# Review Checklist

Before committing:

* implementation complete;
* tests green;
* documentation synchronized;
* next milestone specification prepared;
* exports updated;
* repository consistent;
* no temporary files;
* no debug code.

---

# Conversation Workflow

When starting a new conversation:

1. Read PROJECT_STATUS.md.
2. Read PROJECT_BOOTSTRAP.md.
3. Read DEVELOPMENT_WORKFLOW.md.
4. Read FOUNDATION_BLUEPRINT.md.
5. Read 03_ROADMAP.md.
6. Read the active milestone specification.
7. Review the affected repository area.
8. Produce an implementation plan.
9. Obtain approval.
10. Implement the milestone.

---

# Lessons Learned

The development workflow evolved during the implementation of the Foundation and early Research milestones.

Key lessons include:

* inspect existing code before modifying it;
* implement complete functional blocks;
* keep documentation synchronized with implementation;
* never implement a milestone without an approved specification;
* prepare the next milestone before closing the current one;
* preserve repository consistency at every milestone;
* allow the repository to guide development decisions.

---

# Governance

This workflow applies to every future milestone unless explicitly superseded by approved project documentation.

Repository consistency always takes precedence over conversational context.

No milestone may enter the implementation phase without an approved Milestone Specification.
