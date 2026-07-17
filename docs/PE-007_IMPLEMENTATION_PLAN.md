# PE-007 Implementation Plan

Status: Implemented

---

# Objective

Implement a deterministic, framework-independent distributed research
coordination layer that aggregates multiple research-session executions without
changing Domain responsibilities or existing single-session pipeline behavior.

# Scope

The implementation covers only:

* immutable workload and unit declarations;
* deterministic workload fingerprinting;
* an application-facing distributed service with failure containment;
* immutable unit-result and aggregated-report models;
* integration through an adapter that can execute declared units via the
  existing `ResearchPipeline`.

Real infrastructure-level distribution is intentionally excluded.

# Planned Repository Changes

1. Add a new `src/edge/distributed/` package for workload, report, and service
   types.
2. Export the new public types from `src/edge/distributed/__init__.py`.
3. Add unit tests for workload validation, deterministic fingerprinting,
   ordered aggregation, and failure containment.
4. Add an integration test proving that a `ResearchPipeline` can be used behind
   the distributed adapter without changing unit/session semantics.
5. Update `PROJECT_STATUS.md` and `README.md` after regression passes.

# Test-First Plan

1. Add a failing unit test for deterministic ordered aggregation of multiple
   successful units.
2. Add a failing unit test for duplicate unit identity rejection.
3. Add a failing unit test for contained unit failures and `partial`/`failed`
   aggregate statuses.
4. Add a failing integration test for coordinating real `ResearchPipeline`
   executions through the distributed adapter.
5. Implement the minimum value objects and service required to satisfy the
   tests.
6. Run targeted distributed tests, then the complete regression suite.

# Acceptance Criteria

* A workload with unique ordered units produces a deterministic distributed
  report.
* Duplicate or empty workloads are rejected explicitly.
* Individual unit failures are contained and do not prevent later units from
  executing.
* Aggregated status, counts, fingerprints, and traceability remain
  deterministic.
* Existing single-session `ResearchPipeline` execution remains valid and
  unchanged.
* All targeted and full regression tests pass.