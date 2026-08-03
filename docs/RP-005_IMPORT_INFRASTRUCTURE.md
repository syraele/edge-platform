# Import Infrastructure Theory

Version: 1.1

Status: Active

---

## Purpose

This document defines the conceptual architecture for market-data import within EDGE_ENGINE.

It establishes the principle that research must not depend on the origin of the data.
Research must operate only on datasets that are already registered and available through the Dataset Registry.

This document is conceptual and does not prescribe implementation details.

---

## Core Principle

MT5, Dukascopy, CSV, and any other data source are import mechanisms.
They are not research mechanisms.

Their role is limited to importing market data into the platform's canonical dataset representation.
Once imported, the data becomes a Dataset in the Dataset Registry.
From that point forward, research operates on the Dataset Registry and not on the source system directly.

---

## 1. Why MT5 is not sufficient

MT5 is not a suitable primary architectural dependency for the research platform because it couples the system to a runtime environment that is external, local, and operationally constrained.

This creates several conceptual problems:

- the research pipeline depends on a specific execution environment;
- historical availability is limited by the runtime context;
- the research engine becomes dependent on a live terminal or local integration path;
- the scientific process becomes vulnerable to infrastructure variability.

For this reason, MT5 must be treated as one possible importer, not as the foundation of the research system.

---

## 2. The separation of concerns

The platform must be structured around a strict separation between three responsibilities:

### Import

Importers are responsible for acquiring raw market data from external sources.
Examples include:

- MT5 importer
- Dukascopy importer
- CSV importer
- custom local importer

Their task is to produce a normalized dataset artifact.

### Registry

The Dataset Registry is the authoritative repository of datasets available to the platform.
It stores the datasets that the research system can use.
It is the single reference point for research execution.

### Research

The Research Pipeline consumes datasets from the Dataset Registry.
It does not need to know where the dataset came from.
It does not need to know whether the data was imported from MT5, CSV, or another source.

This separation ensures that research remains stable even when import infrastructure changes.

---

## 3. The conceptual contract of an importer

An importer is a component that performs a translation from an external source into a platform dataset.

Its responsibilities are limited to:

- locating or extracting data from the external source;
- normalizing the data into the platform's canonical dataset form;
- registering the resulting dataset in the Dataset Registry;
- preserving metadata about origin, version, and provenance.

An importer does not define the research logic.
It does not participate in hypothesis generation.
It does not evaluate research outcomes.

The current MT5 importer follows this contract in practice: it imports M1 bars into the local Dataset Registry, validates the requested interval, rejects unsupported timeframes, and raises explicit errors for empty history, missing symbols, and connection failures.

---

## 4. The conceptual contract of the Dataset Registry

The Dataset Registry is the platform's authoritative dataset catalog.

It represents the following:

- which datasets are available;
- which datasets are valid;
- which datasets are versioned;
- which datasets can be used for a specific research run;
- which datasets are immutable and reproducible;
- which datasets are currently imported, validated, deprecated, or corrupted.

Each dataset should be addressable through a stable technical identifier, `dataset_id`, while `version` remains a revision label and `display_name` may provide a human-readable label for operators and interfaces.

Every registry lookup must resolve to exactly one dataset. If a lookup would match multiple candidates, the registry must fail with an explicit ambiguity error rather than silently choosing one.

Research should be defined in terms of selection from the Dataset Registry.
A research run must identify a dataset by reference to the registry and not by direct attachment to a source-specific importer.

---

## 5. The conceptual contract of the Research Pipeline

The Research Pipeline operates on dataset identities that are already registered.

It should not need to know:

- whether the dataset came from MT5;
- whether it came from Dukascopy;
- whether it was generated from a CSV file;
- whether it was imported from a live feed or a historical archive.

Its only concern is the scientific use of the dataset.

This is the key architectural boundary.
It ensures that the research process is insulated from source-specific variability.

---

## 6. Why this matters for scientific rigor

This architecture improves the platform in several ways:

- it makes research reproducible;
- it decouples scientific work from environmental dependencies;
- it makes historical datasets reusable across experiments;
- it allows different importers to be used without altering the research model;
- it makes the platform resilient to changes in external data providers.

Scientific rigor depends on stable inputs.
The Dataset Registry provides that stability.

---

## 7. Foundational rule

The research system must operate on datasets that are already present in the Dataset Registry.

Importers may populate the registry.
Research may consume from the registry.
No component in the research path may depend on the original source of the dataset.

This rule must guide all future architectural decisions.
