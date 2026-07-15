"""
EDGE_ENGINE

Experiment Runner
"""

from __future__ import annotations

from edge.domain.evidence import Evidence
from edge.domain.experiment import Experiment
from edge.domain.services.experiment_executor import ExperimentExecutor


class ExperimentRunner:
    """
    Application Layer component responsible for coordinating
    the execution of a single Experiment.

    The ExperimentRunner delegates all domain behaviour to the
    Domain ExperimentExecutor and remains stateless between
    executions.
    """

    def __init__(self, executor: ExperimentExecutor) -> None:
        self._executor = executor

    def run(self, experiment: Experiment) -> Evidence:
        """
        Execute a single Experiment.

        Returns
        -------
        Evidence
            The objective measurements produced by the Domain.
        """
        return self._executor.execute(experiment)