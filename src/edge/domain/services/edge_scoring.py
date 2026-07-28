from __future__ import annotations

from dataclasses import dataclass

from .discovery_report import DiscoveryReportRow


@dataclass(frozen=True, slots=True)
class RankedEdge:
    hypothesis_name: str
    score: float
    occurrences: float
    average_return: float


class EdgeScoringService:
    """Assign a comparable score to discovery rows for ranking purposes."""

    def score_row(self, row: DiscoveryReportRow) -> float:
        return (
            row.occurrences
            + (row.average_return_10 * 1000.0)
            + (row.average_return_5 * 100.0)
            + (row.average_return_1 * 10.0)
            + (row.average_return * 1.0)
        )

    def rank_rows(self, rows: tuple[DiscoveryReportRow, ...] | list[DiscoveryReportRow]) -> tuple[RankedEdge, ...]:
        ranked = [
            RankedEdge(
                hypothesis_name=row.hypothesis_name,
                score=self.score_row(row),
                occurrences=row.occurrences,
                average_return=row.average_return,
            )
            for row in rows
        ]
        ranked.sort(key=lambda item: item.score, reverse=True)
        return tuple(ranked)
