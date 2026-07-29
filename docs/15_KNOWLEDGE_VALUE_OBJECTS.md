# Purpose

This document defines the official domain specification for the Value Objects belonging to the Knowledge Aggregate within EDGE_ENGINE.

The purpose is to describe the domain building blocks that support the meaning, integrity, and lifecycle of Knowledge without prescribing implementation details.

# Overview

Value Objects within the Knowledge Aggregate provide stable, explicit, and constrained domain concepts that support the meaning of Knowledge.

They are used to describe identity, state, evidence relationships, validity conditions, and descriptive context in a way that is consistent with the Knowledge Lifecycle and the Knowledge Aggregate contract.

These Value Objects do not define implementation behavior. They define the domain semantics that future implementation work must respect.

# Value Objects

## KnowledgeId

- Purpose
  - Identify a Knowledge item as a distinct domain entity.

- Responsibilities
  - Preserve uniqueness of Knowledge within the domain context.
  - Support traceability across lifecycle events.
  - Distinguish one Knowledge item from another.

- Immutability
  - KnowledgeId is immutable once assigned.

- Validation Rules
  - It must be unique.
  - It must be stable over time.
  - It must not be reassigned to a different Knowledge item.

- Invariants
  - A KnowledgeId must not be empty.
  - A KnowledgeId must remain consistent across all lifecycle states.
  - A KnowledgeId must remain independent from the Knowledge state.

- Relationships
  - It is the identity anchor of the Knowledge Aggregate.

- Status
  - Confirmed.

## KnowledgeState

- Purpose
  - Represent the current lifecycle state of a Knowledge item.

- Responsibilities
  - Express whether Knowledge is Candidate, Validated, Operational, Deprecated, or Archived.
  - Preserve the relationship between lifecycle state and domain meaning.

- Immutability
  - The state value is immutable as a single state assignment, though the state may change over time through domain transitions.

- Validation Rules
  - The state must be one of the allowed lifecycle states.
  - The state must be compatible with the current lifecycle rules.

- Invariants
  - A KnowledgeState must not represent a state outside the official lifecycle.
  - A KnowledgeState must remain consistent with the Knowledge lifecycle rules.
  - A KnowledgeState must not be used to bypass lifecycle validation.

- Relationships
  - It is linked to the lifecycle contract of the Knowledge Aggregate.

- Status
  - Confirmed.

## Confidence

- Purpose
  - Express the strength or reliability of a Knowledge item as understood within the domain.

- Responsibilities
  - Represent the degree of trust associated with the current knowledge claim.
  - Support the distinction between provisional and established understanding.

- Immutability
  - Confidence should remain stable once a knowledge claim has been accepted into a given lifecycle state, unless a domain transition explicitly changes its standing.

- Validation Rules
  - Confidence must be expressed within an accepted domain range.
  - It must reflect the evidential support available for the claim.

- Invariants
  - Confidence must not be treated as proof.
  - Confidence must not replace evidence.
  - Confidence must remain subordinate to traceability and validation.

- Relationships
  - It supports the interpretation of a Knowledge item without replacing its evidence basis.

- Status
  - Confirmed.

## ValidityPeriod

- Purpose
  - Describe the temporal scope during which a Knowledge item is considered valid for its intended use.

- Responsibilities
  - Define the period in which the Knowledge item is considered relevant and applicable.
  - Support the distinction between current and historical significance.

- Immutability
  - The bounded period is immutable once established for a given knowledge claim.

- Validation Rules
  - The start and end of the validity period must be coherent.
  - A validity period must not contradict the lifecycle state.

- Invariants
  - A validity period must not be open-ended unless explicitly allowed by domain rules.
  - An expired validity period must not imply that the Knowledge item is automatically invalid without review.
  - A validity period must remain compatible with the Knowledge lifecycle.

- Relationships
  - It is related to the operational relevance of Knowledge and to the transition toward deprecation or archival.

- Status
  - Confirmed.

## EvidenceReference

- Purpose
  - Reference the evidence that supports a Knowledge item.

- Responsibilities
  - Preserve the link between Knowledge and the evidence basis that justifies it.
  - Maintain traceability and auditability.

- Immutability
  - The reference to a specific evidence basis should remain stable once recorded.

- Validation Rules
  - An EvidenceReference must point to a recognized evidence basis.
  - It must be meaningful and traceable.

- Invariants
  - An EvidenceReference must not be empty.
  - An EvidenceReference must remain tied to the underlying evidence rather than to a transient interpretation.
  - A Knowledge item must not lose its evidence reference without a domain transition that changes its status.

- Relationships
  - It connects Knowledge to the evidence foundation of the aggregate.

- Status
  - Confirmed.

## KnowledgeMetadata

- Purpose
  - Carry the descriptive context of a Knowledge item without changing its core meaning.

- Responsibilities
  - Preserve context such as provenance, provenance notes, research context, and domain annotations.
  - Support future understanding and reuse.

- Immutability
  - Metadata should be stable once attached to a knowledge claim, unless a domain change explicitly requires an update.

- Validation Rules
  - Metadata must be coherent and relevant to the Knowledge item.
  - Metadata must not contradict the evidence or lifecycle state.

- Invariants
  - Metadata must not replace evidence.
  - Metadata must remain traceable to the Knowledge item it describes.
  - Metadata must not introduce contradictory domain meaning.

- Relationships
  - It enriches Knowledge while remaining subordinate to the aggregate contract.

- Status
  - Confirmed.

# Aggregate Boundaries

The following information belongs to the Knowledge Aggregate:

- the identity of a Knowledge item;
- its lifecycle state;
- its evidence basis;
- its validity and temporal relevance;
- its descriptive metadata;
- its traceability and history.

The following information does not belong to the Knowledge Aggregate:

- implementation-specific storage details;
- runtime execution details;
- infrastructure concerns;
- unrelated domain concepts not required to define Knowledge.

# Business Constraints

- A Knowledge item must not be considered valid solely by virtue of its state label.
- A Knowledge item must remain traceable to evidence throughout its lifecycle.
- A Knowledge item must not be promoted to a more active state without satisfying domain criteria.
- A Knowledge item must preserve its historical record across transitions.
- A Knowledge item must not be treated as operational unless it is validated.

# Future Extensions

Future extensions may refine the semantics of the Value Objects when the domain requires greater precision.

Possible future extensions include:

- richer evidence provenance semantics;
- more explicit confidence frameworks;
- additional lifecycle annotations;
- domain-specific metadata categories.

Any future extension must remain consistent with the Knowledge Aggregate contract and the Knowledge Lifecycle.

# Non Goals

This document does not define:

- implementation strategies;
- Python classes;
- algorithms;
- interfaces;
- persistence mechanisms;
- execution workflows;
- infrastructure concerns.

This document defines only the official domain specification for the Value Objects belonging to the Knowledge Aggregate within EDGE_ENGINE.
