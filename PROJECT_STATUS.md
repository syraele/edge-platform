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

MDF-001 — Market Description Framework

Status

Completed

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

Implemented the Market Understanding bounded context baseline.

Completed:

- MarketDescription Aggregate
- MarketDescriptor Value Object
- DescriptorMetadata Value Object
- MarketDescriptionBuilder Domain Service

All tests passing.

---

# Current Priorities

Priority 1

Start next milestone.

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
## Assistant Policy

Current objective:

Implement MDF-001.

The Foundation is frozen.

Discussion about alternative architectures is out of scope unless explicitly requested.

# EDGE_ENGINE Project Bootstrap

Version: 2.0

Status: Foundation v2

---

# Purpose

This document defines the bootstrap procedure for starting or resuming work on EDGE_ENGINE.

Its purpose is to ensure that every development session begins from the current project state rather than reconstructing context through conversation.

---

# Bootstrap Procedure

Every new development session follows the same procedure.

## Step 1

Read:

```text
PROJECT_STATUS.md
```

Determine:

* current phase;
* active milestone;
* next objective.

---

## Step 2

Read:

```text
FOUNDATION_BLUEPRINT.md
```

Understand the conceptual foundation of the project.

The Blueprint is the highest-level architectural reference.

---

## Step 3

Read only the document relevant to the current task.

Examples:

| Activity     | Document                   |
| ------------ | -------------------------- |
| Architecture | docs/01_ARCHITECTURE.md    |
| Research     | docs/02_RESEARCH_MODEL.md  |
| Domain       | docs/04_DOMAIN_MODEL.md    |
| Coding       | docs/05_CODING_STANDARD.md |
| Testing      | docs/06_TESTING.md         |

Avoid reading unnecessary documents.

---

## Step 4

Continue from the current milestone.

Do not restart project analysis.

Do not redesign completed Foundation documents.

---

# Working Rules

During normal development:

* Foundation v2 is considered frozen.
* Architectural redesign is not performed.
* Previously approved decisions are treated as authoritative.

If an inconsistency is discovered:

1. identify the problem;
2. analyse its impact;
3. propose an ADR;
4. apply the minimum required change.

Never redesign the entire architecture because of a local issue.

---

# Standard Development Workflow

Every milestone follows the same lifecycle.

```text
Review Current State
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

---

# Conversation Startup Prompt

To resume development in a new conversation, use:

> Read `PROJECT_STATUS.md`, `FOUNDATION_BLUEPRINT.md`, and the documentation relevant to the active milestone. Treat Foundation v2 as the approved baseline and continue implementation from the current milestone without redesigning the architecture unless explicitly requested.

---

# Success Criterion

A new development session should become productive within a few minutes, without reconstructing project history through conversation.

## Foundation Freeze Policy

Foundation v2 is the approved architectural baseline.

During normal development the assistant must assume that every Foundation document is correct.

The assistant must NOT propose architectural redesigns, alternative domain models, or structural improvements unless:

- explicitly requested by the project owner;
- required to fix a demonstrated defect;
- introduced through an Architecture Decision Record (ADR).

The default behavior is implementation, not redesign.
