# Architecture Changelog

## STEP-001

**Decision:**
Architectural Principles Frozen

**Reason:**
Freeze long-term architectural rules before evolving the platform.

**Impact:**
Documentation only.

**Code:**
No changes.

## STEP-001A

**Decision:**
Governance Documentation Consolidation

**Reason:**
Remove duplicated project information and establish a single source of truth for each document.

**Impact:**
Documentation consistency improved.

**Code:**
No changes.

## STEP-001B

**Decision:**
Development Workflow Frozen

**Reason:**
Standardize the lifecycle of every future milestone.

**Impact:**
Governance completed.

**Code:**
No changes.

## STEP-002

**Decision:**
Core Domain Language

**Reason:**
Establish the ubiquitous language that governs the Domain Model.

**Impact:**
Domain vocabulary standardized.

**Code:**
No changes.

## STEP-003

**Decision:**
Knowledge Lifecycle Defined

**Reason:**
Formalize the lifecycle of Knowledge within the platform.

**Impact:**
Formal lifecycle introduced.

**Code:**
No changes.

## STEP-004

**Decision:**
Knowledge Aggregate Specification

**Reason:**
Formal specification before implementation.

**Impact:**
Aggregate contract defined.

**Code:**
No changes.

## STEP-005

**Decision:**
Knowledge Value Objects defined.

**Reason:**
Specify the domain building blocks of the Knowledge Aggregate before implementation.

**Impact:**
Aggregate building blocks specified.

**Code:**
No changes.

## STEP-006

**Decision:**
Knowledge Repository Contract defined.

**Reason:**
Formalize the domain responsibilities of the Knowledge Repository before implementation.

**Impact:**
Repository responsibilities formalized.

**Code:**
No changes.

## STEP-006A

**Decision:**
Domain Map defined.

**Reason:**
Formalize the domain boundaries and aggregate relationships before implementation.

**Impact:**
Aggregate boundaries formalized.

**Code:**
No changes.

## STEP-007

**Decision:**
Domain Review completed.

**Reason:**
Review the coherence of the evolving Domain Model before further milestone work.

**Impact:**
Domain maturity assessed.

**Code:**
No changes.

## STEP-008

**Decision:**
ResearchSession role analyzed.

**Reason:**
Assess whether the domain requires a broader research concept than ResearchSession.

**Impact:**
Research boundaries evaluated.

**Code:**
No changes.

## EDGE-002

**Decision:**
Introduce quantitative research metrics and complete Candidate Edge Selection integration.

**Reason:**
Move the platform from raw discovery output toward a more quantitative and verifiable research stage.

**Impact:**
The Discovery Report now exposes Win Rate, Expectancy, Profit Factor, Payoff, and Drawdown. Candidate Edge Selection is visible in the CLI output and the project is now stable for the next milestone.

**Code:**
Updated the experiment executor to derive quantitative metrics from real trade sequences, propagated the metrics into the discovery report, and verified the workflow end-to-end through CLI execution and regression testing.
