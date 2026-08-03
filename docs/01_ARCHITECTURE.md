# EDGE_ENGINE Architecture

Version: 2.2

Status: Approved for Foundation v2 and KF-004

---

# Purpose

This document describes the current architectural structure of the repository and its implementation boundaries.

The architecture remains aligned with the foundation principles: the domain layer contains the research rules, while the application layer orchestrates execution and the infrastructure layer provides data providers.

---

# Current Architectural Layers

```text
CLI
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```

## Domain

The domain layer contains the core research concepts and services, including:

* ResearchHypothesis
* Experiment and Evidence
* ExperimentExecutor
* PrimitiveCatalog
* PrimitiveDiscoveryEngine
* CombinationEngine
* EdgeScoringService
* DiscoveryReport

These components implement the research rules without depending on infrastructure details.

## Application

The application layer coordinates the workflow and preserves the boundaries between orchestration and domain logic. The main application components are:

* ResearchPipeline
* ExperimentRunner
* ResearchSession
* ResearchEvaluator

The pipeline accepts a dataset query, resolves providers, executes hypotheses, and builds a discovery report.

## Infrastructure

The infrastructure layer provides data access implementations:

* Mt5DatasetProvider
* FilesystemCsvDatasetProvider
* DatasetProviderRegistry

These components are responsible for loading market data into the repository’s domain models.

## CLI

The repository exposes a working command-line entrypoint:

```powershell
.\.venv\Scripts\python.exe -m edge research --provider filesystem-csv --symbol EURUSD --timeframe M1 --from 2024-01-01T00:00:00 --to 2024-01-01T01:00:00 --validation-from 2024-01-01T00:00:00 --validation-to 2024-01-01T01:00:00
```

The CLI builds a dataset query, runs the pipeline, and renders a human-readable discovery report ranked by edge score.

---

# Design Principles

The current implementation remains consistent with the following principles:

* Domain independence
* Reproducibility
* Deterministic execution where possible
* Testability
* Clear separation between orchestration and business rules
* Clear separation of responsibilities across hypothesis, evidence, knowledge, consolidation, candidate-edge qualification, and validation

---

# Current Implementation Notes

The repository currently demonstrates the following concrete flow:

1. The CLI receives research parameters.
2. The pipeline creates a dataset query.
3. The provider registry resolves a dataset provider.
4. The hypothesis factory generates primitive and compound hypotheses.
5. The experiment executor evaluates the hypotheses against the dataset.
6. Evidence is transformed into Knowledge through the research evaluator.
7. Knowledge is consolidated into representative Canonical Knowledge clusters.
8. Candidate-edge qualification selects the most valuable representatives for reporting and promotion.
9. Validation confirms the promoted candidates on a separate dataset context.
10. The discovery report is ranked and printed for human analysis.

This flow is the implementation basis for the documented roadmap. The approved architecture preserves the Domain Model unchanged and introduces Canonical Knowledge as an application-level consolidation concept rather than a duplicate of Knowledge.
