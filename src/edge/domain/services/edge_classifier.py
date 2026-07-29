"""
EDGE_ENGINE

Edge Classifier
"""

from __future__ import annotations

from edge.domain.knowledge import Knowledge
from edge.domain.services.validation_result import ValidationResult


class EdgeClassifier:
    """
    Classify a Knowledge instance into a practical edge quality tier.

    The classifier uses quantitative metrics already present in the
    knowledge metadata when available and produces a lightweight rating
    that can be used by the next validation stage.
    """

    def classify(self, knowledge: Knowledge | None) -> ValidationResult:
        if knowledge is None:
            return ValidationResult.failure("Knowledge is required to classify an Edge.")

        metadata = knowledge.metadata or {}
        occurrences = self._to_float(metadata.get("hypothesis_occurrences"))
        win_rate = self._to_float(metadata.get("hypothesis_win_rate"))
        expectancy = self._to_float(metadata.get("hypothesis_expectancy"))
        profit_factor = self._to_float(metadata.get("hypothesis_profit_factor"))
        payoff = self._to_float(metadata.get("hypothesis_payoff"))
        drawdown = self._to_float(metadata.get("hypothesis_drawdown"))

        score = 0.0
        if occurrences is not None:
            score += min(occurrences / 20.0, 0.25)
        if win_rate is not None:
            score += min(max(win_rate - 0.5, 0.0) / 0.5, 0.25)
        if expectancy is not None:
            score += min(max(expectancy, 0.0) / 0.02, 0.2)
        if profit_factor is not None:
            score += min(max(profit_factor - 1.0, 0.0) / 0.5, 0.15)
        if payoff is not None:
            score += min(max(payoff, 0.0) / 0.01, 0.1)
        if drawdown is not None:
            score += max(0.0, 0.05 - min(drawdown, 0.05)) / 0.05 * 0.05

        score = min(score, 1.0)

        if occurrences is not None and occurrences >= 10 and win_rate is not None and win_rate >= 0.55 and expectancy is not None and expectancy >= 0.01:
            return ValidationResult.success(label="high_confidence", score=score)

        if occurrences is not None and occurrences >= 5:
            return ValidationResult.failure(label="weak", score=score)

        return ValidationResult.failure(label="weak", score=score)

    @staticmethod
    def _to_float(value: object | None) -> float | None:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(str(value))
        except (TypeError, ValueError):
            return None
