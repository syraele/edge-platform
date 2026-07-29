# Knowledge Lifecycle

## Purpose

This document defines the official lifecycle of Knowledge within EDGE_ENGINE.

Its purpose is to preserve the integrity, traceability, and reusability of knowledge as it evolves from initial formulation to long-term preservation.

The lifecycle is intended to support the platform’s mission of accumulating validated quantitative knowledge without weakening the discipline of evidence, reproducibility, or scientific rigor.

## Definition of Knowledge

Knowledge is a validated understanding that has been established through evidence and accepted as reusable insight.

Knowledge is not an observation.

Knowledge is not raw evidence.

Knowledge is not a hypothesis.

Knowledge becomes meaningful when it is grounded in evidence, is traceable to its supporting basis, and is suitable for reuse in future research.

## Knowledge States

### Candidate

#### Definition

A Candidate is a knowledge claim that has been proposed but has not yet been accepted as validated knowledge.

#### Entry Conditions

A knowledge item enters the Candidate state when it is proposed from evidence or from a research outcome that is still under review.

#### Exit Conditions

A Candidate exits this state when it is validated, rejected, or archived.

#### Allowed Transitions

- Candidate → Validated
- Candidate → Archived

#### Invariants

A Candidate MUST remain explicitly provisional.

A Candidate MUST remain traceable to its originating evidence or research context.

A Candidate MUST NOT be treated as established knowledge.

### Validated

#### Definition

A Validated knowledge item is a knowledge claim that has been accepted as sufficiently supported by evidence and suitable for reuse.

#### Entry Conditions

A knowledge item enters the Validated state when it has satisfied the applicable validation criteria and has been accepted as a durable research outcome.

#### Exit Conditions

A Validated knowledge item exits this state when it becomes operational, deprecated, or archived.

#### Allowed Transitions

- Validated → Operational
- Validated → Deprecated
- Validated → Archived

#### Invariants

A Validated knowledge item MUST remain grounded in evidence.

A Validated knowledge item MUST remain traceable to the evidence that supports it.

A Validated knowledge item MUST remain distinguishable from preliminary or superseded claims.

### Operational

#### Definition

An Operational knowledge item is validated knowledge that is currently considered active and reusable in ongoing research.

#### Entry Conditions

A knowledge item enters the Operational state when it is validated and is actively used as a dependable foundation for future research.

#### Exit Conditions

An Operational knowledge item exits this state when it becomes deprecated or archived.

#### Allowed Transitions

- Operational → Deprecated
- Operational → Archived

#### Invariants

An Operational knowledge item MUST remain relevant to the research context in which it is used.

An Operational knowledge item MUST remain consistent with current evidence and accepted understanding.

An Operational knowledge item MUST remain suitable for reuse.

### Deprecated

#### Definition

A Deprecated knowledge item is knowledge that is no longer considered current, preferred, or appropriate for continued use.

#### Entry Conditions

A knowledge item enters the Deprecated state when it is superseded, weakened by newer evidence, or no longer appropriate for active use.

#### Exit Conditions

A Deprecated knowledge item exits this state when it is archived or revalidated.

#### Allowed Transitions

- Deprecated → Archived
- Deprecated → Validated

#### Invariants

A Deprecated knowledge item MUST retain its provenance and reason for deprecation.

A Deprecated knowledge item MUST remain distinguishable from active knowledge.

A Deprecated knowledge item MUST NOT be treated as current without explicit revalidation.

### Archived

#### Definition

An Archived knowledge item is knowledge retained for historical record, audit, or reference rather than active use.

#### Entry Conditions

A knowledge item enters the Archived state when it is no longer active and is preserved for continuity or review.

#### Exit Conditions

An Archived knowledge item exits this state only through explicit review and reactivation.

#### Allowed Transitions

- Archived → Validated

#### Invariants

An Archived knowledge item MUST preserve its full history.

An Archived knowledge item MUST remain traceable to its earlier state and supporting evidence.

An Archived knowledge item MUST remain clearly separated from active knowledge.

## State Transition Rules

A knowledge item may transition only through explicit and documented state changes.

State transitions MUST preserve traceability and provenance.

A transition MUST not erase the history of the knowledge item.

Knowledge MUST NOT move directly from Candidate to Operational without passing through validation.

Knowledge MUST NOT move from Validated to Operational without being recognized as appropriate for reuse.

Knowledge MUST NOT be reintroduced as active knowledge without review.

## Knowledge Validation

Knowledge validation is the process by which a knowledge claim is assessed for readiness to become validated knowledge.

Validation requires that the knowledge claim be:

- grounded in evidence;
- traceable to its supporting basis;
- consistent with the broader research context;
- reproducible in the sense that its claim can be examined and understood;
- suitable for reuse in future research.

Validation is not a declaration of permanence.

Validation establishes that the knowledge is acceptable for its current role and scope.

## Knowledge Invalidations

Knowledge may become invalid or unsuitable when:

- newer evidence contradicts it;
- its original evidence is shown to be insufficient;
- its scope is exceeded;
- its conditions of validity no longer hold;
- it can no longer be reproduced or defended with traceability.

When invalidation occurs, the knowledge item MUST be moved to a less active state, typically Deprecated or Archived, and its reason for change MUST be preserved.

## Knowledge History

Every knowledge item MUST maintain a history of its lifecycle.

The history MUST preserve:

- the original proposal or emergence of the knowledge claim;
- the evidence or context supporting it;
- each state transition;
- the reason for each transition;
- the point at which it was considered validated, operational, deprecated, or archived.

Knowledge history is essential for continuity, auditability, and reproducibility.

## Non Goals

This document does not define:

- implementation strategies;
- software classes;
- algorithms;
- interfaces;
- storage mechanisms;
- execution workflows.

This document defines only the official lifecycle of Knowledge within EDGE_ENGINE.
