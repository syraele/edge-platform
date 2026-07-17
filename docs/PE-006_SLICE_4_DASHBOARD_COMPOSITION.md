# PE-006 Slice 4 - Dashboard Composition Contract

Status: Approved

---

# Purpose

Define the framework-independent application contract that composes a
`VisualizationProjection` into the deterministic input of a visualization
renderer. The contract makes a capability's declared section requirements
enforceable without exposing Domain objects or report internals to renderers.

# Scope

This slice introduces a read-only visualization composition that:

* selects only the named sections required by a `VisualizationCapability`;
* preserves the capability-declared section order;
* rejects a required section that is absent or explicitly unavailable;
* preserves the projection traceability and projection fingerprint;
* renders a valid composition through `VisualizationService`;
* makes composition available from `ResearchPipeline` without mutating the
  research session or its reports.

# Non-Responsibilities

This slice does not introduce:

* a web framework, user interface, chart library, or dashboard layout;
* generic analytics or operational monitoring;
* execution of research, optimization, portfolio aggregation, or ML analysis;
* mutations to Domain aggregates, sessions, reports, providers, or projections;
* changes to the Foundation v2 architecture or Domain Model.

# Public Interface

The visualization package will expose an immutable composition value object
with:

* the projection session identity and fingerprint;
* the selected named sections as presentation-ready payload data;
* the projection traceability;
* a deterministic composition fingerprint.

`VisualizationService` will expose a renderer-facing method that accepts a
`VisualizationCapability` and a `VisualizationProjection`. It will construct
the composition internally and invoke the renderer only when every required
section is available. Existing dictionary-based rendering remains supported for
backward compatibility.

`ResearchPipeline` will expose a matching projection-based visualization method
and attach the resulting visualization report to the session using the existing
lifecycle behavior.

# Availability Rules

For every value in `VisualizationCapability.required_sections`:

1. the projection must contain a section with that identifier;
2. the section availability must be `available`;
3. the renderer receives only the required section data, in the declared order.

If a requirement is unmet, rendering fails deterministically, the renderer is
not invoked, and the failed report preserves the available projection
traceability and capability assumptions.

# Reproducibility And Traceability

The composition fingerprint is derived deterministically from the capability
fingerprint, projection fingerprint, selected section identifiers and data, and
traceability references. The visualization run fingerprint must incorporate the
composition fingerprint, so an output snapshot remains attributable to the
exact input projection and declared capability.

# Acceptance Criteria

* A valid projection produces a deterministic composition containing only its
  capability's required available sections.
* Missing and unavailable required sections produce contained failures without
  renderer invocation.
* Renderer-facing payloads contain no Domain aggregates or source report
  objects.
* Composition and rendering leave the projection, session, and source reports
  unchanged.
* Pipeline integration attaches a projection-based report without changing the
  research outcome.
* Existing dictionary-based visualization behavior remains compatible.
* Focused visualization and pipeline integration tests, followed by the full
  regression suite, pass.

# Test-First Plan

1. Add failing unit tests for deterministic composition and ordered selection.
2. Add failing unit tests for absent and unavailable required sections and
   assert that the renderer is not called.
3. Add a failing service test proving projection traceability and fingerprinting
   are reflected in the visualization output.
4. Add a failing pipeline integration test for the projection-based path.
5. Implement the minimum composition model and service/pipeline integration.
6. Run the targeted tests, then the complete suite.

# Approval Record

Approved by the project owner through the instruction to proceed according to
the approach judged best for the project on 2026-07-17.