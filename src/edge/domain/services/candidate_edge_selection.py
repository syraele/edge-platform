"""
EDGE_ENGINE

Candidate Edge Selection
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from edge.domain.knowledge import Knowledge


@dataclass(frozen=True, slots=True)
class CandidateEdgeSelectionConfig:
    """Configuration for lightweight candidate-edge filtering."""

    min_occurrences: int = 0
    min_average_return_abs: float = 0.0
    min_average_return_10_abs: float = 0.0
    min_average_return_5_abs: float = 0.0
    min_average_return_1_abs: float = 0.0


@dataclass(frozen=True, slots=True)
class CandidateEdgeSelectionResult:
    """Outcome of candidate-edge selection for a single knowledge item."""

    knowledge: Knowledge
    is_selected: bool
    reason: str


class CandidateEdgeSelectionService:
    """Filter knowledge using only metrics already present in evidence."""

    def __init__(self, config: CandidateEdgeSelectionConfig | None = None) -> None:
        self._config = config or CandidateEdgeSelectionConfig()

    def select(self, knowledge_items: list[Knowledge]) -> tuple[list[Knowledge], list[CandidateEdgeSelectionResult]]:
        selected: list[Knowledge] = []
        discarded: list[CandidateEdgeSelectionResult] = []

        for knowledge in knowledge_items:
            result = self._evaluate(knowledge)
            if result.is_selected:
                selected.append(knowledge)
            else:
                discarded.append(result)

        return selected, discarded

    def _evaluate(self, knowledge: Knowledge) -> CandidateEdgeSelectionResult:
        metadata = dict(knowledge.metadata)
        if not metadata:
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="missing_metrics",
            )

        occurrences = self._read_metric(metadata, "hypothesis_occurrences")
        average_return = self._read_metric(metadata, "hypothesis_average_return")
        average_return_10 = self._read_metric(metadata, "hypothesis_average_return_10")
        average_return_5 = self._read_metric(metadata, "hypothesis_average_return_5")
        average_return_1 = self._read_metric(metadata, "hypothesis_average_return_1")

        if occurrences is None:
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="missing_metrics",
            )

        if occurrences < self._config.min_occurrences:
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="min_occurrences",
            )

        if average_return is not None and abs(average_return) < self._config.min_average_return_abs:
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="min_average_return_abs",
            )

        if (
            average_return_10 is not None
            and self._config.min_average_return_10_abs > 0.0
            and abs(average_return_10) < self._config.min_average_return_10_abs
        ):
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="min_average_return_10_abs",
            )

        if (
            average_return_5 is not None
            and self._config.min_average_return_5_abs > 0.0
            and abs(average_return_5) < self._config.min_average_return_5_abs
        ):
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="min_average_return_5_abs",
            )

        if (
            average_return_1 is not None
            and self._config.min_average_return_1_abs > 0.0
            and abs(average_return_1) < self._config.min_average_return_1_abs
        ):
            return CandidateEdgeSelectionResult(
                knowledge=knowledge,
                is_selected=False,
                reason="min_average_return_1_abs",
            )

        return CandidateEdgeSelectionResult(
            knowledge=knowledge,
            is_selected=True,
            reason="selected",
        )

    @staticmethod
    def _read_metric(metadata: Mapping[str, str], key: str) -> float | None:
        value = metadata.get(key)
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
