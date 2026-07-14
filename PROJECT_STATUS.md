# EDGE_ENGINE Project Status

Version: 2.1

Status: Active

Last Updated: RF-002

---

# Project Overview

Current Phase

**Research Framework**

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

**RF-003 — Evidence**

Status

Ready to Start

Objective

Implement the Evidence model according to the approved Domain Model.

---

# Completed Milestones

## Phase 1 — Foundation

### Foundation v1

Status

Completed

Result

Initial project architecture established.

---

### Foundation v2

Status

Completed

Result

Complete architectural redesign and documentation consolidation.

Approved documents:

- FOUNDATION_BLUEPRINT.md
- 00_MANIFESTO.md
- 01_ARCHITECTURE.md
- 02_RESEARCH_MODEL.md
- 03_ROADMAP.md
- 04_DOMAIN_MODEL.md
- 05_CODING_STANDARD.md
- 06_TESTING.md
- 07_GIT_WORKFLOW.md
- 08_DECISIONS.md
- 09_GLOSSARY.md

---

## Phase 2 — Market Description Framework

### MDF-001

Completed

Market Description baseline.

---

### MDF-002

Completed

Descriptor Registry.

---

### MDF-003

Completed

Descriptor Validation.

---

## Phase 3 — Research Framework

### RF-001

Completed

ResearchHypothesis Aggregate.

---

### RF-002

Completed

Experiment Aggregate.

---

# Current Priorities

Priority 1

Implement RF-003.

Priority 2

Maintain architectural consistency.

Priority 3

Keep the regression suite green.

---

# Development Workflow

Every milestone follows:

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

PROJECT_STATUS.md is updated when changing conversation and represents the official project checkpoint.

---

# Architecture Policy

Foundation v2 is the authoritative baseline.

Do not redesign the Foundation during normal development.

Architectural changes require:

- demonstrated defect;
- business change;
- approved ADR.

---

# Next Action

Start RF-003 by implementing the Evidence model.

---

# Assistant Bootstrap

When starting a new conversation:

1. Read PROJECT_STATUS.md.
2. Read PROJECT_BOOTSTRAP.md.
3. Read FOUNDATION_BLUEPRINT.md.
4. Read only the documentation relevant to the active milestone.
5. Continue implementation following the documented workflow.

---

## Assistant Policy

Current objective:

Implement RF-003.

Foundation v2 is frozen.

Implementation takes precedence over architectural discussion unless explicitly requested.