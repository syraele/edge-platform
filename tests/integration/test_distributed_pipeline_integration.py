from edge.application.research.pipeline import ResearchPipeline
from edge.application.research.runner import ExperimentRunner
from edge.application.research.session import ResearchSession, SessionStatus
from edge.distributed import (
    DistributedResearchService,
    DistributedResearchUnit,
    DistributedResearchWorkload,
)
from edge.domain.services import ExperimentExecutor, ResearchEvaluator


class PipelineDistributedExecutor:
    def __init__(self, pipeline: ResearchPipeline) -> None:
        self._pipeline = pipeline

    def execute(self, unit: DistributedResearchUnit):
        return self._pipeline.execute(unit.session, unit.dataset_request)


def test_distributed_service_executes_workload_through_research_pipeline() -> None:
    pipeline = ResearchPipeline(
        runner=ExperimentRunner(ExperimentExecutor()),
        evaluator=ResearchEvaluator(),
    )
    workload = DistributedResearchWorkload(
        workload_id="pipeline-distributed",
        units=(
            DistributedResearchUnit(
                unit_id="unit-a",
                session=ResearchSession(session_id="session-a"),
                execution_context="node-a",
            ),
            DistributedResearchUnit(
                unit_id="unit-b",
                session=ResearchSession(session_id="session-b"),
                execution_context="node-b",
            ),
        ),
        assumptions=("Pipeline executions remain isolated per session.",),
    )

    report = DistributedResearchService(
        PipelineDistributedExecutor(pipeline)
    ).execute(workload)

    assert report.status == "completed"
    assert report.completed_units == 2
    assert report.failed_units == 0
    assert tuple(result.session_id for result in report.unit_results) == (
        "session-a",
        "session-b",
    )
    assert all(result.pipeline_report is not None for result in report.unit_results)
    assert workload.units[0].session.status is SessionStatus.COMPLETED
    assert workload.units[1].session.status is SessionStatus.COMPLETED