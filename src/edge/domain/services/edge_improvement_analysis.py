from __future__ import annotations

from dataclasses import dataclass

from .discovery_report import DiscoveryReport, DiscoveryReportRow
from .edge_scoring import EdgeScoringService


@dataclass(frozen=True, slots=True)
class EdgeImprovementResult:
    base_hypothesis: str
    compound_hypothesis: str
    occurrence_delta: float
    average_return_delta: float
    edge_score_delta: float
    improves: bool


class EdgeImprovementAnalysisService:
    """Compare a two-primitive compound hypothesis against its base hypothesis."""

    def __init__(self, scoring_service: EdgeScoringService | None = None) -> None:
        self._scoring_service = scoring_service or EdgeScoringService()

    def analyze(self, report: DiscoveryReport) -> list[EdgeImprovementResult]:
        rows = {row.hypothesis_name: row for row in report.rows}
        results: list[EdgeImprovementResult] = []

        for row in report.rows:
            hypothesis_name = row.hypothesis_name
            if " AND " not in hypothesis_name:
                continue

            parts = [part.strip() for part in hypothesis_name.split(" AND ")]
            if len(parts) != 2:
                continue

            base_hypothesis = parts[0]
            base_row = rows.get(base_hypothesis)
            if base_row is None:
                continue

            compound_score = self._scoring_service.score_row(row)
            base_score = self._scoring_service.score_row(base_row)

            result = EdgeImprovementResult(
                base_hypothesis=base_hypothesis,
                compound_hypothesis=hypothesis_name,
                occurrence_delta=row.occurrences - base_row.occurrences,
                average_return_delta=row.average_return - base_row.average_return,
                edge_score_delta=compound_score - base_score,
                improves=(row.occurrences > base_row.occurrences)
                or (row.average_return > base_row.average_return)
                or (compound_score > base_score),
            )
            results.append(result)

        return results
