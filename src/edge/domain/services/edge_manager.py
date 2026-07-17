"""
EDGE_ENGINE

Edge Manager
"""

from __future__ import annotations

from edge.domain.edge import Edge
from edge.domain.edge_collection import EdgeCollection
from edge.domain.edge_state import EdgeState


class EdgeManager:
    """Deterministic management service for collections of edges."""

    def add(self, collection: EdgeCollection, edge: Edge) -> EdgeCollection:
        if any(existing.edge_id == edge.edge_id for existing in collection.edges):
            raise ValueError(f"Edge '{edge.edge_id}' is already registered")

        return EdgeCollection(edges=self._sorted_edges(collection.edges + (edge,)))

    def replace(self, collection: EdgeCollection, edge: Edge) -> EdgeCollection:
        if not any(existing.edge_id == edge.edge_id for existing in collection.edges):
            raise ValueError(f"Edge '{edge.edge_id}' is not registered")

        replaced = tuple(
            edge if existing.edge_id == edge.edge_id else existing
            for existing in collection.edges
        )
        return EdgeCollection(edges=self._sorted_edges(replaced))

    def remove(self, collection: EdgeCollection, edge_id: str) -> EdgeCollection:
        if not any(existing.edge_id == edge_id for existing in collection.edges):
            raise ValueError(f"Edge '{edge_id}' is not registered")

        remaining = tuple(existing for existing in collection.edges if existing.edge_id != edge_id)
        return EdgeCollection(edges=self._sorted_edges(remaining))

    def active_edges(self, collection: EdgeCollection) -> tuple[Edge, ...]:
        return tuple(
            edge for edge in collection.edges if edge.state is EdgeState.ACTIVE
        )

    @staticmethod
    def _sorted_edges(edges: tuple[Edge, ...]) -> tuple[Edge, ...]:
        return tuple(sorted(edges, key=lambda edge: edge.edge_id))