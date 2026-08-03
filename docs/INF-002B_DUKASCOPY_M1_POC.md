# INF-002B — Dukascopy M1 Canonical Acquisition POC

Version: 0.1

Status: Proposed

---

## Objective

Evaluate whether EDGE_ENGINE should treat M1 as the canonical acquisition timeframe for external market data and whether a Dukascopy-based proof of concept can support that model.

The architectural goal is not to make the research pipeline depend on whatever timeframe the provider exposes. Instead, the platform should acquire a stable lower-granularity source (M1) and let a later transformation layer derive coarser timeframes such as M5, M15, M30, H1, and D1.

---

## Architectural position

The proposed model is:

1. Provider acquisition layer imports raw bars from an external source.
2. The connector stores the data in the canonical registry as M1 bars.
3. A dedicated dataset builder or timeframe aggregation component derives coarser timeframes from the M1 base dataset.
4. The research pipeline consumes only the canonical dataset artifact, regardless of the origin provider.

This improves architectural independence because the Dataset Registry no longer depends on the provider’s native timeframe availability.

---

## Why M1 is a good canonical acquisition base

Using M1 as the canonical acquisition timeframe is preferable when:

- the provider has reliable minute-level access but inconsistent or incomplete support for M5/M15/H1/D1;
- the platform wants a single lowest-common-denominator source for reproducibility;
- the registry should remain provider-agnostic and resilient to upstream availability changes;
- a later transformation step can generate richer timeframes deterministically.

This is especially valuable for a research platform because the research layer should consume normalized data, not raw provider-specific cadence.

---

## Proposed POC scope

### In scope

- Acquire EURUSD and XAUUSD data from Dukascopy at M1 granularity.
- Normalize the imported bars into the canonical EDGE_ENGINE bar shape.
- Write the result into the Dataset Registry layout.
- Preserve provenance and metadata.
- Produce a minimal derived dataset for M5 or H1 using a deterministic aggregation component.

### Out of scope

- Full provider integration into the CLI.
- Advanced backfilling logic.
- Provider-specific research semantics.
- Broker account dependency.

---

## POC implementation plan

### 1. Connector

Implement a dedicated connector that:

- requests M1 bars from Dukascopy for a bounded historical range;
- normalizes the payload into canonical bars;
- writes the dataset and manifest into the local registry.

### 2. Timeframe derivation component

Introduce a lightweight component that accepts a canonical M1 dataset and produces a higher timeframe dataset by aggregating bars.

Example responsibilities:

- M1 → M5
- M1 → M15
- M1 → M30
- M1 → H1
- M1 → D1

The component should be deterministic and pure. It should not depend on the provider.

### 3. Registry integration

The resulting derived datasets should be stored as separate registry entries with:

- a distinct dataset_id;
- a timeframe label matching the derived cadence;
- provenance metadata pointing to the base M1 dataset.

---

## Acceptance criteria

The POC is considered successful if:

- a Dukascopy-based import can produce a valid M1 dataset for EURUSD and XAUUSD;
- the imported data is normalized into EDGE_ENGINE's canonical bar format;
- the dataset is written into the local registry with manifest and checksum;
- a derived timeframe (for example M5 or H1) can be generated from the M1 source without contacting the provider again;
- the derived dataset is also registered and can be loaded by the existing dataset access path.

---

## Recommendation

If Dukascopy can provide M1 data for at least a limited historical range, then adopting M1 as the canonical acquisition timeframe is the more architecture-correct choice than trying to make the connector depend on every provider-specific timeframe.

This design aligns better with the existing Dataset Connector Framework and preserves the independence of the Dataset Registry from the upstream provider.
