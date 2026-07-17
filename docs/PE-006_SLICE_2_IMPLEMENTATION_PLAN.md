# PE-006 Slice 2 — Research Session Projection Implementation Plan

Status: Implemented

---

# Objective

Implement a deterministic, framework-independent visualization projection for the existing ResearchSession and PipelineReport. The projection will be the canonical renderer input for the core research chain and will preserve provenance and traceability without mutating application or Domain state.

# Scope

The slice covers only these core sections:

* `session` — identity, lifecycle state, timestamps, message, and pipeline-report identity;
* `dataset` — dataset metadata and provider provenance when available;
* `research` — market description, hypotheses, experiments, evidence, knowledge, and edges;
* `availability` — deterministic declaration of absent optional artifacts.

Portfolio research, optimization, ML, and UI composition are intentionally excluded; they are later PE-006 slices.

# Planned Repository Changes

1. Add projection value objects under `src/edge/visualization/` for a named section and an immutable complete projection.
2. Add an application-facing projection builder under `src/edge/visualization/` that accepts a `ResearchSession` and optional `PipelineReport`.
3. Build named sections in a stable order, preserving source identifiers, session/report metadata, provenance, counts, and traceability references.
4. Represent absent dataset provenance, market description, knowledge, edges, and optional reports explicitly; do not fabricate values.
5. Export the new public types from `src/edge/visualization/__init__.py`.
6. Keep `VisualizationService` renderer-agnostic; it will consume the projection only through its existing payload contract in a subsequent, separately tested integration change if needed.

# Test-First Plan

1. Add unit tests for a complete session projection and assert section order, values, traceability, and deterministic fingerprinting.
2. Add a regression test for a session with absent optional artifacts and assert explicit availability instead of omission or inference.
3. Add a regression test that building a projection does not mutate the session or pipeline report.
4. Add an integration test that a projection can be supplied as the payload for an existing visualization capability without changing pipeline outcomes.
5. Run each new test before implementation, then run the visualization unit tests, research-pipeline integration tests, and the full suite.

# Acceptance Criteria

* A completed or failed ResearchSession can be transformed into a deterministic projection.
* The projection contains stable named core sections and explicit availability state.
* Dataset provenance and report/session identity remain traceable.
* The builder has no Domain mutation or execution responsibility.
* Existing visualization failure containment remains unchanged.
* All targeted and full regression tests pass.

# Review Gate

Implemented with targeted and full regression passing and later synchronized as part of the completed PE-006 milestone.
