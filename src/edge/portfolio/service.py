from __future__ import annotations

from edge.application.research.report.pipeline_report import PipelineReport

from .report import PortfolioResearchReport


class PortfolioResearchError(ValueError):
    """Raised when portfolio research aggregation is invalid."""


class PortfolioResearchService:
    """Application-facing aggregation service for portfolio research."""

    @staticmethod
    def _comparison_key(report: PipelineReport) -> tuple[int, int, int, int, str]:
        return (
            0 if report.message is None else 1,
            -1 if report.knowledge is not None else 0,
            -len(report.edges),
            -len(report.evidences),
            report.session_id,
        )

    def aggregate(
        self,
        portfolio_id: str,
        reports: list[PipelineReport] | tuple[PipelineReport, ...],
    ) -> PortfolioResearchReport:
        unit_reports = tuple(reports)

        if not unit_reports:
            raise PortfolioResearchError(
                "Portfolio research requires at least one research unit"
            )

        research_unit_ids = tuple(report.session_id for report in unit_reports)

        if len(set(research_unit_ids)) != len(research_unit_ids):
            raise PortfolioResearchError(
                "Portfolio research units must preserve unique session identities"
            )

        provider_ids = tuple(
            report.dataset_provenance.provider_id
            for report in unit_reports
            if report.dataset_provenance is not None
        )
        dataset_sources = tuple(
            report.dataset_provenance.dataset_source
            for report in unit_reports
            if report.dataset_provenance is not None
        )
        comparison_order = tuple(
            report.session_id
            for report in sorted(unit_reports, key=self._comparison_key)
        )

        return PortfolioResearchReport(
            portfolio_id=portfolio_id,
            units=unit_reports,
            research_unit_ids=research_unit_ids,
            comparison_order=comparison_order,
            provider_ids=provider_ids,
            dataset_sources=dataset_sources,
            completed_units=sum(1 for report in unit_reports if report.message is None),
            failed_units=sum(1 for report in unit_reports if report.message is not None),
            evidence_count=sum(len(report.evidences) for report in unit_reports),
            knowledge_count=sum(1 for report in unit_reports if report.knowledge is not None),
            edge_count=sum(len(report.edges) for report in unit_reports),
        )
