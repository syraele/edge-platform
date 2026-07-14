# EDGE_ENGINE Git Workflow

Version: 2.0

Status: Foundation v2

---

# Purpose

This document defines the Git workflow adopted by EDGE_ENGINE.

Its objective is to ensure a clean, traceable, and reproducible development history.

---

# Development Model

EDGE_ENGINE follows a trunk-based development model.

The main branch always represents a stable state of the project.

Development progresses through small, incremental commits.

---

# Development Cycle

Every implementation follows the same lifecycle.

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
```

Code is committed only after tests successfully pass.

---

# Commit Principles

Every commit should:

* represent one logical change;
* leave the project in a working state;
* preserve a green test suite;
* be understandable without additional context.

Avoid mixing unrelated changes in the same commit.

---

# Commit Messages

Commit messages follow the Conventional Commits specification.

Examples:

* feat(domain): add MarketDescription aggregate
* feat(research): implement hypothesis validation
* fix(core): preserve aggregate invariant
* refactor(application): simplify experiment workflow
* docs(manifesto): rewrite Foundation v2 manifesto
* test(domain): add Experiment aggregate tests

---

# Branch Strategy

The default branch is the stable branch.

Feature branches may be used for large milestones, but should remain short-lived.

Long-running branches should be avoided.

---

# Tags

Tags identify significant project milestones.

Typical examples include:

* foundation-v2.0
* mdf-001
* mdf-002

Tags represent stable, review-approved project states.

---

# Pull Request Review

Before integration, every change should verify:

* architecture consistency;
* domain consistency;
* coding standards;
* successful automated tests;
* documentation updates when required.

---

# Definition of Ready

Implementation starts only after:

* requirements are understood;
* design is approved;
* architecture impact is evaluated.

---

# Definition of Done

A milestone is complete only when:

* implementation is complete;
* tests pass;
* documentation is updated;
* review is completed;
* changes are committed.

---

# Governance

Git history is considered part of the project documentation.

Every commit should contribute to telling the evolution of the project in a clear and traceable manner.
