from datetime import UTC, datetime

import pytest

from edge.application.research.report import PipelineReport
from edge.application.research.session import SessionStatus
from edge.data.providers import DatasetProvenance
from edge.portfolio import PortfolioResearchError, PortfolioResearchReport, PortfolioResearchService


def _build_report(
    session_id: str,
    *,
    provider_id: str | None = None,
    dataset_source: str | None = None,
    message: str | None = None,
    evidence_count: int = 1,
    knowledge=None,
):
    provenance = None
    if provider_id is not None and dataset_source is not None:
        provenance = DatasetProvenance(
            provider_id=provider_id,
            provider_version="1.0.0",
            dataset_source=dataset_source,
            retrieved_at=datetime(2024, 1, 1, tzinfo=UTC),
            requested_start=None,
            requested_end=None,
            dataset_start=datetime(2024, 1, 1, tzinfo=UTC),
            dataset_end=datetime(2024, 1, 1, tzinfo=UTC),
            normalization="as_is",
        )

    return PipelineReport(
        session_id=session_id,
        status=SessionStatus.COMPLETED if message is None else SessionStatus.FAILED,
        started_at=datetime(2024, 1, 1, tzinfo=UTC),
        completed_at=datetime(2024, 1, 1, tzinfo=UTC),
        dataset=None,
        dataset_provenance=provenance,
        market_description=None,
        hypotheses=(),
        experiments=(),
        evidences=tuple(object() for _ in range(evidence_count)),
        knowledge=knowledge,
        edges=(),
        message=message,
    )


def test_portfolio_service_aggregates_reports_with_traceability():
    service = PortfolioResearchService()
    reports = [
        _build_report("session-a", provider_id="provider-a", dataset_source="source-a"),
        _build_report(
            "session-b",
            provider_id="provider-b",
            dataset_source="source-b",
            evidence_count=2,
            knowledge=object(),
        ),
    ]

    result = service.aggregate("portfolio-alpha", reports)

    assert isinstance(result, PortfolioResearchReport)
    assert result.portfolio_id == "portfolio-alpha"
    assert result.research_unit_ids == ("session-a", "session-b")
    assert result.comparison_order == ("session-b", "session-a")
    assert result.provider_ids == ("provider-a", "provider-b")
    assert result.dataset_sources == ("source-a", "source-b")
    assert result.completed_units == 2
    assert result.failed_units == 0
    assert result.evidence_count == 3
    assert result.knowledge_count == 1


def test_portfolio_service_rejects_duplicate_session_identity():
    service = PortfolioResearchService()
    duplicate_reports = [
        _build_report("session-a"),
        _build_report("session-a"),
    ]

    with pytest.raises(PortfolioResearchError):
        service.aggregate("portfolio-alpha", duplicate_reports)


def test_portfolio_service_orders_failed_units_last():
    service = PortfolioResearchService()
    reports = [
        _build_report("session-failed", message="failed", evidence_count=3),
        _build_report("session-ok", evidence_count=1),
    ]

    result = service.aggregate("portfolio-alpha", reports)

    assert result.comparison_order == ("session-ok", "session-failed")
