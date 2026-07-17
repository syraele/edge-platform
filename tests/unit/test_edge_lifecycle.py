import pytest

from edge.domain import Edge, EdgeState, Knowledge


def test_edge_can_progress_through_valid_lifecycle() -> None:
    edge = Edge(
        edge_id="edge-001",
        knowledge=Knowledge(statement="Validated conclusion."),
    )

    validated = edge.validate()
    active = validated.activate()
    retired = active.retire()

    assert edge.state is EdgeState.CANDIDATE
    assert validated.state is EdgeState.VALIDATED
    assert active.state is EdgeState.ACTIVE
    assert retired.state is EdgeState.RETIRED


def test_edge_rejects_skipping_lifecycle_states() -> None:
    edge = Edge(
        edge_id="edge-001",
        knowledge=Knowledge(statement="Validated conclusion."),
    )

    with pytest.raises(ValueError):
        edge.activate()


def test_retired_edge_cannot_transition() -> None:
    edge = Edge(
        edge_id="edge-001",
        knowledge=Knowledge(statement="Validated conclusion."),
    ).validate().activate().retire()

    with pytest.raises(ValueError):
        edge.activate()