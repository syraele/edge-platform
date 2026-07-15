"""
EDGE_ENGINE

Research Pipeline
"""

from __future__ import annotations

from edge.application.research.report import PipelineReport
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession
from edge.domain.services.research_evaluator import ResearchEvaluator


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
    ) -> None:
        self._runner = runner
        self._evaluator = evaluator

    def execute(self, session: ResearchSession) -> ResearchSession:
        """
        Execute a complete research session.

        The pipeline orchestrates the workflow while delegating
        every business decision to the Domain.
        """

        session.start()

        try:
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