# Purpose

This document analyzes the role of ResearchSession within the domain of EDGE_ENGINE.

Its purpose is to evaluate whether ResearchSession is sufficient to represent the full research process or whether the domain would benefit from a broader concept that captures the larger purpose, continuity, and governance of research work.

The analysis is domain-focused and does not prescribe implementation choices.

# Current Model Analysis

ResearchSession currently serves as the bounded unit that organizes research activity around a coherent purpose.

In the current model, it acts as a coordination container for the research flow that connects observations, datasets, hypotheses, experiments, evidence, knowledge, and edges.

This role is meaningful because it gives the domain a unit of work that is coherent, bounded, and traceable.

Its strengths are:

- it expresses a clear unit of research activity;
- it preserves continuity across related domain artifacts;
- it supports the idea of a contained investigation;
- it helps keep the research process understandable.

Its limitations are:

- it is oriented toward coordination rather than the full meaning of the research effort;
- it does not by itself represent the larger objective that unifies multiple sessions, experiments, and knowledge outcomes;
- it does not clearly capture the long-term accumulation of knowledge across repeated research activity.

# Gap Analysis

ResearchSession is useful, but the domain appears to require a broader concept when the research effort exceeds a single bounded activity.

The main gaps are:

- ResearchSession does not fully represent the overarching purpose of an investigation over time.
- It does not clearly own the continuity of a research initiative that may span multiple sessions, multiple experiments, and multiple knowledge outcomes.
- It does not sufficiently capture the distinction between an execution unit and the broader research endeavor that produces validated understanding.
- It does not fully express the long-term accumulation of knowledge that is central to the manifesto and blueprint.

In other words, ResearchSession is appropriate as a coordination concept, but it may be too narrow to represent the full domain meaning of a research program.

# Research Lifecycle

A research effort in EDGE_ENGINE is not limited to one single act of evaluation.

The domain lifecycle of research is better understood as a progression that includes:

- an initial intention or research question;
- the formulation of a hypothesis or exploration direction;
- the execution of experiments and collection of evidence;
- the validation and interpretation of results;
- the transformation of evidence into knowledge;
- the reuse of knowledge and the possible formation of edges;
- the preservation of the research legacy for future work.

This lifecycle is broader than a single session. It spans multiple moments of inquiry and multiple domain outcomes.

ResearchSession can represent one moment within that lifecycle, but it does not fully represent the whole lifecycle itself.

# Relationship with

## Hypothesis

ResearchSession can contain and organize hypotheses, but it does not own the meaning of a hypothesis itself.

A hypothesis remains a distinct domain proposition. ResearchSession provides context and coordination, not hypothesis authority.

## Experiment

ResearchSession can coordinate experiments, but it should not absorb their internal evaluation role.

Experiment remains the bounded domain act of testing a hypothesis.

## Evidence

ResearchSession can gather and relate evidence, but evidence remains tied to the experiment and hypothesis that produced it.

ResearchSession can preserve traceability, but not replace evidence ownership.

## Knowledge

This is the strongest relationship.

ResearchSession can contribute to the creation and organization of Knowledge, but Knowledge itself owns the lifecycle of validated understanding.

A broader research concept would help represent the accumulation of knowledge over time, while ResearchSession remains a more local coordination unit.

## Edge

ResearchSession can support the emergence of edges by organizing the context of research outcomes.

However, an edge is a durable research result that should remain distinct from the operational container that supported its formation.

# Alternative Models

## Option 1: Keep only ResearchSession

### Advantages

- Preserves simplicity.
- Keeps the domain model compact.
- Avoids introducing a new abstraction that may be unclear.

### Disadvantages

- It may underrepresent the broader purpose of research.
- It may blur the distinction between an execution unit and an overarching research endeavor.
- It may become overloaded when the domain needs to express continuity across multiple sessions and outcomes.

### Impact on the domain

This option keeps the model lean but risks making ResearchSession carry more meaning than it can comfortably own.

## Option 2: Introduce an Aggregate Research

### Advantages

- Provides a broader concept that can own the overall purpose and continuity of research work.
- Better captures the full lifecycle of inquiry than ResearchSession alone.
- Keeps the distinction between a bounded activity and a larger research effort.

### Disadvantages

- The concept may be too generic if the domain needs a stronger sense of formal structure or ownership.
- It may overlap with ResearchSession unless boundaries are clearly defined.

### Impact on the domain

This option improves expressiveness, but it may introduce a concept that is not yet sufficiently precise for the current level of maturity.

## Option 3: Introduce an Aggregate ResearchProject

### Advantages

- Gives the domain a larger, more explicit unit for long-running research work.
- Aligns well with the idea of sustained inquiry and cumulative knowledge.
- Distinguishes a project-level effort from a single session or experiment.
- Preserves the role of ResearchSession as a more focused operational unit.

### Disadvantages

- It may be more formal than the current domain needs.
- It could introduce a level of abstraction that feels heavier than the existing model.

### Impact on the domain

This option provides the clearest conceptual separation between a short-lived research activity and a broader, durable research effort. It is the most expressive option among the three.

# Recommendation

ResearchSession is not sufficient on its own to represent the full research process of EDGE_ENGINE.

It is a valuable concept for coordination and bounded activity, but the domain also needs a broader concept that can represent the larger purpose, continuity, and cumulative outcome of research work.

The most suitable option is to introduce a broader domain concept such as ResearchProject in future domain evolution, while preserving ResearchSession as a subordinate unit of activity.

This recommendation is justified because:

- it aligns with the manifesto’s emphasis on cumulative knowledge;
- it preserves the scientific method as a broader journey rather than a single session;
- it keeps ResearchSession focused and coherent without overloading it;
- it provides a more accurate domain representation of long-running research effort.

The recommendation is not to replace ResearchSession immediately, but to recognize that the current model is strong for coordination and weak for representing the full research endeavor.
