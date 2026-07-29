# Knowledge Aggregate

## Purpose

This document defines the official domain specification for the Knowledge Aggregate within EDGE_ENGINE.

The purpose of this specification is to establish the domain contract that governs Knowledge as a coherent, traceable, and reusable unit of research value.

The Knowledge Aggregate exists to preserve the integrity of validated understanding as it evolves through the Knowledge Lifecycle and becomes part of the platform’s accumulated research foundation.

## Aggregate Root

Knowledge is the Aggregate Root because it is the authoritative domain concept that unifies the meaning, validity, and lifecycle of a unit of research understanding.

Knowledge represents the stable point at which evidence, interpretation, and reuse converge.

As the Aggregate Root, Knowledge governs the domain rules that determine whether a claim is provisional, validated, operational, deprecated, or archived.

## Identity

Knowledge has a domain identity that distinguishes one knowledge item from another.

The identity of a Knowledge item must be:

- unique within the domain context;
- stable over time;
- independent from its current lifecycle state;
- preserved even when the knowledge item becomes deprecated or archived.

The identity of a Knowledge item must not change merely because its state changes.

The identity must remain immutable once a Knowledge item is created.

## Responsibilities

The Knowledge Aggregate governs the domain meaning of Knowledge.

Its responsibilities include:

- preserving the integrity of a knowledge claim as a unit of domain meaning;
- maintaining the relationship between Knowledge and the evidence that supports it;
- enforcing the lifecycle states defined by the Knowledge Lifecycle;
- preserving traceability across validation, promotion, deprecation, and archival;
- ensuring that Knowledge remains reusable and trustworthy within the research process.

The Knowledge Aggregate does not define implementation behavior. It defines the domain contract that must be respected by future implementation work.

## State Model

The Knowledge Aggregate adopts the official Knowledge Lifecycle.

The lifecycle states are:

- Candidate
- Validated
- Operational
- Deprecated
- Archived

A Knowledge item progresses through these states according to domain rules and must preserve its full history throughout the lifecycle.

## Invariants

All Knowledge items must satisfy the following invariants.

- A Knowledge item must have at least one Evidence basis.
- A Knowledge item must remain traceable to the evidence that supports it.
- A Knowledge Operational must be Validated.
- A Knowledge Archived must be immutable with respect to its domain meaning and prior state history.
- No transition may violate the Knowledge Lifecycle.
- A Knowledge item must not be treated as active knowledge while it is Candidate.
- A Knowledge item must not be treated as current knowledge while it is Deprecated.
- A Knowledge item must preserve its identity across all lifecycle states.
- A Knowledge item must preserve its provenance and history across all lifecycle states.
- A Knowledge item must remain distinguishable from raw evidence, unvalidated claims, and speculative conclusions.
- A Knowledge item must remain suitable for reuse only when it is in an appropriate lifecycle state.
- A Knowledge item must not be reactivated without explicit review and revalidation when appropriate.

## Domain Commands

The following domain commands define the official business operations for the Knowledge Aggregate.

- Create Knowledge
- Validate Knowledge
- Promote Knowledge
- Deprecate Knowledge
- Archive Knowledge

Each command expresses a domain action that changes the state or status of a Knowledge item within the aggregate.

## Domain Events

The following domain events are produced by the Knowledge Aggregate.

- KnowledgeCreated
- KnowledgeValidated
- KnowledgePromoted
- KnowledgeDeprecated
- KnowledgeArchived

Each event represents a meaningful domain change and contributes to the historical record of the Knowledge item.

## Business Rules

The Knowledge Aggregate must obey the following business rules.

- Knowledge may only be created from a domain claim that is grounded in evidence.
- Knowledge may not become Validated unless it is supported by sufficient evidence and is suitable for reuse.
- Knowledge may not become Operational unless it is already Validated.
- Knowledge may not be promoted to active reuse without satisfying the validation and lifecycle criteria.
- Knowledge may be Deprecated when it is superseded, weakened, or no longer appropriate for current use.
- Knowledge may be Archived when it is no longer active and must be preserved for historical reference.
- Knowledge must retain its history regardless of its current state.
- Knowledge must remain traceable and reproducible in its domain meaning.
- Knowledge must not be discarded merely because it becomes less active.

## Consistency Rules

The Knowledge Aggregate must remain consistent in the following ways.

- The lifecycle state must always be consistent with the current domain meaning of the Knowledge item.
- The evidence basis must remain consistent with the knowledge claim.
- The identity of the Knowledge item must remain stable.
- The historical record must remain complete and coherent.
- State transitions must remain compatible with the Knowledge Lifecycle.
- The aggregate must preserve the distinction between active, inactive, and historical knowledge.

## Non Goals

This specification does not define:

- software implementation details;
- Python classes;
- algorithms;
- interfaces;
- persistence mechanisms;
- execution workflows;
- infrastructure concerns.

This document defines only the official domain specification for the Knowledge Aggregate within EDGE_ENGINE.
