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
        hypothesis_matches = 0
        hypothesis_total_return = 0.0
        hypothesis_positive_returns = 0.0
        hypothesis_negative_returns = 0.0
        hypothesis_winning_trades = 0
        hypothesis_losing_trades = 0
        hypothesis_peak_equity = 0.0
        hypothesis_equity = 0.0
        hypothesis_max_drawdown = 0.0

        return_sums = {
            "return_1": 0.0,
            "return_5": 0.0,
            "return_10": 0.0,
            "return_20": 0.0,
        }
        hypothesis_return_sums = {
            "return_1": 0.0,
            "return_5": 0.0,
            "return_10": 0.0,
            "return_20": 0.0,
        }
        hypothesis_return_counts = {
            "return_1": 0,
            "return_5": 0,
            "return_10": 0,
            "return_20": 0,
        }
        return_counts = {
            "return_1": 0,
            "return_5": 0,
            "return_10": 0,
            "return_20": 0,
        }

        previous_bar = None
        for index, bar in enumerate(bars):
            total_return += (bar.close - bar.open) / bar.open
            bars_processed += 1

            matches_hypothesis = self._matches_hypothesis(
                experiment.hypothesis.statement,
                bar,
                previous_bar,
            )
            if matches_hypothesis:
                hypothesis_matches += 1
                hypothesis_total_return += (bar.close - bar.open) / bar.open
                trade_return = (bar.close - bar.open) / bar.open
                if trade_return > 0.0:
                    hypothesis_winning_trades += 1
                    hypothesis_positive_returns += trade_return
                elif trade_return < 0.0:
                    hypothesis_losing_trades += 1
                    hypothesis_negative_returns += abs(trade_return)

                hypothesis_equity += trade_return
                if hypothesis_equity > hypothesis_peak_equity:
                    hypothesis_peak_equity = hypothesis_equity
                current_drawdown = (hypothesis_peak_equity - hypothesis_equity) / hypothesis_peak_equity if hypothesis_peak_equity > 0.0 else 0.0
                hypothesis_max_drawdown = max(hypothesis_max_drawdown, current_drawdown)

            previous_bar = bar
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

                if matches_hypothesis:
                    hypothesis_return_sums[horizon_name] += future_return
                    hypothesis_return_counts[horizon_name] += 1

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
        hypothesis_average_return = (
            hypothesis_total_return / hypothesis_matches
            if hypothesis_matches > 0
            else 0.0
        )
        hypothesis_win_rate = (
            hypothesis_winning_trades / hypothesis_matches
            if hypothesis_matches > 0
            else 0.0
        )
        hypothesis_expectancy = (
            (hypothesis_positive_returns - hypothesis_negative_returns) / hypothesis_matches
            if hypothesis_matches > 0
            else 0.0
        )
        hypothesis_profit_factor = (
            hypothesis_positive_returns / hypothesis_negative_returns
            if hypothesis_negative_returns > 0.0
            else float("inf") if hypothesis_positive_returns > 0.0 else 0.0
        )
        hypothesis_payoff = (
            hypothesis_positive_returns / hypothesis_winning_trades
            if hypothesis_winning_trades > 0
            else 0.0
        )
        hypothesis_drawdown = hypothesis_max_drawdown
        hypothesis_average_return_1 = (
            hypothesis_return_sums["return_1"] / hypothesis_return_counts["return_1"]
            if hypothesis_return_counts["return_1"] > 0
            else 0.0
        )
        hypothesis_average_return_5 = (
            hypothesis_return_sums["return_5"] / hypothesis_return_counts["return_5"]
            if hypothesis_return_counts["return_5"] > 0
            else 0.0
        )
        hypothesis_average_return_10 = (
            hypothesis_return_sums["return_10"] / hypothesis_return_counts["return_10"]
            if hypothesis_return_counts["return_10"] > 0
            else 0.0
        )
        hypothesis_average_return_20 = (
            hypothesis_return_sums["return_20"] / hypothesis_return_counts["return_20"]
            if hypothesis_return_counts["return_20"] > 0
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
                "hypothesis_matches": float(hypothesis_matches),
                "hypothesis_occurrences": float(hypothesis_matches),
                "hypothesis_average_return": hypothesis_average_return,
                "hypothesis_win_rate": hypothesis_win_rate,
                "hypothesis_expectancy": hypothesis_expectancy,
                "hypothesis_profit_factor": hypothesis_profit_factor,
                "hypothesis_payoff": hypothesis_payoff,
                "hypothesis_drawdown": hypothesis_drawdown,
                "hypothesis_average_return_1": hypothesis_average_return_1,
                "hypothesis_average_return_5": hypothesis_average_return_5,
                "hypothesis_average_return_10": hypothesis_average_return_10,
                "hypothesis_average_return_20": hypothesis_average_return_20,
            }
        )

    @staticmethod
    def _matches_hypothesis(statement: str, bar, previous_bar) -> bool:
        normalized_statement = statement.strip().lower()

        if " and " in normalized_statement:
            parts = [part.strip() for part in normalized_statement.split(" and ")]
            return all(
                ExperimentExecutor._matches_hypothesis(part, bar, previous_bar)
                for part in parts
            )

        if normalized_statement in {"close > open", "close > open"}:
            return bar.close > bar.open
        if normalized_statement in {"close < open", "close < open"}:
            return bar.close < bar.open
        if normalized_statement in {"close > previous close", "close > previous_close"}:
            return previous_bar is not None and bar.close > previous_bar.close
        if normalized_statement in {"close < previous close", "close < previous_close"}:
            return previous_bar is not None and bar.close < previous_bar.close
        if normalized_statement in {"high > previous high", "high > previous_high"}:
            return previous_bar is not None and bar.high > previous_bar.high
        if normalized_statement in {"low < previous low", "low < previous_low"}:
            return previous_bar is not None and bar.low < previous_bar.low

        return False