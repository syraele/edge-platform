# EDGE_ENGINE Research Status

## Purpose

This document defines the current phase of EDGE_ENGINE and establishes the official reference point for the transition from platform infrastructure development to quantitative research on market edges.

The platform foundation is now stable. The focus of the project has shifted from building infrastructure toward the systematic discovery, validation, and refinement of quantitative edges from market data.

---

## Current Platform Status

The current implementation is centered on a discovery-oriented research flow that follows this progression:

Historical Dataset
↓
Primitive Discovery
↓
Hypothesis Generation
↓
Experiment Execution
↓
Evidence Generation
↓
Knowledge Generation
↓
Candidate Edge Selection
↓
Discovery Report

This flow represents the operating model of the current platform stage. It is the basis for research execution and for the evaluation of candidate opportunities derived from observed market behavior.

Foundation v2 is frozen. The architectural principles and the structural boundaries that govern the platform remain stable and should not be treated as open design space for this phase.

---

## EXP-003

EXP-003 introduced an expansion of the primitive discovery layer and increased the capacity of the platform to generate hypotheses from observable market structure.

This expansion broadened the set of primitives available to the discovery engine and increased the breadth of exploratory research. The result is a stronger initial search surface for identifying candidate patterns that may later become valuable quantitative edges.

---

## First Real Test

The first real execution of the discovery workflow was performed against historical market data using the following configuration:

- Provider: MT5
- Symbol: XAUUSD
- Timeframe: M1

The initial results were dominated by simple and highly frequent patterns, primarily:

- close < previous_close
- close < open
- close > previous_close
- close > open

These results were valuable because they demonstrated that the pipeline could produce real hypotheses from live market data. They also exposed a structural issue in the ranking logic: the system was not yet distinguishing between frequent patterns and genuinely operationally valuable ones.

---

## Edge Score Analysis

The current Edge Score used by the platform is a linear combination of the following metrics:

Occurrences
+ 1000 × Average Return 10
+ 100 × Average Return 5
+ 10 × Average Return 1
+ Average Return

This scoring model is useful for a first approximation, but it is not yet a robust scientific discriminator. The most important issue is that the weight of Occurrences dominates the ranking. As a consequence, the system tends to privilege patterns that are frequent rather than patterns that are truly meaningful in operational terms.

This is not a final ranking philosophy. It is a transitional mechanism that helped the platform move from infrastructure construction to quantitative observation.

---

## New Research Philosophy

The current phase introduces a more disciplined conceptual model for research progression:

Primitive
↓
Hypothesis
↓
Experiment
↓
Evidence
↓
Knowledge
↓
Candidate Edge
↓
Validated Edge

This model makes a crucial distinction: a Knowledge artifact is not automatically an Edge.

Knowledge represents validated information derived from evidence. Candidate Edge represents a filtered subset of Knowledge that satisfies preliminary quantitative criteria. Validated Edge represents the stronger stage in which the candidate becomes supported by deeper and more robust evidence.

---

## EDGE-001

EDGE-001 is the milestone that completed the first candidate-edge selection stage.

The milestone introduced Candidate Edge Selection as a lightweight filtering layer applied after Knowledge generation. The filter uses only metrics that are already available in the existing evidence and knowledge model. Its purpose is not to replace the broader research process, but to make the transition from raw discovered patterns to a smaller set of candidate opportunities more explicit and more verifiable.

---

## Verification of Integration

The integration of Candidate Edge Selection has been verified at the implementation level:

- CandidateEdgeSelection is executed during the discovery flow.
- DiscoveryReportService constructs the selection summary.
- The CLI formatter has been updated to render the selection summary.
- The discovery report now shows the selection summary in the output.

Example output:

Knowledge generate: 3
Knowledge scartate: 2
Candidate Edge: 1

This confirms that the selection stage is now visible in the end-to-end discovery report and that the pipeline is no longer only exposing raw ranking results.

---

## Open Improvements

The current report still shows generic identifiers such as rejected-1 and rejected-2 in the rejection section. This is acceptable as an intermediate step, but it is not sufficient for long-term research usability.

Future work must improve the report so that it shows:

- the real hypothesis name;
- the detailed reason for rejection;
- the quantitative context that explains why the candidate was filtered out.

---

## Principles of the New Phase

The new phase of EDGE_ENGINE is governed by the following principles:

- every new metric must be scientifically motivated;
- every modification must be verifiable;
- every milestone must be validated through real executions of the Discovery Pipeline.

These principles are intended to ensure that the project remains grounded in evidence and does not drift into speculative or unvalidated ranking behavior.

---

## Validation

EDGE-002 is considered completed and validated.

- Regression: 160/160 PASS
- Dataset validated: MT5 XAUUSD M1
- Discovery Report verified
- Quantitative metrics validated on a real trade sequence
- Project state updated to Stable

The current milestone is EDGE-003.

---

## Roadmap

### EDGE-001
Candidate Edge Selection
COMPLETATA

### EDGE-002
Introduction of new quantitative metrics:
- Win Rate
- Expectancy
- Profit Factor
- Payoff
- Drawdown
COMPLETATA

### EDGE-003
New multi-criteria ranking system.

### EDGE-004
Temporal validation.

### EDGE-005
Multi-market validation.

### EDGE-006
Automatic promotion from Candidate Edge to Validated Edge.

---

## Final Objective

The future development of EDGE_ENGINE will be oriented exclusively toward quantitative research. The long-term objective remains unchanged: transform market data into validated quantitative edges through disciplined analysis, measurable criteria, and repeated real-world verification.
