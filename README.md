# EDGE_ENGINE

A domain-driven research engine for building, validating, and evolving quantitative knowledge from historical market data.

---

## Overview

EDGE_ENGINE is a research platform for turning historical market data into reproducible evidence, validated hypotheses, reusable quantitative knowledge, and recognized market phenomena.

The repository currently contains a verified end-to-end discovery workflow that can run research from the command line, evaluate primitive and compound hypotheses, rank results with edge scoring, and render a human-readable discovery report.

EDGE_ENGINE is not a trading platform or an automated trading system. Its current purpose is the construction, preservation, and consolidation of quantitative research understanding.

---

## Current Implementation Status

The repository currently implements the following capabilities:

* A working CLI entrypoint via `python -m edge research ...`
* A filesystem CSV dataset provider for local, reproducible research execution
* A dataset registry and manifest-backed local dataset resolution flow
* A primitive catalog and primitive discovery engine
* A combination engine for level 1 compound hypotheses
* Compound hypothesis evaluation in the experiment executor
* Edge scoring for ranking discovery results
* A human-readable discovery report rendered in the CLI
* An end-to-end discovery pipeline that produces a discovery report from a dataset query
* Candidate-edge selection reporting aligned with Knowledge-based selection results

---

## Quick Start

Run the official local benchmark workflow:

```powershell
.\.venv\Scripts\python.exe -m edge research --provider filesystem-csv --symbol EURUSD --timeframe M1 --from 2024-01-01T00:00:00 --to 2024-01-01T01:00:00 --validation-from 2024-01-01T00:00:00 --validation-to 2024-01-01T01:00:00
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
* [docs/10_MARKET_PHENOMENA.md](docs/10_MARKET_PHENOMENA.md) — foundational theory of market phenomena
* [docs/11_DISCOVERY_THEORY.md](docs/11_DISCOVERY_THEORY.md) — theory of discovery for the Intelligence phase

---

## Contributing

Contributions should remain consistent with the foundation blueprint, the manifesto, and the current architecture. Any significant architectural change must be introduced through an approved milestone or ADR.

---

## License

Project license: TBD.
