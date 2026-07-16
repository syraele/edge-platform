# AGENTS.md

Version: 1.3

Status: Active

---

# Mission

Act as an assistant for EDGE_ENGINE using the repository as the only authoritative source of project knowledge.

The repository must always take precedence over chat history.

The assistant must preserve architectural coherence and support the project by following the approved documentation, governance rules, and workflow.

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
7. docs/10_PLATFORM_PRINCIPLES.md

After reading the documents:

* determine the active milestone;
* verify whether a milestone specification exists and is approved;
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

Specification Review & Approval

↓

Test-First Implementation

↓

Regression Test

↓

Documentation Synchronization

↓

Update PROJECT_STATUS.md

↓

Commit

---

# Test-First Implementation

Before implementing a milestone:

1. Read the approved specification.
2. Identify the smallest behavior that must be verified.
3. Add or update a regression test that captures the expected behavior.
4. Run the relevant test and confirm that it fails.
5. Implement the minimum change required to satisfy the specification.
6. Re-run the targeted test and the relevant regression suite.

Implementation must never begin from an undocumented assumption.

---

# Rules

* Foundation v2 is frozen.
* The Domain Model is frozen.
* The roadmap is authoritative.
* The repository is the source of truth.
* No implementation without approval.
* No milestone may proceed to implementation while its specification remains incomplete, ambiguous, or unreviewed.
* Every milestone requires an approved specification.
* A milestone is not ready for implementation if the specification is incomplete or lacks review criteria.
* Every implementation must be testable and traceable to the approved specification.
* No architectural refactoring without an ADR.

---

# Milestone Closure

A milestone is complete only when:

* tests are fully green;
* documentation is synchronized;
* PROJECT_STATUS.md is updated;
* the work is committed;
* the next milestone is prepared or clearly identified.

---

# New Conversations

A new conversation must be able to continue development without relying on prior chat history.

All project knowledge must be recoverable from the repository alone.

The assistant’s role is to preserve continuity, architectural discipline, and review readiness throughout the project lifecycle.
