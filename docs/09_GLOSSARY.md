# EDGE_ENGINE Glossary

---
**Document ID:** GLOSSARY-001
**Version:** 1.0.0
**Status:** Approved
**Owner:** EDGE_ENGINE Project
**Last Updated:** 2026-07-14
---

# Purpose

This document defines the official vocabulary of EDGE_ENGINE.

Every technical document, implementation and discussion should use these terms consistently.

---

# Core Concepts

## Bar

One immutable market observation (OHLCV).

## HistoricalDataset

An immutable collection of historical market data with metadata.

## MarketDescription

An objective description of market behaviour extracted from a HistoricalDataset.

## MarketDescriptor

One measurable characteristic of market behaviour.

Examples:

- Trend
- Volatility
- Noise
- Liquidity
- Momentum
- Efficiency

## MarketVocabulary

A standardized language used to describe market states.

## VocabularyTerm

A single concept within the Market Vocabulary.

## ResearchConfiguration

A deterministic specification of a research experiment.

## Experiment

An executable research hypothesis.

## ExperimentResult

The raw output produced by an experiment.

## Evidence

Statistical measurements extracted from an ExperimentResult.

Evidence supports or rejects a research hypothesis.

## Knowledge

Validated market understanding derived from evidence.

Knowledge is independent from storage.

## Edge

A research hypothesis supported by sufficient evidence.

## ValidatedEdge

An edge approved for continuous monitoring.

---

# Architectural Terms

## Domain

Business knowledge independent from technology.

## Application

Coordinates research workflows.

## Infrastructure

Technical implementations such as storage, files and external services.

## Core

Shared technical building blocks.

---

# Research Terms

## Deterministic

Produces the same result given the same inputs.

## Reproducible

Can be independently repeated with identical results.

## Statistical Validation

Verification that observed behaviour is unlikely to be random.

## Hypothesis

A proposed explanation of observed market behaviour.

---

# Maintenance

The glossary evolves together with the Domain Model.

New business concepts must be added before implementation.

End of Document
