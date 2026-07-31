from __future__ import annotations

from dataclasses import dataclass
from math import log1p

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
        occurrence_term = log1p(max(row.occurrences, 0.0)) * 0.10
        return_term = (
            (row.average_return_10 * 1000.0)
            + (row.average_return_5 * 200.0)
            + (row.average_return_1 * 50.0)
            + (row.average_return * 10.0)
        )
        win_rate_term = row.win_rate * 1.2
        expectancy_term = row.expectancy * 6.0
        profit_factor_term = max(row.profit_factor - 1.0, 0.0) * 1.0
        payoff_term = row.payoff * 0.9
        drawdown_penalty = row.drawdown * 2.5

        return (
            occurrence_term
            + return_term
            + win_rate_term
            + expectancy_term
            + profit_factor_term
            + payoff_term
            - drawdown_penalty
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
