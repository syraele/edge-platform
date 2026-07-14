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
