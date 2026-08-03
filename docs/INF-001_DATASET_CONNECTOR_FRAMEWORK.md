# INF-001 — Dataset Connector Framework

Version: 1.1

Status: Active

---

## Purpose

This document defines the architectural foundation for the Dataset Connector Framework within EDGE_ENGINE.

Its purpose is to establish the conceptual and structural contract for all data acquisition components that import external market data into the platform's canonical research representation.

This document is a design reference for future connectors such as Dukascopy, CSV, MT5, Polygon, Binance, and others.

It is intentionally conceptual and does not prescribe implementation details or code structure.

---

## Architectural Principle

The Research Pipeline must never depend on the origin of the data.

Research operates exclusively on Historical Dataset objects that are available through the Dataset Registry.

Data sources are acquisition components.
The Research Pipeline consumes only canonical datasets that have already been imported, normalized, and registered.

This principle is mandatory and must govern all future connector development.

---

## 1. What is a Dataset Connector?

A Dataset Connector is an acquisition component responsible for translating data from an external source into a canonical dataset that can be registered and used by the research system.

It is not a research component.
It does not perform analysis.
It does not decide what should be studied.
It exists only to import and normalize data into the platform's dataset domain.

A connector is therefore an adapter between an external source and the platform's canonical dataset model.

---

## 2. Responsibilities of a Dataset Connector

A Dataset Connector has the following responsibilities:

### 2.1 Source access

It must understand how to access the specific source it is designed for.

This may include:

- a local file;
- a remote API;
- a broker terminal integration;
- a historical archive;
- a streaming or batch source.

### 2.2 Data extraction

It must collect the required market data from the source.

### 2.3 Normalization

It must transform the extracted data into the canonical representation required by the platform.

### 2.4 Metadata enrichment

It must attach provenance and source-specific context needed to preserve traceability.

### 2.5 Validation

It must validate the resulting dataset before registration.

### 2.6 Registration preparation

It must produce a dataset artifact that is suitable for registration in the Dataset Registry.

The connector does not itself define research behavior.
Its responsibility ends once the dataset is prepared for registration and validation.

---

## 3. Lifecycle of a dataset through the framework

The complete lifecycle is the following:

Source
→ Connector
→ Builder
→ Registry
→ Historical Dataset

### Stage 1 — Source

The source is the external provider of raw market data.
Examples include:

- Dukascopy
- CSV files
- MT5
- Polygon
- Binance

### Stage 2 — Connector

The connector acquires the raw data from the source and transforms it into a normalized intermediate form.

### Stage 3 — Builder

The builder converts the normalized data into the platform's canonical dataset representation.

### Stage 4 — Registry

The Dataset Registry receives the built dataset, validates it, stores it, and makes it available for research.

### Stage 5 — Historical Dataset

The resulting object is a Historical Dataset available to the Research Pipeline.

At this point, the origin of the data is no longer relevant to research.
The research system sees only a canonical dataset.

---

## 4. Common interface every connector must implement

Every Dataset Connector must expose a common contract that defines its role in the acquisition pipeline.

The contract should define the following conceptual operations:

### 4.1 Discover availability

The connector must be able to determine whether the requested dataset is available from the source.

### 4.2 Fetch data

The connector must acquire the data for the requested identifier, symbol, timeframe, and range.

### 4.3 Normalize data

The connector must convert the source payload into a normalized representation.

### 4.4 Produce metadata

The connector must provide metadata describing the source, version, range, and provenance.

### 4.5 Validate the result

The connector must be able to confirm that the produced data is structurally and semantically valid.

For the current MT5 implementation, this includes:

- rejecting an invalid range where `--from` is greater than `--to`;
- accepting only `M1` for the current connector implementation;
- surfacing explicit failures for unavailable historical data, an invalid or unknown symbol, and MT5 connectivity problems.

### 4.6 Hand off to builder or registry

The connector must produce a dataset artifact that can be passed to the Builder and then to the Registry.

The interface must remain source-agnostic.
It should not expose implementation details that are specific to a single connector type.

---

## 5. Governance of versions, metadata, checksum, provenance, and validation

### 5.1 Versions

Every dataset import should be versioned.

Versioning is necessary for:

- reproducibility;
- traceability;
- comparison between imports;
- controlled evolution of historical datasets.

A version should be attached at the dataset level and must be preserved through registration.

To avoid ambiguity when multiple imports share the same symbol and timeframe, the registry must treat each imported dataset as a distinct logical record with:

- dataset_id: a stable technical identifier, assigned once and preserved through registration;
- display_name: an optional human-readable label for CLI, UI, and operator-facing workflows;
- version: a version label used for revisioning and reproducibility.

The registry must resolve every lookup to exactly one dataset. If a selection request matches more than one candidate, the lookup must fail explicitly with an ambiguity error rather than silently choosing one.

### 5.2 Metadata

Each dataset must carry metadata describing:

- symbol;
- timeframe;
- source;
- connector type;
- import time;
- range covered;
- range_start;
- range_end;
- bars_count;
- data quality notes;
- version identifier;
- registry state.

Metadata must be preserved through the full lifecycle.

### 5.3 Checksum

Every imported dataset should be associated with a checksum or equivalent integrity fingerprint.

Its purpose is to ensure that:

- the imported data has not been altered;
- the same dataset can be recognized as identical across re-imports;
- accidental divergence can be detected.

Checksum is a stability and integrity mechanism, not a research metric.

### 5.4 Provenance

Provenance records where the dataset came from and how it was created.

It should preserve:

- connector identity;
- source identifier;
- import timestamp;
- transformation steps;
- any relevant source-specific metadata.

Provenance ensures that the dataset remains traceable even if the source system changes later.

### 5.5 Validation

A dataset should not be considered ready for research until it has passed validation.

Validation should verify:

- structural integrity;
- completeness of the requested range;
- coherence of timestamps;
- consistency of field values;
- presence of required metadata;
- compatibility with the canonical dataset representation.

Validation is a prerequisite for registration.

### 5.6 Registry state

The registry may track a simple lifecycle state for each dataset as metadata:

- IMPORTED
- VALIDATED
- DEPRECATED
- CORRUPTED

This state is a registry concern and should support observability, lifecycle governance, and safe reuse of imported datasets. It should not be used as a substitute for the research pipeline's own validation logic.

---

## 6. How the Dataset Registry registers a new dataset

The Dataset Registry is the authoritative point of registration for all datasets used in research.

The registration flow is:

1. A connector acquires and normalizes data.
2. A builder converts the normalized data into the canonical dataset representation.
3. The dataset is validated.
4. The dataset is registered in the Dataset Registry.
5. The registry assigns the dataset a stable identity and version.
6. The dataset becomes available to the Research Pipeline as a Historical Dataset.

The Registry must treat registration as a formal act of publication.
Only registered datasets are considered valid research inputs.

---

## 7. How to keep the Research Pipeline independent from the data source

The Research Pipeline must never interact directly with any connector or source-specific component.

The boundary is simple:

- acquisition components import and register data;
- research components consume registered Historical Datasets.

This means that the Research Pipeline should depend only on:

- a dataset identifier;
- a canonical dataset object;
- the Dataset Registry interface.

It must not need to know:

- whether the data came from CSV;
- whether it came from MT5;
- whether it came from Dukascopy;
- whether it came from an API or a local file.

That knowledge belongs only to the acquisition layer.

This is the core architectural guarantee of the framework.

---

## 8. Architectural boundary to preserve

The following boundary must remain intact:

- Acquisition layer: source access, import, normalization, validation, registration.
- Research layer: hypothesis generation, evidence generation, knowledge formation, validation, and edge qualification.

No research logic should be allowed to cross this boundary.

---

## 9. Design guidance for future connectors

Every future connector must respect the following rules:

- it must produce a canonical dataset artifact;
- it must preserve provenance and metadata;
- it must validate before registration;
- it must not bypass the Dataset Registry;
- it must not introduce research logic into the acquisition layer;
- it must be replaceable without altering the Research Pipeline.

---

## 10. Foundational decision

The Dataset Connector Framework exists to make data acquisition modular, traceable, and independent from research execution.

The platform will treat data ingestion as an infrastructure concern and research as a separate concern.

This separation is essential for reproducibility, maintainability, and scientific rigor.
