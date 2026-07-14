# EDGE_ENGINE Domain Model

---
**Document ID:** DOMAIN-001
**Version:** 0.9 (Draft)
**Status:** Review
**Owner:** EDGE_ENGINE Project
**Last Updated:** 2026-07-14

**Related Documents**

- 00_MANIFESTO.md
- 01_ARCHITECTURE.md
- 02_RESEARCH_MODEL.md
- 03_ROADMAP.md
---

# 1. Purpose

This document defines the official Domain Model of EDGE_ENGINE.

It establishes the business language used throughout the platform and specifies the core domain artifacts and their relationships.

The Domain Model is technology-independent.

---

# 2. Domain Philosophy

EDGE_ENGINE is not centered around trading.

Its domain is the discovery, validation and accumulation of market knowledge.

The domain models **how knowledge is created**, not how trades are executed.

---

# 3. Domain Principles

- The Domain is independent from Infrastructure.
- Every artifact has a single responsibility.
- Domain artifacts should be immutable whenever possible.
- Business concepts must be explicit.
- Research must be deterministic and reproducible.

---

# 4. Knowledge Transformation

```text
Market Data
      │
      ▼
HistoricalDataset
      │
      ▼
MarketDescription
      │
      ▼
MarketVocabulary
      │
      ▼
ResearchConfiguration
      │
      ▼
Experiment
      │
      ▼
ExperimentResult
      │
      ▼
Evidence
      │
      ▼
Knowledge
      │
      ▼
ValidatedEdge
```

Each artifact increases the information value produced by the previous one.

---

# 5. Domain Artifacts

## Bar

Represents one immutable market observation.

---

## HistoricalDataset

Purpose:
Provide a normalized and immutable historical dataset.

Owns:

- Bars
- DatasetMetadata

Produces:

- Input for MarketDescription

---

## MarketDescription

Represents an objective description of market behaviour.

Owns a collection of MarketDescriptor objects.

---

## MarketDescriptor

Represents one measurable market characteristic.

Examples:

- Trend
- Volatility
- Noise
- Liquidity
- Momentum
- Efficiency
- Compression
- Expansion

---

## MarketVocabulary

Transforms descriptions into a common research language.

---

## VocabularyTerm

Represents one standardized market concept.

---

## ResearchConfiguration

Defines one deterministic research experiment.

Contains:

- Dataset
- Parameters
- Constraints

---

## Experiment

Represents one executable research hypothesis.

---

## ExperimentResult

Contains the raw output of an experiment.

Examples:

- trades
- equity curve
- drawdown
- returns

---

## Evidence

Represents statistical evidence extracted from an ExperimentResult.

Examples:

- Sharpe Ratio
- Expectancy
- Stability
- Robustness
- p-value
- Confidence

Evidence supports or rejects a hypothesis.

---

## Knowledge

Represents validated research knowledge.

Knowledge is independent from storage.

Persistence belongs to Infrastructure.

---

## Edge

Represents one research hypothesis supported by evidence.

Properties:

- confidence
- supporting evidence
- creation date
- status

Status values:

- Candidate
- Validated
- Active
- Retired
- Rejected

---

## ValidatedEdge

Represents an edge approved for continuous monitoring.

---

# 6. Artifact Relationships

```text
HistoricalDataset
        │
        ▼
MarketDescription
        │
        ▼
MarketVocabulary
        │
        ▼
ResearchConfiguration
        │
        ▼
Experiment
        │
        ▼
ExperimentResult
        │
        ▼
Evidence
        │
        ▼
Knowledge
        │
        ▼
ValidatedEdge
```

---

# 7. Domain Invariants

- HistoricalDataset is immutable.
- MarketDescription is immutable.
- Evidence never modifies ExperimentResult.
- Knowledge never modifies history.
- Infrastructure never defines business rules.
- Business decisions belong to the Domain.

---

# 8. Aggregate Overview

| Aggregate | Root |
|-----------|------|
| Dataset | HistoricalDataset |
| Description | MarketDescription |
| Vocabulary | MarketVocabulary |
| Research | Experiment |
| Evidence | Evidence |
| Knowledge | Knowledge |
| Edge | Edge |

---

# 9. Future Evolution

Future artifacts may extend the model without modifying existing concepts.

Examples:

- Regime
- EdgeLifecycle
- PortfolioOfEdges

---

# 10. Conclusion

The Domain Model defines the common language of EDGE_ENGINE.

All future implementations must derive from this specification.

End of Document
