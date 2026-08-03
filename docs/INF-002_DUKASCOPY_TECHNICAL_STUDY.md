# INF-002 — Dukascopy Technical Study

Version: 1.0

Status: Proposed

---

## Purpose

This document evaluates Dukascopy as a candidate external data source for the EDGE_ENGINE import architecture.

Its purpose is not to implement a connector yet. Instead, it defines whether Dukascopy is a credible future official acquisition source, what constraints must be understood before implementation, and how it would fit the existing dataset-first architecture.

This study is intentionally design-oriented and should be read alongside the Dataset Connector Framework and the Import Infrastructure Theory.

---

## Executive Summary

Dukascopy appears to be a credible candidate for future import infrastructure because it is publicly positioned as a broker and market-data provider with a historical data export offering for a broad set of financial instruments, including Forex, commodities, and indices.

However, the public evidence available in the current review is insufficient to justify immediate implementation. The public pages confirm that historical data export is a real business offering, but they do not expose a stable, machine-readable API contract, a documented schema, or the licensing conditions required for a production-grade connector.

Recommendation: treat Dukascopy as a strong candidate for a future connector, but do not make it the official research dependency yet. Keep the current local dataset-first baseline as the operational research path while a formal Dukascopy proof-of-concept is evaluated.

---

## 1. What the public Dukascopy evidence indicates

The public Dukascopy material reviewed during this study indicates the following:

- Dukascopy presents itself as a broker and market-data provider with a visible historical data export section.
- The historical-data pages describe historical price data for a broad universe of instruments, including Forex, commodities, and indices.
- The public market-info pages show wide instrument coverage and a large market-data ecosystem.
- The public content does not provide enough detail to define an implementation-ready connector contract.

This means the current evidence is sufficient to justify a technical study, but not sufficient to justify implementation without a deeper data-access investigation.

---

## 2. Architectural fit with EDGE_ENGINE

Dukascopy should be evaluated as an import connector, not as a research engine.

Under the approved architecture:

1. Dukascopy would act as an acquisition source.
2. A Dukascopy connector would extract raw data from the source.
3. A builder would convert the raw payload into the platform's canonical dataset representation.
4. The Dataset Registry would validate and register the resulting dataset.
5. The Research Pipeline would consume the registered dataset without caring where it came from.

This is fully consistent with the Dataset Connector Framework and the Import Infrastructure Theory.

The key architectural constraint is that research must remain decoupled from Dukascopy-specific logic. Dukascopy may be used to populate the registry, but it must never become a direct dependency of the research execution path.

---

## 3. Why Dukascopy is attractive

### 3.1 Strong external credibility

Dukascopy is a recognizable provider in the FX and market-data ecosystem. Its public presence suggests a mature data business rather than a one-off experimental feed.

### 3.2 Broad instrument universe

The public pages suggest support for a wide range of instruments, including major FX pairs and other asset classes. This is valuable because EDGE_ENGINE is designed to operate on a general market-data abstraction rather than on a single instrument.

### 3.3 Alignment with the import architecture

Dukascopy fits naturally into the connector model already described in the repository. It can be treated as one more acquisition source behind the same dataset-registration boundary.

### 3.4 Reproducibility opportunities

If Dukascopy can be integrated in a controlled and versioned way, it can support the same reproducibility goals that motivate the local dataset registry.

---

## 4. Why Dukascopy is not yet sufficient for implementation

### 4.1 Public documentation is incomplete for automation

The pages reviewed during this assessment do not reveal an implementation-ready contract for:

- authentication and access rules;
- exact data endpoint structure;
- the output schema;
- historical range guarantees;
- licensing and redistribution conditions.

This is the main limiting factor.

### 4.2 The public pages do not guarantee a stable import path

Even if historical data export exists, the mechanism may depend on:

- account-based access;
- export workflows;
- rate limits;
- terms that are not suitable for automated ingestion;
- data formats that require additional reverse-engineering.

That makes the connector a higher-risk implementation candidate until the access path is validated.

### 4.3 Data semantics must be verified explicitly

The public pages do not provide enough evidence to confirm the canonical fields required by EDGE_ENGINE, including:

- time granularity;
- timezone handling;
- missing-data behavior;
- symbol naming conventions;
- session handling;
- whether OHLCV-like bars or another representation is expected.

These details must be confirmed with a sample import before implementation.

---

## 5. Design implications for EDGE_ENGINE

If Dukascopy is pursued, the connector should be designed around the following principles:

### 5.1 Import-only responsibility

The connector must not participate in research logic. Its only duty is to acquire data and hand it off to the canonical dataset path.

### 5.2 Canonical dataset boundary

The connector must normalize all source-specific rows into the platform's canonical dataset representation before registration.

### 5.3 Metadata and provenance

Every imported dataset must preserve:

- source identity;
- connector type;
- import timestamp;
- symbol and timeframe;
- range covered;
- provenance and transformation notes.

### 5.4 Validation before registration

The connector must not register a dataset unless the data passes structural and semantic validation.

### 5.5 Versioning and immutability

Each import must be versioned so research can remain reproducible and traceable.

---

## 6. Technical risks to evaluate before implementation

The following risks should be treated as study items before any connector implementation is approved:

- Access and licensing risk
  - The connector may depend on terms that are not compatible with automated or redistributed ingestion.

- Schema risk
  - The data format may differ from what the platform expects and may require custom normalization.

- Availability risk
  - Historical coverage may vary by symbol, timeframe, or account type.

- Timezone and session risk
  - The platform needs a precise and reproducible handling strategy for timestamps and market-session boundaries.

- Reliability risk
  - The import workflow may be brittle if it depends on manual export steps or fragile scraping logic.

- Maintenance risk
  - A connector that depends on a public web flow may become unstable if the provider changes the interface.

---

## 7. Recommended evaluation approach

The next step should be a sandbox-style proof of concept rather than a production implementation.

### Proposed study path

1. Select a small sample instrument and timeframe.
2. Acquire a small historical sample from Dukascopy using the least invasive documented access path available.
3. Map the result into the canonical dataset shape used by EDGE_ENGINE.
4. Validate the imported sample against the platform's dataset expectations.
5. Capture metadata and provenance from the sample import.
6. Decide whether the connector should proceed to implementation.

This approach keeps the study focused on whether Dukascopy can satisfy the platform's import contract before any broader integration effort begins.

---

## 8. Recommendation

Dukascopy is a promising candidate for future data acquisition infrastructure because it appears to have a real historical-data offering and matches the platform's import-connector model.

However, it should not be treated as an implementation-ready official source until the following are confirmed:

- a stable and lawful access method;
- a known source schema;
- a tested import flow into the canonical dataset format;
- a validation and provenance strategy that fits the existing Dataset Registry contract.

### Final recommendation

Approve Dukascopy as a candidate connector for a future implementation phase, but keep the current local filesystem dataset workflow as the official research baseline until a documented proof-of-concept proves the Dukascopy path is reliable and compatible.

---

## 9. Acceptance criteria for the next phase

The next phase should proceed only if the following conditions are met:

- a sample import can be produced without manual intervention;
- the sample data can be normalized into the canonical dataset representation;
- validation succeeds before registration;
- metadata and provenance are preserved;
- the import path remains compatible with the Dataset Registry contract;
- the access method is documented and acceptable for long-term use.

If these conditions are met, Dukascopy may become a valid future official connector candidate.
