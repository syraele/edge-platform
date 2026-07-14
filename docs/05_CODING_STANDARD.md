# EDGE_ENGINE Coding Standard

Version: 2.0

Status: Foundation v2

---

# Purpose

This document defines the mandatory coding rules for EDGE_ENGINE.

Its objective is to ensure consistency, maintainability, readability, and long-term evolution of the codebase.

These rules apply to every source file in the project.

---

# General Principles

## CS-001 — Domain First

Business rules belong to the Domain Layer.

No business logic may exist in Infrastructure or Plugins.

---

## CS-002 — Single Responsibility

Every class must have one clearly defined responsibility.

If a class has multiple reasons to change, it should be split.

---

## CS-003 — Explicit Code

Code must be explicit and readable.

Avoid clever solutions when a simpler implementation exists.

---

## CS-004 — Immutability First

Prefer immutable objects.

Mutability must be introduced only when required by the domain.

---

## CS-005 — Composition Over Inheritance

Favor composition instead of inheritance whenever possible.

---

# Domain Rules

## CS-006 — Protect the Domain

The Domain Layer must not depend on frameworks, databases, APIs, or infrastructure.

---

## CS-007 — Rich Domain Model

Business rules belong inside the domain model.

Avoid anemic domain objects.

---

## CS-008 — Value Objects

Value Objects must be immutable.

Equality is based on value.

---

## CS-009 — Aggregate Integrity

Aggregate invariants must never be violated.

Only Aggregate Roots expose public behavior.

---

# Application Rules

## CS-010 — Thin Application Layer

The Application Layer coordinates use cases.

It does not implement business rules.

---

## CS-011 — Dependency Injection

Dependencies must be injected.

Avoid creating dependencies inside business classes.

---

# Infrastructure Rules

## CS-012 — Replaceable Infrastructure

Infrastructure components must be replaceable without modifying the Domain.

---

## CS-013 — External Isolation

External libraries must remain isolated inside Infrastructure.

---

# Testing Rules

## CS-014 — Testability

Business logic must be testable without infrastructure.

---

## CS-015 — Determinism

Tests must be deterministic.

The same inputs must always produce the same outputs.

---

# Naming Rules

## CS-016 — Ubiquitous Language

Use names defined by the Domain Model and Glossary.

Do not invent synonyms.

---

## CS-017 — Meaningful Names

Names must describe business intent.

Avoid abbreviations unless universally accepted.

---

# Complexity Rules

## CS-018 — Small Functions

Functions should perform one logical operation.

---

## CS-019 — No Premature Optimization

Optimize only after measurement demonstrates a need.

---

## CS-020 — Simplicity

Prefer the simplest solution that satisfies the domain requirements.

---

# Governance

Every Pull Request must comply with this Coding Standard.

Exceptions require an Architecture Decision Record (ADR).
