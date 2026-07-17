"""
EDGE_ENGINE

Edge
"""

from dataclasses import dataclass, replace

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

    def validate(self) -> "Edge":
        return self._transition(EdgeState.CANDIDATE, EdgeState.VALIDATED)

    def activate(self) -> "Edge":
        return self._transition(EdgeState.VALIDATED, EdgeState.ACTIVE)

    def retire(self) -> "Edge":
        return self._transition(EdgeState.ACTIVE, EdgeState.RETIRED)

    def _transition(self, expected: EdgeState, target: EdgeState) -> "Edge":
        if self.state is not expected:
            raise ValueError(
                f"Edge transition requires state '{expected.value}', got '{self.state.value}'"
            )

        return replace(self, state=target)