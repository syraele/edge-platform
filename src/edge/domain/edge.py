"""
EDGE_ENGINE

Edge
"""

from dataclasses import dataclass

from edge.domain.edge_state import EdgeState
from edge.domain.knowledge import Knowledge


@dataclass(frozen=True, slots=True)
class Edge:
    """
    Immutable Edge Aggregate.

    An Edge represents validated quantitative knowledge
    considered operationally useful.

    The Edge lifecycle is represented by EdgeState.
    """

    edge_id: str

    knowledge: Knowledge

    state: EdgeState = EdgeState.CANDIDATE