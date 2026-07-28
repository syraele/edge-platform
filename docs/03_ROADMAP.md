# EDGE_ENGINE Roadmap

## Current Status

The repository is currently in the Discovery Engine phase. The implemented workflow is stable and validated on real MT5 data.

---

## Completed Milestones

### Foundation

**COMPLETE**

The architectural foundation, documentation structure, and domain boundaries are present and stable.

### Dataset Layer

**COMPLETE**

The repository includes both an MT5 provider and a filesystem CSV provider.

### Research Pipeline

**COMPLETE**

The application layer orchestrates dataset loading, hypothesis execution, evidence collection, and report generation.

### Discovery Engine

**COMPLETE**

The current implementation includes:

* Primitive Catalog
* Primitive Discovery Engine
* Combination Engine Level 1
* Compound Hypothesis Evaluation
* Edge Scoring
* Human Discovery Report

### CLI

**COMPLETE**

The CLI entrypoint is operational and can run:

```bash
python -m edge research --provider mt5 --symbol XAUUSD --timeframe M1 --from 2026-04-20 --to 2026-04-22
```

---

## Next Milestone

### DI-006 — Edge Improvement Analysis

**PLANNED**

This is the next milestone in the current roadmap.
