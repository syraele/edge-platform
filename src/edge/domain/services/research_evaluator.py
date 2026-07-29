"""
EDGE_ENGINE

Research Evaluator
"""

from edge.domain import Evidence, Knowledge
from .candidate_edge_selection import CandidateEdgeSelectionService


class ResearchEvaluator:
    """
    Domain Service responsible for evaluating research evidence.

    This baseline implementation transforms objective
    Evidence into validated Knowledge.
    """

    def __init__(self, selection_service: CandidateEdgeSelectionService | None = None) -> None:
        self._selection_service = selection_service

    def evaluate(self, evidence: Evidence) -> Knowledge | None:
        """
        Evaluate Evidence and produce Knowledge.

        Returns:
            Knowledge if objective measurements are present;
            otherwise None.
        """

        if not evidence.measurements:
            return None

        metadata = {
            "source": "research_evaluator",
            "measurement_count": str(len(evidence.measurements)),
        }
        metadata.update({key: str(value) for key, value in evidence.measurements.items()})

        return Knowledge(
            statement="Evidence successfully validated.",
            evidence_reference=str(id(evidence)),
            metadata=metadata,
        )