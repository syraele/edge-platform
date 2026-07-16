from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from .session_status import SessionStatus


@dataclass(slots=True)
class ResearchSession:
    """
    Represents a single quantitative research execution.

    The ResearchSession belongs to the Application Layer and is responsible
    only for maintaining the execution context of a research process.
    No domain business logic is implemented here.
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None

    status: SessionStatus = SessionStatus.CREATED

    dataset: Any | None = None
    dataset_provenance: Any | None = None
    ml_report: Any | None = None
    market_description: Any | None = None

    hypotheses: list[Any] = field(default_factory=list)
    experiments: list[Any] = field(default_factory=list)
    evidences: list[Any] = field(default_factory=list)

    knowledge: Any | None = None
    edges: list[Any] = field(default_factory=list)

    message: str | None = None

    def start(self) -> None:
        """Mark the session as running."""
        if self.status is not SessionStatus.CREATED:
            raise RuntimeError("ResearchSession can only be started once.")

        self.status = SessionStatus.RUNNING
        self.started_at = datetime.utcnow()

    def complete(self) -> None:
        """Mark the session as successfully completed."""
        if self.status is not SessionStatus.RUNNING:
            raise RuntimeError("Only a running session can be completed.")

        self.status = SessionStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def fail(self, message: str | None = None) -> None:
        """Mark the session as failed."""
        if self.status.is_terminal:
            raise RuntimeError("ResearchSession has already finished.")

        self.status = SessionStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.message = message