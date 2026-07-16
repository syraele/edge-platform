from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from edge.application.research.report.pipeline_report import PipelineReport


@dataclass(frozen=True, slots=True)
class PortfolioResearchReport:
    """Aggregated portfolio-level view of multiple research reports."""

    portfolio_id: str
    units: tuple[PipelineReport, ...]
    research_unit_ids: tuple[str, ...]
    comparison_order: tuple[str, ...]
    provider_ids: tuple[str, ...]
    dataset_sources: tuple[str, ...]
    completed_units: int
    failed_units: int
    evidence_count: int
    knowledge_count: int
    edge_count: int

    created_at: datetime = field(default_factory=datetime.utcnow)
