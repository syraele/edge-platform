# EDGE_ENGINE Project Status

Version: 2.0

Status: Active

Last Updated: Foundation v2

---

# Project Overview

Current Phase

**Foundation v2**

Project State

**Stable**

Architecture

**Frozen**

Domain Model

**Frozen**

Foundation Blueprint

**Frozen**

---

# Current Milestone

**MDF-001 — Market Description Framework**

Status

Ready to Start

Objective

Implement the first production-ready bounded context responsible for transforming historical market data into structured market descriptions.

---

# Completed Milestones

## Foundation v1

Status

Completed

Result

Initial project architecture established.

---

## Foundation v2

Status

Completed

Result

Complete architectural redesign and documentation consolidation.

The following documents are approved and considered frozen:

* FOUNDATION_BLUEPRINT.md
* 00_MANIFESTO.md
* 01_ARCHITECTURE.md
* 02_RESEARCH_MODEL.md
* 03_ROADMAP.md
* 04_DOMAIN_MODEL.md
* 05_CODING_STANDARD.md
* 06_TESTING.md
* 07_GIT_WORKFLOW.md
* 08_DECISIONS.md
* 09_GLOSSARY.md

---

# Current Priorities

Priority 1

Implement MDF-001.

Priority 2

Maintain architectural consistency.

Priority 3

Keep the test suite green.

---

# Development Workflow

Every milestone follows the same lifecycle.

```text
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

No implementation starts before design approval.

No milestone is complete until all tests pass.

---

# Architecture Policy

Foundation v2 is considered the authoritative baseline of the project.

During normal development, the Foundation must not be redesigned.

Changes to the Foundation are allowed only if one of the following conditions is met:

- a demonstrated architectural flaw is identified;
- the business domain changes;
- an Architecture Decision Record (ADR) is proposed, reviewed, and accepted.

Otherwise, development proceeds by implementing the current milestone.

---

# Next Action

Start implementation of MDF-001.

The first objective is the design and implementation of the Market Description Framework according to the approved Domain Model.

---

# Assistant Bootstrap

When starting a new conversation:

1. Read this document.
2. Read FOUNDATION_BLUEPRINT.md.
3. Read the document related to the active milestone.
4. Continue implementation without redesigning the Foundation unless explicitly requested.

The default assumption is that the Foundation v2 is the authoritative baseline of the project.
