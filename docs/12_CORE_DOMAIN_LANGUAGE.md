# Observation

## Definition

An Observation is a recorded fact about the observed context that can be considered as input for research.

## Responsibilities

An Observation provides the raw material from which the research process can begin.

## Is NOT

An Observation is NOT a conclusion.

An Observation is NOT a hypothesis.

An Observation is NOT proof.

## Produced By

An Observation is produced by the observed context and by data collection.

## Consumed By

An Observation is consumed by Market Description, Hypothesis, and Evidence.

## Relationships

An Observation contributes to the formation of a Market Description.

An Observation may support the creation of a Hypothesis.

An Observation may become part of the evidence chain.

## Invariants

An Observation MUST remain factual and traceable.

An Observation MUST remain distinguishable from interpretation.

# Dataset

## Definition

A Dataset is the structured collection of observations that constitutes the material basis for research.

## Responsibilities

A Dataset provides the organized evidence base used to build understanding and evaluate research questions.

## Is NOT

A Dataset is NOT a hypothesis.

A Dataset is NOT a conclusion.

A Dataset is NOT a single observation.

## Produced By

A Dataset is produced from collected observations.

## Consumed By

A Dataset is consumed by Market Description, Experiment, and Research Session.

## Relationships

A Dataset supports the construction of a Market Description.

A Dataset provides the context required for an Experiment.

## Invariants

A Dataset MUST remain coherent and internally consistent.

A Dataset MUST preserve the traceability of its observations.

# Market Description

## Definition

A Market Description is the structured interpretation of a Dataset in terms of the market context relevant to research.

## Responsibilities

A Market Description organizes observations into a meaningful context for hypothesis formation and analysis.

## Is NOT

A Market Description is NOT a raw dataset.

A Market Description is NOT a hypothesis.

A Market Description is NOT a final conclusion.

## Produced By

A Market Description is produced from a Dataset and its observations.

## Consumed By

A Market Description is consumed by Hypothesis and Research Session.

## Relationships

A Market Description provides the context from which a Hypothesis is formed.

A Market Description may be refined as more evidence is accumulated.

## Invariants

A Market Description MUST remain grounded in the underlying Dataset.

A Market Description MUST remain distinguishable from asserted truth.

# Hypothesis

## Definition

A Hypothesis is a testable proposition formulated from a Market Description and intended to be evaluated through investigation.

## Responsibilities

A Hypothesis expresses a possible relationship that can be examined through Experiment.

## Is NOT

A Hypothesis is NOT evidence.

A Hypothesis is NOT knowledge.

A Hypothesis is NOT a final conclusion.

## Produced By

A Hypothesis is produced from a Market Description and research intent.

## Consumed By

A Hypothesis is consumed by Experiment and Research Session.

## Relationships

A Hypothesis is evaluated through Experiment.

A Hypothesis may lead to Evidence.

## Invariants

A Hypothesis MUST remain testable.

A Hypothesis MUST remain explicit and distinguishable from validated knowledge.

# Experiment

## Definition

An Experiment is the structured act of evaluating a Hypothesis under controlled conditions.

## Responsibilities

An Experiment provides the mechanism by which a Hypothesis is examined and tested.

## Is NOT

An Experiment is NOT a conclusion.

An Experiment is NOT knowledge.

An Experiment is NOT a hypothesis.

## Produced By

An Experiment is produced from a Hypothesis and an execution context.

## Consumed By

An Experiment is consumed by Evidence and Research Session.

## Relationships

An Experiment produces Evidence.

An Experiment is associated with a Hypothesis.

## Invariants

An Experiment MUST remain tied to a defined hypothesis and context.

An Experiment MUST preserve its traceability to the hypothesis it evaluates.

# Evidence

## Definition

Evidence is the outcome of an Experiment that supports or refutes a Hypothesis.

## Responsibilities

Evidence provides the basis for validating claims and forming knowledge.

## Is NOT

Evidence is NOT a hypothesis.

Evidence is NOT knowledge.

Evidence is NOT a final judgment.

## Produced By

Evidence is produced by Experiment.

## Consumed By

Evidence is consumed by Knowledge and Research Session.

## Relationships

Evidence supports the emergence of Knowledge.

Evidence is grounded in Experiment.

## Invariants

Evidence MUST remain traceable to the Experiment that produced it.

Evidence MUST remain separate from interpretation.

# Knowledge

## Definition

Knowledge is a validated understanding that has been established through evidence and accepted as reusable insight.

## Responsibilities

Knowledge preserves the durable understanding generated by research.

## Is NOT

Knowledge is NOT a hypothesis.

Knowledge is NOT raw evidence.

Knowledge is NOT an observation.

## Produced By

Knowledge is produced from Evidence and validation.

## Consumed By

Knowledge is consumed by Knowledge Collection, Edge, and Research Session.

## Relationships

Knowledge may be grouped into Knowledge Collection.

Knowledge may contribute to the formation of an Edge.

## Invariants

Knowledge MUST remain grounded in evidence.

Knowledge MUST remain traceable to the evidence that supports it.

# Knowledge Collection

## Definition

A Knowledge Collection is an organized set of Knowledge items that share a common research purpose or lineage.

## Responsibilities

A Knowledge Collection preserves and organizes reusable knowledge for future research.

## Is NOT

A Knowledge Collection is NOT a single piece of knowledge.

A Knowledge Collection is NOT evidence.

## Produced By

A Knowledge Collection is produced from Knowledge.

## Consumed By

A Knowledge Collection is consumed by Research Session and future knowledge work.

## Relationships

A Knowledge Collection groups related Knowledge.

A Knowledge Collection may inform the creation of new hypotheses.

## Invariants

A Knowledge Collection MUST remain coherent and purposefully organized.

A Knowledge Collection MUST preserve the traceability of contained knowledge.

# Edge

## Definition

An Edge is a validated and reusable insight that represents a meaningful advantage discovered through research.

## Responsibilities

An Edge expresses a durable outcome of the research process that can be reviewed, compared, and reused.

## Is NOT

An Edge is NOT a raw observation.

An Edge is NOT a hypothesis.

An Edge is NOT unvalidated speculation.

## Produced By

An Edge is produced from validated Knowledge and research evaluation.

## Consumed By

An Edge is consumed by Research Session and future review cycles.

## Relationships

An Edge is derived from validated Knowledge.

An Edge is the outcome of research progression toward durable insight.

## Invariants

An Edge MUST remain grounded in validated knowledge.

An Edge MUST remain distinguishable from preliminary evidence.

# Research Session

## Definition

A Research Session is the bounded period of work in which research activity is organized around a coherent purpose.

## Responsibilities

A Research Session coordinates the flow of observations, datasets, hypotheses, experiments, evidence, knowledge, and edges.

## Is NOT

A Research Session is NOT a single hypothesis.

A Research Session is NOT a single experiment.

A Research Session is NOT a final conclusion.

## Produced By

A Research Session is produced by the orchestration of research activity.

## Consumed By

A Research Session is consumed by further research and review.

## Relationships

A Research Session contains and relates the core concepts of the domain.

A Research Session may produce Knowledge and Edge.

## Invariants

A Research Session MUST remain coherent and bounded.

A Research Session MUST preserve traceability across the concepts it contains.
