"""
EDGE_ENGINE

Research Pipeline
"""

from __future__ import annotations

from typing import Any

from edge.application.research.report import PipelineReport
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession
from edge.data import DatasetProviderRegistry, DatasetQuery
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.experiment import Experiment
from edge.domain.experiment_status import ExperimentStatus
from edge.domain.market_description import MarketDescription
from edge.domain.research_configuration import ResearchConfiguration
from edge.domain.research_hypothesis import ResearchHypothesis
from edge.domain.services import (
    CandidateEdgeSelectionService,
    DiscoveryReport,
    DiscoveryReportService,
    ExperimentExecutor,
    HypothesisFactory,
    ResearchEvaluator,
)
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
        registry: DatasetProviderRegistry | None = None,
        optimization_service: OptimizationService | None = None,
        ml_service: MachineLearningService | None = None,
        visualization_service: VisualizationService | None = None,
        selection_service: CandidateEdgeSelectionService | None = None,
    ) -> None:
        self._runner = runner
        self._evaluator = evaluator
        self._dataset_access_service = dataset_access_service
        self._registry = registry
        self._optimization_service = optimization_service
        self._ml_service = ml_service
        self._visualization_service = visualization_service
        self._selection_service = selection_service or CandidateEdgeSelectionService()
        self._hypothesis_factory = HypothesisFactory()
        self._discovery_report_service = DiscoveryReportService(selection_service=self._selection_service)

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
                    selected, _ = self._selection_service.select([knowledge])
                    if selected:
                        session.knowledge = knowledge
                    else:
                        session.knowledge = None

            session.complete()
            return PipelineReport.from_session(session)

        except Exception as exc:
            session.fail(str(exc))
            raise

    def execute_discovery(
        self,
        query: DatasetQuery,
        session: ResearchSession | None = None,
    ) -> DiscoveryReport:
        """Execute a full discovery flow from dataset query to discovery report."""

        active_session = session or ResearchSession()
        active_session.start()

        try:
            if self._registry is not None:
                dataset_result = self._registry.load(query)
            elif self._dataset_access_service is not None:
                dataset_result = self._dataset_access_service.request_dataset(
                    symbol=query.symbol,
                    timeframe=query.timeframe,
                    start=query.start,
                    end=query.end,
                    source=query.source,
                    provider_id=query.provider_id,
                )
            else:
                raise RuntimeError("Dataset provider registry or dataset access service is not configured.")

            dataset = dataset_result.dataset
            active_session.dataset = dataset
            active_session.dataset_provenance = getattr(dataset_result, "provenance", None)

            market_description = MarketDescription(
                dataset=dataset,
                metadata=DescriptorMetadata(
                    created_at=active_session.created_at,
                    builder_version="1.0",
                ),
                descriptors=(),
            )
            active_session.market_description = market_description

            hypotheses = self._hypothesis_factory.create_hypotheses(market_description)
            active_session.hypotheses = hypotheses

            evidences = []
            for hypothesis in hypotheses:
                experiment = Experiment(
                    hypothesis=hypothesis,
                    configuration=ResearchConfiguration(
                        name=hypothesis.statement,
                    ),
                    status=ExperimentStatus.CREATED,
                )
                active_session.experiments.append(experiment)
                evidence = self._runner.run(experiment)
                active_session.evidences.append(evidence)
                evidences.append(evidence)

            report = self._discovery_report_service.create_report(hypotheses, evidences)
            active_session.discovery_report = report
            if report.knowledge is not None:
                active_session.knowledge = report.knowledge
            active_session.complete()
            return report
        except Exception as exc:
            active_session.fail(str(exc))
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