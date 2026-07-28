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

        return_sums = {
            "return_1": 0.0,
            "return_5": 0.0,
            "return_10": 0.0,
            "return_20": 0.0,
        }
        return_counts = {
            "return_1": 0,
            "return_5": 0,
            "return_10": 0,
            "return_20": 0,
        }

        for index, bar in enumerate(bars):
            total_return += (bar.close - bar.open) / bar.open
            bars_processed += 1

            current_close = bar.close
            if current_close == 0.0:
                continue

            for horizon_name, horizon in (
                ("return_1", 1),
                ("return_5", 5),
                ("return_10", 10),
                ("return_20", 20),
            ):
                future_index = index + horizon
                if future_index >= len(bars):
                    continue

                future_bar = bars[future_index]
                future_return = (future_bar.close - current_close) / current_close
                return_sums[horizon_name] += future_return
                return_counts[horizon_name] += 1

        average_return = (
            total_return / bars_processed if bars_processed > 0 else 0.0
        )

        average_return_1 = (
            return_sums["return_1"] / return_counts["return_1"]
            if return_counts["return_1"] > 0
            else 0.0
        )
        average_return_5 = (
            return_sums["return_5"] / return_counts["return_5"]
            if return_counts["return_5"] > 0
            else 0.0
        )
        average_return_10 = (
            return_sums["return_10"] / return_counts["return_10"]
            if return_counts["return_10"] > 0
            else 0.0
        )
        average_return_20 = (
            return_sums["return_20"] / return_counts["return_20"]
            if return_counts["return_20"] > 0
            else 0.0
        )

        return Evidence(
            measurements={
                "bars_processed": float(bars_processed),
                "average_return": average_return,
                "average_return_1": average_return_1,
                "average_return_5": average_return_5,
                "average_return_10": average_return_10,
                "average_return_20": average_return_20,
            }
        )