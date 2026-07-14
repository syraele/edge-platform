"""
EDGE_ENGINE

Research Evaluator
"""

from edge.domain import Evidence


class ResearchEvaluator:
    """
    Domain Service responsible for evaluating research evidence.

    This baseline implementation only determines whether
    objective measurements are available.

    Future milestones will extend this service with the
    business rules required to produce validated Knowledge.
    """

    def evaluate(self, evidence: Evidence) -> bool:
        """
        Evaluate evidence.

        Returns True when objective measurements are present.
        """

        return bool(evidence.measurements)