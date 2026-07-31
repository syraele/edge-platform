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
    validation_occurrences: float = 0.0
    validation_average_return: float = 0.0
    validation_average_return_1: float = 0.0
    validation_average_return_5: float = 0.0
    validation_average_return_10: float = 0.0
    validation_average_return_20: float = 0.0
    validation_win_rate: float = 0.0
    validation_expectancy: float = 0.0
    validation_profit_factor: float = 0.0
    validation_payoff: float = 0.0
    validation_drawdown: float = 0.0
    confirmed: bool = False


@dataclass(frozen=True, slots=True)
class CandidateEdgeSelectionSummary:
    """Summary of knowledge filtering for candidate-edge selection."""

    generated_count: int
    rejected_count: int
    selected_count: int
    rejections: tuple[CandidateEdgeSelectionResult, ...] = ()


@dataclass(frozen=True, slots=True)
class DiscoveryReportSummary:
    """Aggregate experiment summary for the final report."""

    hypotheses_generated: int
    knowledge_generated: int
    candidate_edges: int
    candidate_edges_confirmed: int
    candidate_edges_rejected: int
    confirmation_rate: float


@dataclass(frozen=True, slots=True)
class DiscoveryReport:
    """Simple, extensible discovery report container."""

    rows: tuple[DiscoveryReportRow, ...]
    knowledge: Knowledge | None = None
    selection_summary: CandidateEdgeSelectionSummary | None = None
    summary: DiscoveryReportSummary | None = None


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
        validation_evidences: list[Evidence] | None = None,
        knowledge_items: list[Knowledge] | None = None,
        knowledge_by_hypothesis: dict[str, Knowledge] | None = None,
    ) -> DiscoveryReport:
        rows = []
        evaluator_knowledge_items = list(knowledge_items or [])
        knowledge: Knowledge | None = None
        validation_metrics_by_statement = {}
        if validation_evidences is not None:
            for hypothesis, evidence in zip(hypotheses, validation_evidences, strict=False):
                validation_metrics_by_statement[hypothesis.statement] = evidence.measurements

        selected_knowledge, discarded_results = self._selection_service.select(evaluator_knowledge_items)
        selected_knowledge_ids = {knowledge_item.knowledge_id for knowledge_item in selected_knowledge}
        knowledge_by_hypothesis = knowledge_by_hypothesis or {}
        has_explicit_mapping = bool(knowledge_by_hypothesis)
        rows_with_selection_flags = []
        for hypothesis, evidence in zip(hypotheses, evidences, strict=False):
            validation_metrics = validation_metrics_by_statement.get(hypothesis.statement, {})
            confirmed = False
            if validation_metrics:
                validation_knowledge = Knowledge(
                    statement="Validation evidence evaluated.",
                    evidence_reference=str(id(validation_metrics)),
                    metadata={"source": "validation", "measurement_count": str(len(validation_metrics))}
                    | {k: str(v) for k, v in validation_metrics.items()},
                )
                selected_validation, _ = self._selection_service.select([validation_knowledge])
                confirmed = bool(selected_validation)

            hypothesis_knowledge = knowledge_by_hypothesis.get(hypothesis.statement)
            if has_explicit_mapping:
                row_is_selected = (
                    hypothesis_knowledge is not None and hypothesis_knowledge.knowledge_id in selected_knowledge_ids
                )
            else:
                row_is_selected = False
            rows_with_selection_flags.append(
                (
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
                        validation_occurrences=validation_metrics.get("hypothesis_occurrences", 0.0),
                        validation_average_return=validation_metrics.get("hypothesis_average_return", 0.0),
                        validation_average_return_1=validation_metrics.get("hypothesis_average_return_1", 0.0),
                        validation_average_return_5=validation_metrics.get("hypothesis_average_return_5", 0.0),
                        validation_average_return_10=validation_metrics.get("hypothesis_average_return_10", 0.0),
                        validation_average_return_20=validation_metrics.get("hypothesis_average_return_20", 0.0),
                        validation_win_rate=validation_metrics.get("hypothesis_win_rate", 0.0),
                        validation_expectancy=validation_metrics.get("hypothesis_expectancy", 0.0),
                        validation_profit_factor=validation_metrics.get("hypothesis_profit_factor", 0.0),
                        validation_payoff=validation_metrics.get("hypothesis_payoff", 0.0),
                        validation_drawdown=validation_metrics.get("hypothesis_drawdown", 0.0),
                        confirmed=confirmed,
                    ),
                    row_is_selected,
                )
            )
        summary = CandidateEdgeSelectionSummary(
            generated_count=len(evaluator_knowledge_items),
            rejected_count=len(discarded_results),
            selected_count=len(selected_knowledge),
            rejections=tuple(discarded_results),
        )
        selected_knowledge_item = selected_knowledge[0] if selected_knowledge else None

        ordered_rows_with_selection_flags = sorted(
            rows_with_selection_flags,
            key=lambda item: item[0].average_return_10,
            reverse=True,
        )
        ordered_rows = tuple(row for row, _ in ordered_rows_with_selection_flags)
        selected_rows_with_selection_flags = [item for item in ordered_rows_with_selection_flags if item[1]]
        if has_explicit_mapping:
            confirmed_count = sum(1 for row, _ in selected_rows_with_selection_flags if row.confirmed)
            selected_rows_count = len(selected_rows_with_selection_flags)
            rejected_count = sum(1 for row, _ in selected_rows_with_selection_flags if not row.confirmed)
            confirmation_rate = (confirmed_count / selected_rows_count * 100.0) if selected_rows_count else 0.0
        else:
            confirmed_count = 0
            selected_rows_count = len(selected_knowledge)
            rejected_count = 0
            confirmation_rate = (confirmed_count / selected_rows_count * 100.0) if selected_rows_count else 0.0
        report_summary = DiscoveryReportSummary(
            hypotheses_generated=len(ordered_rows),
            knowledge_generated=len(evaluator_knowledge_items),
            candidate_edges=selected_rows_count,
            candidate_edges_confirmed=confirmed_count,
            candidate_edges_rejected=rejected_count,
            confirmation_rate=confirmation_rate,
        )
        return DiscoveryReport(
            rows=tuple(ordered_rows),
            knowledge=selected_knowledge_item,
            selection_summary=summary,
            summary=report_summary,
        )
