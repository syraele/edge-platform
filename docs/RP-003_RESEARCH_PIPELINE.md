# RP-003 — Research Pipeline

Version: 1.1

Status: Implemented

Phase: Application Layer & Research Pipeline

---

# Purpose

The Research Pipeline is the application-layer orchestrator for the current discovery workflow.

It coordinates the execution of the existing domain services without introducing business logic. The pipeline remains responsible for orchestration only.

---

# Current Responsibilities

The implemented pipeline:

* accepts a dataset query and a research session;
* resolves a dataset provider through the provider registry;
* builds the market description and hypotheses;
* runs experiments with the experiment runner;
* collects evidence and forms a discovery report;
* returns the resulting report to the caller.

The pipeline does not interpret market data directly and does not implement the hypothesis logic itself.

---

# Current Workflow

The current implementation follows this workflow:

```text
DatasetQuery
        ↓
DatasetProviderRegistry
        ↓
MarketDescription
        ↓
HypothesisFactory
        ↓
ExperimentRunner
        ↓
DiscoveryReport
```

The domain services remain responsible for the actual evaluation rules, including primitive and compound hypothesis matching, edge scoring, and report rendering.

---

# Current Interface

The pipeline is invoked by the CLI through the command:

```bash
python -m edge research --provider mt5 --symbol XAUUSD --timeframe M1 --from 2026-04-20 --to 2026-04-22
```

The CLI builds the query, runs the pipeline, and renders the resulting human-readable report.

---

# Result

The repository now contains an operational research pipeline that executes the discovery workflow end to end and produces a discovery report suitable for human review.
