# Purpose

This document defines the official Domain Map of EDGE_ENGINE.

Its purpose is to identify the core domain concepts, their boundaries, and the relationships that preserve coherence across the platform’s research process.

The Domain Map is necessary because it establishes the shared understanding of the domain before implementation decisions are made.

# Domain Overview

EDGE_ENGINE is a research platform whose purpose is to transform observations into validated knowledge and, ultimately, into reusable edges.

The logical flow of the domain is:

Observation → Dataset → Market Description → Hypothesis → Experiment → Evidence → Knowledge → Edge

This flow describes the progression of meaning within the domain.

It is not an implementation workflow and it does not prescribe technical execution.

# Core Aggregates

## Observation

- Purpose
  - Represent a recorded fact that can serve as input for research.

- Responsibilities
  - Preserve factual content.
  - Remain distinct from interpretation and conclusion.

- Owned Concepts
  - Observation content.
  - Traceability to source context.

- Lifecycle Ownership
  - Observation is not treated as an Aggregate Root in the main lifecycle model. It is a foundational domain concept that supports higher-level aggregates.

## Dataset

- Purpose
  - Organize observations into a coherent body of evidence for research.

- Responsibilities
  - Preserve internal coherence.
  - Provide the domain basis for market description and hypothesis formation.

- Owned Concepts
  - Observation collection.
  - Dataset context.
  - Traceability.

- Lifecycle Ownership
  - Dataset is a domain aggregate because it owns a coherent body of evidence and governs its integrity as a unit.

## MarketDescription

- Purpose
  - Interpret a dataset within the relevant market context.

- Responsibilities
  - Provide structured domain understanding.
  - Connect observations to a meaningful market framing.

- Owned Concepts
  - Market interpretation.
  - Contextual framing.
  - Relationship to a dataset.

- Lifecycle Ownership
  - MarketDescription is a domain aggregate because it governs a coherent interpretation of a dataset.

## Hypothesis

- Purpose
  - Express a testable proposition for research.

- Responsibilities
  - Preserve testability and explicitness.
  - Remain distinct from validated knowledge.

- Owned Concepts
  - Proposition.
  - Evaluation intent.
  - Relationship to market description.

- Lifecycle Ownership
  - Hypothesis is an aggregate because it governs a distinct research proposition and its state of evaluation.

## Experiment

- Purpose
  - Evaluate a hypothesis under controlled conditions.

- Responsibilities
  - Preserve the relationship between a hypothesis and the conditions under which it is tested.
  - Produce evidence.

- Owned Concepts
  - Experimental context.
  - Evaluation criteria.
  - Evidence outcome.

- Lifecycle Ownership
  - Experiment is an aggregate because it governs a coherent evaluation process and its resulting evidence.

## Evidence

- Purpose
  - Record the outcome of an experiment that supports or refutes a hypothesis.

- Responsibilities
  - Preserve traceability to the experiment that produced it.
  - Remain distinct from interpretation and final knowledge.

- Owned Concepts
  - Evidence content.
  - Supporting relationship to experiment and hypothesis.

- Lifecycle Ownership
  - Evidence is an aggregate because it represents a distinct domain unit that must preserve integrity and provenance.

## Knowledge

- Purpose
  - Preserve validated and reusable understanding derived from evidence.

- Responsibilities
  - Govern the lifecycle of validated understanding.
  - Preserve evidence basis and traceability.
  - Support reuse in future research.

- Owned Concepts
  - Knowledge identity.
  - Knowledge state.
  - Evidence relationship.
  - Metadata and validity context.

- Lifecycle Ownership
  - Knowledge is an Aggregate Root because it governs the lifecycle of validated understanding and the rules that determine its active, deprecated, or archived status.

## Edge

- Purpose
  - Represent a validated and reusable insight that provides a meaningful advantage.

- Responsibilities
  - Preserve the durability and relevance of a research outcome.
  - Distinguish validated insight from raw evidence or tentative knowledge.

- Owned Concepts
  - Edge value.
  - Supporting knowledge.
  - Validation context.

- Lifecycle Ownership
  - Edge is an aggregate because it governs a meaningful domain result that must remain traceable and reusable.

## ResearchSession

- Purpose
  - Organize research activity around a coherent purpose.

- Responsibilities
  - Coordinate the relationship among research concepts.
  - Preserve boundedness and traceability of research work.

- Owned Concepts
  - Research intent.
  - Related aggregates.
  - Session history.

- Lifecycle Ownership
  - ResearchSession is a domain aggregate because it governs a cohesive and bounded unit of research work.

## Notes on Non-Aggregates

Some concepts are not treated as aggregates because they serve as foundational or descriptive elements rather than as autonomous units of domain authority.

Examples include:

- Observation, which supports higher-level aggregates but does not govern a complete lifecycle on its own.
- MarketDescription, although meaningful, is considered a bounded interpretation unit and may be treated as an aggregate only if its own lifecycle and invariants need to be explicitly modeled.

The distinction should be made on the basis of whether the concept owns independent invariants and lifecycle rules.

# Aggregate Relationships

The aggregates collaborate through controlled relationships.

## Allowed Relationships

- A Dataset may contain many Observations.
- A MarketDescription is derived from a Dataset.
- A Hypothesis is formed from a MarketDescription.
- An Experiment evaluates a Hypothesis.
- An Experiment produces Evidence.
- Evidence supports the creation of Knowledge.
- Knowledge may support the creation of an Edge.
- A ResearchSession contains and organizes the related aggregates involved in a coherent investigation.

## Dependency Rules

- Higher-level aggregates may depend on lower-level domain concepts for meaning, but they must not depend on implementation details.
- Knowledge should not depend on unrelated domain objects outside its evidence basis and lifecycle context.
- Evidence should remain traceable to the Experiment that produced it.
- Hypothesis should remain distinct from validated Knowledge.
- ResearchSession may coordinate other aggregates, but it should not absorb their internal lifecycle rules.

## Boundaries of Awareness

- Knowledge may know about the evidence that supports it.
- Evidence may know about the experiment that produced it.
- Experiment may know about the hypothesis it evaluates.
- Hypothesis may know about the market description from which it was formed.
- ResearchSession may coordinate multiple aggregates without owning their internal invariants.

- Aggregates should not directly depend on unrelated external concerns such as infrastructure, execution mechanics, or presentation details.

# Domain Services

Domain services are used when a capability requires coordination across aggregates but does not belong to a single aggregate.

Examples of domain services include:

- validation services for determining whether a knowledge claim is acceptable;
- evaluation services for assessing whether evidence supports a hypothesis;
- lifecycle coordination services for moving knowledge through its states.

These services exist to preserve domain coherence and to avoid overloading aggregates with cross-aggregate responsibilities.

# Domain Events

The following events are central to the domain flow:

- ObservationRecorded
- DatasetComposed
- MarketDescriptionFormed
- HypothesisCreated
- ExperimentStarted
- EvidenceProduced
- KnowledgeCreated
- KnowledgeValidated
- KnowledgePromoted
- KnowledgeDeprecated
- KnowledgeArchived
- EdgeFormed
- ResearchSessionStarted
- ResearchSessionCompleted

These events represent meaningful domain changes and contribute to the historical record of the research process.

# Aggregate Boundaries

Each aggregate must preserve clear boundaries.

## Dataset

- Owns the collection of observations that constitute a coherent evidence basis.
- Does not own the meaning assigned by a hypothesis or market description.

## MarketDescription

- Owns the interpretation of a dataset within a market context.
- Does not own the evidence or the experimental evaluation process.

## Hypothesis

- Owns the proposition under review.
- Does not own the evidence that validates or refutes it.

## Experiment

- Owns the evaluation process and its contextual conditions.
- Does not own the broader research session or unrelated aggregates.

## Evidence

- Owns the recorded outcome of an experiment.
- Does not own the broader interpretation of that outcome beyond its domain meaning.

## Knowledge

- Owns the lifecycle and integrity of validated understanding.
- Does not own external implementation concerns or unrelated domain concepts.

## Edge

- Owns the validated insight that becomes reusable research value.
- Does not own the proof process behind every supporting knowledge item.

## ResearchSession

- Owns the bounded coordination of related research activity.
- Does not replace the internal rules of the aggregates it contains.

# Design Principles

The domain should remain coherent by following these principles:

- Domain first: the domain structure must remain central.
- Clear boundaries: aggregates must own only what belongs to them.
- Traceability: each domain outcome must remain linked to its supporting basis.
- Reusability: validated knowledge and edges must remain available for future research.
- Lifecycle discipline: state changes must remain compatible with the domain lifecycle.
- Explicit ownership: each aggregate must own its invariants and responsibilities.

# Future Evolution

The Domain Map may evolve as the platform grows.

Potential future aggregates may include:

- ResearchPortfolio
- EvidenceSet
- KnowledgeCollection
- ValidationReport
- DiscoveryOutcome

These future aggregates should be introduced only when they own distinct invariants and domain responsibilities.

# Non Goals

This document does not define:

- implementation strategies;
- code structure;
- class design;
- database design;
- infrastructure concerns;
- execution workflows.

This document defines only the official Domain Map of EDGE_ENGINE.
