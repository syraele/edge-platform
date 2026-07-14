# EDGE_ENGINE Project Bootstrap

Version: 2.1

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

- current phase;
- active milestone;
- next objective.

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

Read only the documentation relevant to the active milestone.

Examples:

| Activity | Document |
|----------|----------|
| Architecture | docs/01_ARCHITECTURE.md |
| Research | docs/02_RESEARCH_MODEL.md |
| Domain | docs/04_DOMAIN_MODEL.md |
| Coding | docs/05_CODING_STANDARD.md |
| Testing | docs/06_TESTING.md |

Avoid reading unnecessary documents.

---

## Step 4

Continue from the active milestone.

Do not restart project analysis.

Do not redesign completed Foundation documents.

---

# Working Rules

During normal development:

- Foundation v2 is considered frozen.
- Architectural redesign is not performed.
- Previously approved decisions are treated as authoritative.

If an inconsistency is discovered:

1. Identify the problem.
2. Analyse its impact.
3. Propose an ADR.
4. Apply the minimum required change.

Never redesign the entire architecture because of a local issue.

---

# Development Conventions

Unless explicitly requested otherwise, development follows these conventions.

## Existing Project Structure

Before creating new files or directories, inspect the existing project structure.

Prefer extending the current structure rather than introducing new packages or directories.

Do not duplicate existing project organization.

---

## Test Organization

The project already defines the following structure:

```text
tests/
    unit/
    integration/
    performance/
```

Rules:

- Unit tests belong in `tests/unit`.
- Integration tests belong in `tests/integration`.
- Performance tests belong in `tests/performance`.
- Do not create additional test folders unless explicitly required.

---

## File Updates

When generating implementation:

- Always provide complete files.
- Never provide partial patches.
- Never provide "add these lines".
- Assume the file will be replaced entirely.

---

## Domain-Driven Development

The approved Domain Model drives implementation.

Implement only responsibilities required by the active milestone.

Do not introduce future concepts prematurely.

Avoid speculative design.

---

## Incremental Development

Build the project incrementally.

Future milestones extend previous ones.

Do not anticipate future functionality.

---

# Standard Development Workflow

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

## Repository Discipline

The repository should always remain in a releasable state.

Each completed milestone must leave:

- all tests passing;
- documentation consistent;
- clean Git history;
- stable commit before starting the next milestone.

---

# Conversation Startup Prompt

To resume development in a new conversation, use:

> Read PROJECT_STATUS.md, PROJECT_BOOTSTRAP.md, FOUNDATION_BLUEPRINT.md and the documentation relevant to the active milestone. Treat Foundation v2 as frozen. Follow the documented project conventions. Continue implementation from the active milestone without redesigning the architecture unless explicitly requested or a demonstrated defect requires an ADR.

---

# Success Criterion

A new development session should become productive within a few minutes without reconstructing project history through conversation.

---

# Foundation Freeze Policy

Foundation v2 is the approved architectural baseline.

During normal development the assistant must assume every Foundation document is correct.

The assistant must NOT propose:

- architectural redesigns;
- alternative domain models;
- structural improvements;

unless:

- explicitly requested by the project owner;
- required to fix a demonstrated defect;
- introduced through an ADR.

The default behaviour is implementation, not redesign.