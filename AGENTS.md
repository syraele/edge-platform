# AGENTS.md

Version: 1.2

Status: Active

---

# Mission

Act as an assistant for EDGE_ENGINE using the repository as the only authoritative source of project knowledge.

The repository must always take precedence over chat history.

The assistant must preserve architectural coherence and support the project by following the approved documentation and workflow.

---

# Repository First

Always start from the repository.

Do not rely on previous conversation memory as a source of truth.

When a new conversation begins, reconstruct the context from the repository before acting.

---

# Bootstrap

Read the documentation in this order:

1. PROJECT_STATUS.md
2. PROJECT_BOOTSTRAP.md
3. docs/DEVELOPMENT_SETUP.md
4. docs/DEVELOPMENT_WORKFLOW.md
5. FOUNDATION_BLUEPRINT.md
6. docs/03_ROADMAP.md

After reading the documents:

* determine the active milestone;
* read the milestone documentation;
* inspect the relevant code and tests.

---

# Operating Workflow

Every milestone must follow this sequence:

Repository Review

↓

Technical Review

↓

Implementation Plan

↓

Wait for user approval

↓

Implementation

↓

Regression Test

↓

Documentation Synchronization

↓

Update PROJECT_STATUS.md

↓

Commit

---

# Rules

* Foundation v2 is frozen.
* The Domain Model is frozen.
* The roadmap is authoritative.
* The repository is the source of truth.
* No implementation without approval.
* Every milestone requires an approved specification.
* No architectural refactoring without an ADR.

---

# Milestone Closure

A milestone is complete only when:

* tests are fully green;
* documentation is synchronized;
* PROJECT_STATUS.md is updated;
* the work is committed.

---

# New Conversations

A new conversation must be able to continue development without relying on prior chat history.

All project knowledge must be recoverable from the repository alone.
