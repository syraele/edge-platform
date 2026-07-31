# EDGE_ENGINE

A domain-driven research engine for building, validating, and evolving quantitative knowledge from historical market data.

---

## Overview

EDGE_ENGINE is a research platform for turning historical market data into reproducible evidence, validated hypotheses, and reusable quantitative knowledge.

The repository currently contains a working end-to-end discovery workflow that can run research from the command line, evaluate primitive and compound hypotheses, rank results with edge scoring, and render a human-readable discovery report.

EDGE_ENGINE is not a trading platform or an automated trading system. Its current purpose is the construction and preservation of quantitative knowledge.

---

## Current Implementation Status

The repository currently implements the following capabilities:

* A working CLI entrypoint via `python -m edge research ...`
* An MT5 dataset provider for real market data ingestion
* A filesystem CSV dataset provider for local test data
* A primitive catalog and primitive discovery engine
* A combination engine for level 1 compound hypotheses
* Compound hypothesis evaluation in the experiment executor
* Edge scoring for ranking discovery results
* A human-readable discovery report rendered in the CLI
* An end-to-end discovery pipeline that produces a discovery report from a dataset query
* Candidate-edge selection reporting aligned with Knowledge-based selection results

---

## Quick Start

Run discovery against real MT5 data:

```bash
python -m edge research --provider mt5 --symbol XAUUSD --timeframe M1 --from 2026-04-01 --to 2026-04-30
```

The command executes the discovery pipeline and prints a ranked report for human review.

---

## Project Structure

```text
edge-platform/
├── README.md
├── PROJECT_STATUS.md
├── PROJECT_BOOTSTRAP.md
├── FOUNDATION_BLUEPRINT.md
├── docs/
├── src/
└── tests/
```

---

## Documentation

The repository documentation is organized as follows:

* [PROJECT_STATUS.md](PROJECT_STATUS.md) — current milestone status and validation summary
* [docs/00_MANIFESTO.md](docs/00_MANIFESTO.md) — project philosophy and principles
* [docs/01_ARCHITECTURE.md](docs/01_ARCHITECTURE.md) — architecture and current implementation boundaries
* [docs/02_RESEARCH_MODEL.md](docs/02_RESEARCH_MODEL.md) — research methodology
* [docs/03_ROADMAP.md](docs/03_ROADMAP.md) — current roadmap and next milestone
* [docs/04_DOMAIN_MODEL.md](docs/04_DOMAIN_MODEL.md) — domain concepts

---

## Contributing

Contributions should remain consistent with the foundation blueprint, the manifesto, and the current architecture. Any significant architectural change must be introduced through an approved milestone or ADR.

---

## License

Project license: TBD.
