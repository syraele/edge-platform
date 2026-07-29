# Restart Checkpoint — Candidate Edge Selection

Date: 2026-07-29

## Current state

The discovery flow is producing hypotheses, evidence, and a discovery report. The current gap is in the interpretation of candidate edges:

- the discovery report still counts one candidate edge per hypothesis row;
- the Knowledge-based selection service is applied separately, but it is not yet the authoritative filter for the final candidate-edge count.

## Observed issue

With 172 hypotheses and 1 generated knowledge item, the report still exposes 172 candidate edges. This is inconsistent with the expectation that the final candidate-edge set should be derived from the Knowledge selection step.

## Where to resume

The next correction should be made in the discovery report flow, specifically where the report builds the final candidate-edge list from the hypothesis rows instead of from the selected Knowledge items.

## Recommended next action

1. Trace the discovery report construction path.
2. Ensure the final candidate-edge list is derived from the selected Knowledge result.
3. Keep the existing validation/reporting structure intact while aligning the count with the selection logic.

## Repository checkpoint

This note is intended as the restart point for the next implementation step.
