"""
EDGE_ENGINE

Experiment Executor
"""

from __future__ import annotations

from edge.domain.evidence import Evidence
from edge.domain.experiment import Experiment


class ExperimentExecutor:
    """
    Domain Service responsible for executing an Experiment.

    The ExperimentExecutor transforms an Experiment into
    objective Evidence.

    It contains the domain behaviour required to perform
    a research experiment while remaining independent from
    the Application Layer.
    """

    def execute(self, experiment: Experiment) -> Evidence:
        """
        Execute one Experiment.

        This baseline implementation produces a minimal
        Evidence instance.

        Future milestones will replace this implementation
        with actual quantitative research execution.
        """

        _ = experiment

        return Evidence(
            measurements={}
        )