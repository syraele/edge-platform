"""
EDGE_ENGINE

Discovery Report
"""

from __future__ import annotations

from dataclasses import dataclass

from edge.domain.evidence import Evidence
from edge.domain.knowledge import Knowledge
from edge.domain.research_hypothesis import ResearchHypothesis
from .candidate_edge_selection import CandidateEdgeSelectionConfig, CandidateEdgeSelectionResult, CandidateEdgeSelectionService


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
    win_rate: float = 0.0
    expectancy: float = 0.0
    profit_factor: float = 0.0
    payoff: float = 0.0
    drawdown: float = 0.0


@dataclass(frozen=True, slots=True)
class CandidateEdgeSelectionSummary:
    """Summary of knowledge filtering for candidate-edge selection."""

    generated_count: int
    rejected_count: int
    selected_count: int
    rejections: tuple[CandidateEdgeSelectionResult, ...] = ()


@dataclass(frozen=True, slots=True)
class DiscoveryReport:
    """Simple, extensible discovery report container."""

    rows: tuple[DiscoveryReportRow, ...]
    knowledge: Knowledge | None = None
    selection_summary: CandidateEdgeSelectionSummary | None = None


class DiscoveryReportService:
    """Build a readable discovery report from hypotheses and evidence."""

    def __init__(self, selection_service: CandidateEdgeSelectionService | None = None) -> None:
        self._selection_service = selection_service or CandidateEdgeSelectionService(
            CandidateEdgeSelectionConfig()
        )

    def create_report(
        self,
        hypotheses: list[ResearchHypothesis],
        evidences: list[Evidence],
    ) -> DiscoveryReport:
        rows = []
        knowledge_items: list[Knowledge] = []
        knowledge: Knowledge | None = None
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
                    win_rate=evidence.measurements.get("hypothesis_win_rate", 0.0),
                    expectancy=evidence.measurements.get("hypothesis_expectancy", 0.0),
                    profit_factor=evidence.measurements.get("hypothesis_profit_factor", 0.0),
                    payoff=evidence.measurements.get("hypothesis_payoff", 0.0),
                    drawdown=evidence.measurements.get("hypothesis_drawdown", 0.0),
                )
            )
            if evidence.measurements:
                knowledge_item = Knowledge(
                    statement="Evidence successfully validated.",
                    evidence_reference=str(id(evidence)),
                    metadata={
                        "source": "discovery_report",
                        "measurement_count": str(len(evidence.measurements)),
                    } | {k: str(v) for k, v in evidence.measurements.items()},
                )
                knowledge_items.append(knowledge_item)
                if knowledge is None:
                    knowledge = knowledge_item

        selected_knowledge, discarded_results = self._selection_service.select(knowledge_items)
        summary = CandidateEdgeSelectionSummary(
            generated_count=len(knowledge_items),
            rejected_count=len(discarded_results),
            selected_count=len(selected_knowledge),
            rejections=tuple(discarded_results),
        )
        selected_knowledge_item = selected_knowledge[0] if selected_knowledge else None

        ordered_rows = sorted(
            rows,
            key=lambda row: row.average_return_10,
            reverse=True,
        )
        return DiscoveryReport(
            rows=tuple(ordered_rows),
            knowledge=selected_knowledge_item,
            selection_summary=summary,
        )
