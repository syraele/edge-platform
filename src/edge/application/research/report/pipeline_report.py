"""
EDGE_ENGINE

Pipeline Report
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from edge.application.research.session import ResearchSession
from edge.application.research.session.session_status import SessionStatus


@dataclass(frozen=True, slots=True)
class PipelineReport:
    """Represents the result of a completed Research Pipeline execution."""

    session_id: str
    status: SessionStatus
    started_at: datetime | None
    completed_at: datetime | None

    dataset: Any | None
    dataset_provenance: Any | None
    market_description: Any | None
    hypotheses: tuple[Any, ...]
    experiments: tuple[Any, ...]
    evidences: tuple[Any, ...]
    knowledge: Any | None
    edges: tuple[Any, ...]
    message: str | None

    report_id: str = field(init=False, default_factory=lambda: str(uuid4()))
    created_at: datetime = field(init=False, default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_session(cls, session: ResearchSession) -> "PipelineReport":
        return cls(
            session_id=session.session_id,
            status=session.status,
            started_at=session.started_at,
            completed_at=session.completed_at,
            dataset=session.dataset,
            dataset_provenance=session.dataset_provenance,
            market_description=session.market_description,
            hypotheses=tuple(session.hypotheses),
            experiments=tuple(session.experiments),
            evidences=tuple(session.evidences),
            knowledge=session.knowledge,
            edges=tuple(session.edges),
            message=session.message,
        )
