from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from edge.application.research.report import PipelineReport
from edge.application.research.session import ResearchSession
from edge.ml.report import MachineLearningReport
from edge.optimization.report import OptimizationReport
from edge.portfolio.report import PortfolioResearchReport

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
        portfolio_report: PortfolioResearchReport | None = None,
        optimization_report: OptimizationReport | None = None,
        machine_learning_report: MachineLearningReport | None = None,
    ) -> VisualizationProjection:
        machine_learning_report = machine_learning_report or session.ml_report
        sections = [
            self._build_session_section(session, pipeline_report),
            self._build_dataset_section(session),
            self._build_research_section(session),
            self._build_extensions_section(machine_learning_report),
        ]
        if portfolio_report is not None:
            sections.append(self._build_portfolio_section(portfolio_report))
        if optimization_report is not None:
            sections.append(self._build_optimization_section(optimization_report))
        if machine_learning_report is not None:
            sections.append(
                self._build_machine_learning_section(machine_learning_report)
            )
        section_tuple = tuple(sections)
        traceability = self._build_traceability(
            session,
            pipeline_report,
            portfolio_report,
            optimization_report,
            machine_learning_report,
        )
        return VisualizationProjection(
            session_id=session.session_id,
            sections=section_tuple,
            traceability=traceability,
            fingerprint=self._build_fingerprint(
                session.session_id, section_tuple, traceability
            ),
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
    def _build_extensions_section(
        machine_learning_report: MachineLearningReport | None,
    ) -> VisualizationSection:
        data = {
            "portfolio_available": False,
            "optimization_available": False,
            "machine_learning_available": machine_learning_report is not None,
        }
        availability = "available" if any(data.values()) else "unavailable"
        return VisualizationSection("extensions", availability, data)

    @staticmethod
    def _build_portfolio_section(
        report: PortfolioResearchReport,
    ) -> VisualizationSection:
        return VisualizationSection(
            "portfolio",
            "available",
            {
                "portfolio_id": report.portfolio_id,
                "research_unit_count": len(report.research_unit_ids),
                "comparison_order": list(report.comparison_order),
                "provider_ids": list(report.provider_ids),
                "dataset_sources": list(report.dataset_sources),
                "completed_units": report.completed_units,
                "failed_units": report.failed_units,
                "evidence_count": report.evidence_count,
                "knowledge_count": report.knowledge_count,
                "edge_count": report.edge_count,
            },
        )

    @staticmethod
    def _build_optimization_section(
        report: OptimizationReport,
    ) -> VisualizationSection:
        return VisualizationSection(
            "optimization",
            "available",
            {
                "problem_id": report.problem_id,
                "problem_fingerprint": report.problem_fingerprint,
                "status": report.status,
                "objective_name": report.objective_name,
                "maximize": report.maximize,
                "constraint_count": len(report.constraints),
                "assumptions": list(report.assumptions),
                "ranking": list(report.ranking),
                "winner_configuration": report.winner_configuration,
                "best_objective_value": report.best_objective_value,
                "succeeded_candidates": report.succeeded_candidates,
                "failed_candidates": report.failed_candidates,
                "failure_messages": list(report.failure_messages),
                "run_fingerprint": report.run_fingerprint,
            },
        )

    @staticmethod
    def _build_machine_learning_section(
        report: MachineLearningReport,
    ) -> VisualizationSection:
        return VisualizationSection(
            "machine_learning",
            "available",
            {
                "capability_id": report.capability_id,
                "capability_fingerprint": report.capability_fingerprint,
                "status": report.status,
                "input_metric_names": list(report.input_metric_names),
                "assumption_count": report.assumption_count,
                "assumptions": list(report.result.assumptions),
                "output_name": report.output_name,
                "output_value": report.output_value,
                "failure_message": report.failure_message,
                "run_fingerprint": report.run_fingerprint,
            },
        )

    @staticmethod
    def _build_traceability(
        session: ResearchSession,
        pipeline_report: PipelineReport | None,
        portfolio_report: PortfolioResearchReport | None,
        optimization_report: OptimizationReport | None,
        machine_learning_report: MachineLearningReport | None,
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
        if portfolio_report is not None:
            references.append(
                VisualizationDataReference(
                    reference_type="portfolio_report",
                    reference_id=portfolio_report.portfolio_id,
                )
            )
        if optimization_report is not None:
            references.append(
                VisualizationDataReference(
                    reference_type="optimization_report",
                    reference_id=optimization_report.problem_id,
                    fingerprint=optimization_report.run_fingerprint,
                )
            )
        if machine_learning_report is not None:
            references.append(
                VisualizationDataReference(
                    reference_type="machine_learning_report",
                    reference_id=machine_learning_report.capability_id,
                    fingerprint=machine_learning_report.run_fingerprint,
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
