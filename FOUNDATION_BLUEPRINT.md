# FOUNDATION_BLUEPRINT.md

Version: 1.0

Status: Frozen (Foundation v2)

Purpose: High-level architectural blueprint that defines the conceptual foundation of EDGE_ENGINE. Every document and every architectural decision must be consistent with this Blueprint.

---

# 1. Identity

EDGE_ENGINE is a system for building, validating, and evolving quantitative knowledge about financial markets through a reproducible scientific research process.

---

# 2. Purpose

EDGE_ENGINE exists to transform quantitative research from a collection of isolated experiments into a systematic process for building reliable, reproducible, and reusable quantitative knowledge.

---

# 3. Core Domain

Transform market observations into verifiable quantitative knowledge through the systematic validation of research hypotheses.

---

# 4. Core Concepts

The fundamental concepts of the domain are:

* HistoricalDataset
* MarketDescription
* ResearchHypothesis
* Experiment
* Evidence
* Knowledge
* Edge

Their responsibilities, relationships, and implementation are defined in the Domain Model.

---

# 5. Knowledge Flow

```text
HistoricalDataset
        ↓
MarketDescription
        ↓
ResearchHypothesis
        ↓
Experiment
        ↓
Evidence
        ↓
Knowledge
        ↓
Edge
```

This flow represents the **conceptual transformation of knowledge inside the domain**.

It is **not** the implementation workflow and **not** the execution pipeline.

### Relationship with the Manifesto

The Manifesto defines the **Scientific Method**:

**Observation → Hypothesis → Experiment → Evidence → Knowledge → Edge**

The Scientific Method describes **how research is conducted**.

The Knowledge Flow describes **how domain concepts evolve**.

These two views are complementary and intentionally represent different perspectives of the same system.

---

# 6. Architectural Principles

The architecture is governed by the following principles:

1. Domain First
2. Evidence Before Opinion
3. Knowledge Must Accumulate
4. Reproducibility by Design
5. Evolution Over Perfection
6. Simplicity Over Cleverness
7. Clean Boundaries

Their complete definition is provided in the Manifesto.

---

# 7. Success Criteria

EDGE_ENGINE is successful when it is able to build, validate, preserve, and evolve quantitative knowledge in a reproducible, technology-independent, and sustainable way over time.

---

# Blueprint Rules

* The Blueprint is the conceptual foundation of Foundation v2.
* Every document inside `docs/` must be consistent with this Blueprint.
* Every significant architectural decision must be traceable to the Blueprint.
* The Blueprint remains frozen during milestone development.
* The documentation derives from the Blueprint.
* The implementation derives from the documentation.
