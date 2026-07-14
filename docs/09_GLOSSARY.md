# EDGE_ENGINE Glossary

Version: 2.0

Status: Foundation v2

---

# Purpose

This document defines the ubiquitous language of EDGE_ENGINE.

Every business concept used throughout the project is defined here to ensure consistency across documentation, architecture, implementation, and testing.

The glossary is the authoritative source for domain terminology.

---

# Domain Concepts

## HistoricalDataset

Immutable collection of historical market data used as the input for quantitative research.

---

## MarketDescription

Structured description of market behaviour extracted from a HistoricalDataset.

It represents the starting point of the research process.

---

## ResearchHypothesis

A falsifiable statement describing an expected market behaviour.

Every hypothesis must be testable through experimentation.

---

## Experiment

Execution of a ResearchHypothesis under controlled conditions.

Its purpose is to generate objective evidence.

---

## Evidence

Objective measurements produced by an Experiment.

Evidence alone does not constitute knowledge.

---

## Knowledge

Validated, reproducible and reusable quantitative conclusions derived from Evidence.

Knowledge is cumulative and represents the primary asset of EDGE_ENGINE.

---

## Edge

Actionable quantitative knowledge demonstrating repeatable value.

Edges are derived from validated Knowledge.

---

# Architectural Concepts

## Domain

The business core of the system.

Contains business rules independent from technology.

---

## Application

Coordinates use cases and orchestrates domain behaviour.

Contains no business rules.

---

## Infrastructure

Implements technical capabilities required by the application.

Infrastructure depends on the Domain, never the opposite.

---

## Plugin

Extension that adds new capabilities without modifying the Core.

Plugins interact through stable contracts.

---

## Aggregate

Cluster of domain objects treated as a single consistency boundary.

Each Aggregate is represented by an Aggregate Root.

---

## Aggregate Root

The only externally accessible entity responsible for preserving aggregate invariants.

---

## Entity

Domain object identified by stable identity.

Equality is based on identity rather than value.

---

## Value Object

Immutable domain object identified entirely by its values.

Equality is value-based.

---

## Domain Service

Business behaviour that does not naturally belong to a single Aggregate.

---

## Domain Event

Immutable record describing a significant business fact that has already occurred.

---

# Research Concepts

## Observation

Objective description of market behaviour prior to interpretation.

---

## Scientific Method

Research process followed by EDGE_ENGINE.

Observation

↓

Research Hypothesis

↓

Experiment

↓

Evidence

↓

Knowledge

↓

Edge

---

# Project Concepts

## Foundation

The stable conceptual basis of the project.

Defines the architecture, domain model, research model and development principles.

---

## Milestone

Incremental development objective delivering measurable project progress.

---

## Architecture Decision Record (ADR)

Document describing an accepted architectural decision and its consequences.

---

## Ubiquitous Language

The shared vocabulary used consistently throughout the project.

All documentation and source code must use these terms without introducing synonyms.

---

# Naming Rule

Every new business concept introduced into EDGE_ENGINE must first be defined in this Glossary before becoming part of the Domain Model or implementation.

This document is the authoritative reference for project terminology.
