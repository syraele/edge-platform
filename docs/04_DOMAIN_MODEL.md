# EDGE_ENGINE Domain Model

Version: 2.0

Status: Foundation v2

---

# Purpose

This document defines the business domain of EDGE_ENGINE using Domain-Driven Design (DDD).

Its purpose is to identify the concepts, responsibilities, relationships, and invariants that represent the business domain independently from software implementation.

It does not describe architecture, research methodology, or implementation details.

---

# Domain Overview

The purpose of the domain is to transform market observations into validated quantitative knowledge through a systematic and reproducible research process.

The domain does not model trading execution.

It models the discovery, validation, preservation, and evolution of quantitative knowledge.

---

# Ubiquitous Language

The following concepts form the ubiquitous language of EDGE_ENGINE.

* HistoricalDataset
* MarketDescription
* ResearchHypothesis
* Experiment
* Evidence
* Knowledge
* Edge

These terms must be used consistently throughout the entire project.

---

# Strategic DDD

## Core Domain

The Core Domain is the systematic validation of research hypotheses in order to produce reliable quantitative knowledge.

The Core Domain includes:

* MarketDescription
* ResearchHypothesis
* Experiment
* Evidence
* Knowledge
* Edge

---

## Supporting Domain

Supporting capabilities include:

* HistoricalDataset
* Configuration
* Persistence
* Reporting

---

## Generic Domain

Generic concerns include:

* Logging
* Serialization
* Configuration loading
* Dependency Injection
* Infrastructure adapters

---

# Bounded Contexts

## Market Understanding

Responsible for transforming historical market data into structured market descriptions.

---

## Research

Responsible for hypothesis definition, experimentation, and evidence generation.

---

## Knowledge

Responsible for preserving validated knowledge and making it reusable.

---

## Edge Management

Responsible for managing validated edges and their lifecycle.

---

# Domain Concepts

## HistoricalDataset

Represents immutable historical market data used as research input.

---

## MarketDescription

Represents a structured description of market behaviour extracted from a dataset.

---

## ResearchHypothesis

Represents a falsifiable statement about market behaviour.

---

## Experiment

Represents the execution of a research hypothesis under controlled conditions.

---

## Evidence

Represents objective measurements produced by an experiment.

Evidence alone does not constitute knowledge.

---

## Knowledge

Represents validated, reproducible, and reusable research conclusions.

Knowledge is cumulative.

---

## Edge

Represents actionable quantitative knowledge with demonstrated value.

---

# Aggregate Roots

The Aggregate Roots of the domain are:

* HistoricalDataset
* MarketDescription
* ResearchHypothesis
* Experiment
* Edge

Each Aggregate protects its own business invariants.

Knowledge and Evidence are treated as Value Objects representing validated outcomes.

---

# Entities

Entities possess stable identity and lifecycle.

Current entities are limited to Aggregate Roots.

Additional entities may emerge only when justified by domain complexity.

---

# Value Objects

The primary Value Objects are:

* Bar
* MarketDescriptor
* Evidence
* Knowledge
* ResearchConfiguration
* DatasetMetadata
* DescriptorMetadata

Value Objects are immutable.

Equality is based on value rather than identity.

---

# Domain Services

The domain currently defines the following services:

## MarketDescriptionBuilder

Transforms historical datasets into market descriptions.

---

## ResearchEvaluator

Evaluates evidence and determines whether validated knowledge has been produced.

Domain Services contain business rules that do not naturally belong to a single Aggregate.

---

# Domain Invariants

## HistoricalDataset

* Immutable after creation.
* Represents a single historical source.

---

## MarketDescription

* Refers to exactly one HistoricalDataset.
* Immutable after creation.

---

## ResearchHypothesis

* Must describe a single falsifiable hypothesis.
* Cannot exist without a MarketDescription.

---

## Experiment

* Refers to exactly one ResearchHypothesis.
* Executes under exactly one ResearchConfiguration.
* Produces objective Evidence.
* Immutable after completion.

---

## Edge

* Must originate from validated Knowledge.
* Must maintain a valid lifecycle state.

---

# Aggregate Lifecycles

## Experiment

Created

↓

Running

↓

Completed

↓

Archived

---

## Edge

Candidate

↓

Validated

↓

Active

↓

Retired

---

# Relationships

The conceptual domain flow is:

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

This represents conceptual evolution rather than implementation dependencies.

---

# Domain Events

The domain may publish events describing significant business facts.

Examples include:

* ExperimentCompleted
* KnowledgeValidated
* EdgeValidated
* EdgeRetired

The event model will evolve together with the implementation.

---

# Evolution Rules

The Domain Model is considered stable.

Future changes must satisfy all of the following conditions:

* solve a demonstrated business problem;
* preserve the ubiquitous language;
* preserve aggregate invariants;
* remain consistent with the Foundation Blueprint and Manifesto;
* be documented through an Architecture Decision Record (ADR).

The Domain Model evolves incrementally rather than through complete redesigns.
