# EDGE_ENGINE Architecture

Version: 2.1

Status: Current implementation aligned with the repository

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

```bash
python -m edge research --provider mt5 --symbol XAUUSD --timeframe M1 --from 2026-04-01 --to 2026-04-30
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

---

# Current Implementation Notes

The repository currently demonstrates the following concrete flow:

1. The CLI receives research parameters.
2. The pipeline creates a dataset query.
3. The provider registry resolves a dataset provider.
4. The hypothesis factory generates primitive and compound hypotheses.
5. The experiment executor evaluates the hypotheses against the dataset.
6. The discovery report is ranked and printed for human analysis.

This flow is the implementation currently present in the repository and is the basis for the documented roadmap. The current repository state also includes candidate-edge selection reporting aligned with the Knowledge-based selection step, and the relevant regression suite is passing.
