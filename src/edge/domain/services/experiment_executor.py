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

        PR-001 introduces a stable orchestration skeleton for
        the Quantitative Engine entry point.

        The executor remains free of quantitative business
        algorithms at this stage.
        """

        dataset = experiment.hypothesis.market_description.dataset
        bars = dataset.bars

        total_return = 0.0
        bars_processed = 0

        for bar in bars:
            total_return += (bar.close - bar.open) / bar.open
            bars_processed += 1

        average_return = (
            total_return / bars_processed if bars_processed > 0 else 0.0
        )

        return Evidence(
            measurements={
                "bars_processed": float(bars_processed),
                "average_return": average_return,
            }
        )