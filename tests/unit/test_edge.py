from edge.domain import Edge, EdgeState, Knowledge


def test_edge_defaults_to_candidate() -> None:
    knowledge = Knowledge(
        statement="Validated conclusion."
    )

    edge = Edge(
        edge_id="edge-001",
        knowledge=knowledge,
    )

    assert edge.state == EdgeState.CANDIDATE


def test_edge_stores_knowledge() -> None:
    knowledge = Knowledge(
        statement="Validated conclusion."
    )

    edge = Edge(
        edge_id="edge-001",
        knowledge=knowledge,
    )

    assert edge.knowledge == knowledge


def test_edge_has_value_equality() -> None:
    knowledge = Knowledge(
        statement="Validated conclusion."
    )

    first = Edge(
        edge_id="edge-001",
        knowledge=knowledge,
    )

    second = Edge(
        edge_id="edge-001",
        knowledge=knowledge,
    )

    assert first == second