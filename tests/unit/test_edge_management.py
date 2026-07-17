import pytest

from edge.domain import Edge, EdgeCollection, Knowledge
from edge.domain.services import EdgeManager


def _build_edge(edge_id: str) -> Edge:
    return Edge(
        edge_id=edge_id,
        knowledge=Knowledge(statement=f"Knowledge for {edge_id}."),
    )


def test_edge_manager_adds_edges_in_deterministic_order() -> None:
    manager = EdgeManager()
    collection = EdgeCollection()

    collection = manager.add(collection, _build_edge("edge-b"))
    collection = manager.add(collection, _build_edge("edge-a").validate().activate())

    assert tuple(edge.edge_id for edge in collection.edges) == ("edge-a", "edge-b")
    assert tuple(edge.edge_id for edge in manager.active_edges(collection)) == ("edge-a",)


def test_edge_manager_rejects_duplicate_identity() -> None:
    manager = EdgeManager()
    collection = manager.add(EdgeCollection(), _build_edge("edge-a"))

    with pytest.raises(ValueError):
        manager.add(collection, _build_edge("edge-a"))


def test_edge_manager_replaces_existing_edge_by_identity() -> None:
    manager = EdgeManager()
    original = _build_edge("edge-a")
    collection = manager.add(EdgeCollection(), original)

    updated = original.validate()
    collection = manager.replace(collection, updated)

    assert collection.edges == (updated,)


def test_edge_manager_rejects_unknown_removal() -> None:
    manager = EdgeManager()

    with pytest.raises(ValueError):
        manager.remove(EdgeCollection(), "missing-edge")