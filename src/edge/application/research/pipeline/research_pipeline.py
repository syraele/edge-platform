"""
EDGE_ENGINE

Research Pipeline
"""

from __future__ import annotations

from typing import Any

from edge.application.research.report import PipelineReport
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession
from edge.domain.services.research_evaluator import ResearchEvaluator
from edge.ml.capability import MachineLearningCapability
from edge.ml.report import MachineLearningReport
from edge.ml.service import MachineLearningService
from edge.optimization.problem import OptimizationProblem
from edge.optimization.report import OptimizationReport
from edge.optimization.service import OptimizationService
from edge.visualization import (
    VisualizationCapability,
    VisualizationDataReference,
    VisualizationReport,
    VisualizationService,
)


class ResearchPipeline:
    """
    Application Layer component responsible for orchestrating
    an entire research execution.

    The pipeline coordinates existing Application and Domain
    components without introducing business logic.
    """

    def __init__(
        self,
        runner: ExperimentRunner,
        evaluator: ResearchEvaluator,
        dataset_access_service: Any | None = None,
        optimization_service: OptimizationService | None = None,
        ml_service: MachineLearningService | None = None,
        visualization_service: VisualizationService | None = None,
    ) -> None:
        self._runner = runner
        self._evaluator = evaluator
        self._dataset_access_service = dataset_access_service
        self._optimization_service = optimization_service
        self._ml_service = ml_service
        self._visualization_service = visualization_service

    def execute(
        self,
        session: ResearchSession,
        dataset_request: dict[str, Any] | None = None,
    ) -> ResearchSession:
        """
        Execute a complete research session.

        The pipeline orchestrates the workflow while delegating
        every business decision to the Domain.
        """

        session.start()

        try:
            if (
                dataset_request is not None
                and self._dataset_access_service is not None
                and session.dataset is None
            ):
                dataset_result = self._dataset_access_service.request_dataset(
                    **dataset_request,
                )
                session.dataset = dataset_result.dataset
                session.dataset_provenance = dataset_result.provenance

            for experiment in session.experiments:
                evidence = self._runner.run(experiment)
                session.evidences.append(evidence)

                knowledge = self._evaluator.evaluate(evidence)

                if knowledge is not None:
                    session.knowledge = knowledge

            session.complete()
            return PipelineReport.from_session(session)

        except Exception as exc:
            session.fail(str(exc))
            raise

    def execute_optimization(
        self,
        problem: OptimizationProblem,
    ) -> OptimizationReport:
        if self._optimization_service is None:
            raise RuntimeError("Optimization service is not configured.")

        return self._optimization_service.optimize(problem)

    def execute_ml_analysis(
        self,
        session: ResearchSession,
        capability: MachineLearningCapability,
        evidence,
    ) -> MachineLearningReport:
        if self._ml_service is None:
            raise RuntimeError("Machine learning service is not configured.")

        report = self._ml_service.analyze(capability, evidence)
        session.ml_report = report
        return report

    def execute_visualization(
        self,
        session: ResearchSession,
        capability: VisualizationCapability,
        payload: dict[str, Any],
        traceability: tuple[VisualizationDataReference, ...] = (),
    ) -> VisualizationReport:
        if self._visualization_service is None:
            raise RuntimeError("Visualization service is not configured.")

        report = self._visualization_service.render(
            capability=capability,
            payload=payload,
            traceability=traceability,
        )
        session.visualization_report = report
        return report

    def execute_visualization_projection(
        self,
        session: ResearchSession,
        capability: VisualizationCapability,
        projection: Any,
    ) -> VisualizationReport:
        if self._visualization_service is None:
            raise RuntimeError("Visualization service is not configured.")

        report = self._visualization_service.render_projection(
            capability,
            projection,
        )
        session.visualization_report = report
        return report