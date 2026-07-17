from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from edge.application.research.report import PipelineReport
from edge.application.research.session import ResearchSession

from .report import VisualizationDataReference


@dataclass(frozen=True, slots=True)
class VisualizationSection:
    """A named, read-only section of a research visualization projection."""

    section_id: str
    availability: str
    data: dict[str, Any]


@dataclass(frozen=True, slots=True)
class VisualizationProjection:
    """Deterministic renderer input derived from existing research artifacts."""

    session_id: str
    sections: tuple[VisualizationSection, ...]
    traceability: tuple[VisualizationDataReference, ...]
    fingerprint: str

    @property
    def section_ids(self) -> tuple[str, ...]:
        return tuple(section.section_id for section in self.sections)

    def section(self, section_id: str) -> VisualizationSection:
        for section in self.sections:
            if section.section_id == section_id:
                return section
        raise KeyError(f"Unknown visualization section: {section_id}")


class VisualizationProjectionBuilder:
    """Builds a deterministic, read-only projection of a research session."""

    def build(
        self,
        session: ResearchSession,
        pipeline_report: PipelineReport | None = None,
    ) -> VisualizationProjection:
        sections = (
            self._build_session_section(session, pipeline_report),
            self._build_dataset_section(session),
            self._build_research_section(session),
            self._build_extensions_section(session),
        )
        traceability = self._build_traceability(session, pipeline_report)
        return VisualizationProjection(
            session_id=session.session_id,
            sections=sections,
            traceability=traceability,
            fingerprint=self._build_fingerprint(session.session_id, sections, traceability),
        )

    @staticmethod
    def _build_session_section(
        session: ResearchSession,
        pipeline_report: PipelineReport | None,
    ) -> VisualizationSection:
        status = getattr(session.status, "value", str(session.status))
        data: dict[str, Any] = {
            "status": status,
            "created_at": session.created_at.isoformat(),
            "started_at": (
                session.started_at.isoformat() if session.started_at is not None else None
            ),
            "completed_at": (
                session.completed_at.isoformat()
                if session.completed_at is not None
                else None
            ),
            "message": session.message,
            "pipeline_report_id": pipeline_report.report_id if pipeline_report else None,
        }
        return VisualizationSection("session", "available", data)

    @staticmethod
    def _build_dataset_section(session: ResearchSession) -> VisualizationSection:
        if session.dataset is None:
            return VisualizationSection("dataset", "unavailable", {})

        metadata = getattr(session.dataset, "metadata", None)
        provenance = session.dataset_provenance
        return VisualizationSection(
            "dataset",
            "available",
            {
                "symbol": getattr(metadata, "symbol", None),
                "timeframe": getattr(metadata, "timeframe", None),
                "provider_id": getattr(provenance, "provider_id", None),
            },
        )

    @staticmethod
    def _build_research_section(session: ResearchSession) -> VisualizationSection:
        return VisualizationSection(
            "research",
            "available",
            {
                "market_description_available": session.market_description is not None,
                "hypothesis_count": len(session.hypotheses),
                "experiment_count": len(session.experiments),
                "evidence_count": len(session.evidences),
                "knowledge_available": session.knowledge is not None,
                "edge_count": len(session.edges),
            },
        )

    @staticmethod
    def _build_extensions_section(session: ResearchSession) -> VisualizationSection:
        data = {
            "portfolio_available": False,
            "optimization_available": False,
            "machine_learning_available": session.ml_report is not None,
        }
        availability = "available" if any(data.values()) else "unavailable"
        return VisualizationSection("extensions", availability, data)

    @staticmethod
    def _build_traceability(
        session: ResearchSession,
        pipeline_report: PipelineReport | None,
    ) -> tuple[VisualizationDataReference, ...]:
        references = [
            VisualizationDataReference(
                reference_type="research_session",
                reference_id=session.session_id,
            )
        ]
        if pipeline_report is not None:
            references.append(
                VisualizationDataReference(
                    reference_type="pipeline_report",
                    reference_id=pipeline_report.report_id,
                )
            )
        return tuple(references)

    @staticmethod
    def _build_fingerprint(
        session_id: str,
        sections: tuple[VisualizationSection, ...],
        traceability: tuple[VisualizationDataReference, ...],
    ) -> str:
        payload = {
            "session_id": session_id,
            "sections": [
                {
                    "section_id": section.section_id,
                    "availability": section.availability,
                    "data": section.data,
                }
                for section in sections
            ],
            "traceability": [
                {
                    "reference_type": reference.reference_type,
                    "reference_id": reference.reference_id,
                    "fingerprint": reference.fingerprint,
                }
                for reference in traceability
            ],
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
