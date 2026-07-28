"""
EDGE_ENGINE

Discovery Report
"""

from __future__ import annotations

from dataclasses import dataclass

from edge.domain.evidence import Evidence
from edge.domain.research_hypothesis import ResearchHypothesis


@dataclass(frozen=True, slots=True)
class DiscoveryReportRow:
    """Single row in a discovery report."""

    hypothesis_name: str
    occurrences: float
    average_return: float
    average_return_1: float
    average_return_5: float
    average_return_10: float
    average_return_20: float


@dataclass(frozen=True, slots=True)
class DiscoveryReport:
    """Simple, extensible discovery report container."""

    rows: tuple[DiscoveryReportRow, ...]


class DiscoveryReportService:
    """Build a readable discovery report from hypotheses and evidence."""

    def create_report(
        self,
        hypotheses: list[ResearchHypothesis],
        evidences: list[Evidence],
    ) -> DiscoveryReport:
        rows = []
        for hypothesis, evidence in zip(hypotheses, evidences, strict=False):
            rows.append(
                DiscoveryReportRow(
                    hypothesis_name=hypothesis.statement,
                    occurrences=evidence.measurements.get("hypothesis_occurrences", 0.0),
                    average_return=evidence.measurements.get("hypothesis_average_return", 0.0),
                    average_return_1=evidence.measurements.get("hypothesis_average_return_1", 0.0),
                    average_return_5=evidence.measurements.get("hypothesis_average_return_5", 0.0),
                    average_return_10=evidence.measurements.get("hypothesis_average_return_10", 0.0),
                    average_return_20=evidence.measurements.get("hypothesis_average_return_20", 0.0),
                )
            )

        ordered_rows = sorted(
            rows,
            key=lambda row: row.average_return_10,
            reverse=True,
        )
        return DiscoveryReport(rows=tuple(ordered_rows))
