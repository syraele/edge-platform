from datetime import datetime

from edge.domain.experiment import Experiment
from edge.domain.experiment_status import ExperimentStatus
from edge.domain.research_configuration import ResearchConfiguration
from edge.domain.research_hypothesis import ResearchHypothesis
from edge.domain.hypothesis_metadata import HypothesisMetadata
from edge.domain.market_description import MarketDescription
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.domain.evidence import Evidence
from edge.domain.services.research_evaluator import ResearchEvaluator
from edge.optimization import (
    OptimizationConstraint,
    OptimizationProblem,
    OptimizationService,
)


def _build_experiment(configuration_name: str) -> Experiment:
    dataset = HistoricalDataset(
        metadata=DatasetMetadata(symbol="EURUSD", timeframe="M1"),
        bars=(
            Bar(
                timestamp=datetime(2024, 1, 1),
                open=1.0,
                high=2.0,
                low=0.5,
                close=1.5,
            ),
        ),
    )

    market_description = MarketDescription(
        dataset=dataset,
        metadata=DescriptorMetadata(created_at=datetime.utcnow(), builder_version="1.0"),
        descriptors=(),
    )

    hypothesis = ResearchHypothesis(
        market_description=market_description,
        metadata=HypothesisMetadata(created_at=datetime.utcnow()),
        statement=f"hypothesis-{configuration_name}",
    )

    return Experiment(
        hypothesis=hypothesis,
        configuration=ResearchConfiguration(name=configuration_name),
        status=ExperimentStatus.CREATED,
    )


class StubRunner:
    def __init__(self, mapping: dict[str, dict[str, float] | Exception]) -> None:
        self._mapping = mapping

    def run(self, experiment: Experiment) -> Evidence:
        result = self._mapping[experiment.configuration.name]
        if isinstance(result, Exception):
            raise result
        return Evidence(measurements=result)


def test_optimization_service_ranks_candidates_by_objective_descending():
    experiments = (
        _build_experiment("baseline"),
        _build_experiment("improved"),
    )
    service = OptimizationService(
        runner=StubRunner(
            {
                "baseline": {"sharpe": 1.0},
                "improved": {"sharpe": 1.5},
            }
        ),
        evaluator=ResearchEvaluator(),
    )

    report = service.optimize(
        OptimizationProblem(
            problem_id="opt-1",
            objective_name="sharpe",
            experiments=experiments,
        )
    )

    assert report.problem_fingerprint
    assert report.run_fingerprint
    assert report.evaluated_configurations == ("baseline", "improved")
    assert report.status == "completed"
    assert report.assumptions == ()
    assert report.constraints == ()
    assert report.ranking == ("improved", "baseline")
    assert report.winner_configuration == "improved"
    assert report.best_objective_value == 1.5
    assert report.succeeded_candidates == 2
    assert report.failed_candidates == 0


def test_optimization_service_supports_minimize_mode():
    experiments = (
        _build_experiment("slow"),
        _build_experiment("fast"),
    )
    service = OptimizationService(
        runner=StubRunner(
            {
                "slow": {"latency": 3.0},
                "fast": {"latency": 1.0},
            }
        ),
        evaluator=ResearchEvaluator(),
    )

    report = service.optimize(
        OptimizationProblem(
            problem_id="opt-2",
            objective_name="latency",
            experiments=experiments,
            maximize=False,
        )
    )

    assert report.ranking == ("fast", "slow")
    assert report.winner_configuration == "fast"
    assert report.best_objective_value == 1.0


def test_optimization_service_contains_candidate_failures():
    experiments = (
        _build_experiment("broken"),
        _build_experiment("working"),
    )
    service = OptimizationService(
        runner=StubRunner(
            {
                "broken": RuntimeError("execution failed"),
                "working": {"sharpe": 0.5},
            }
        ),
        evaluator=ResearchEvaluator(),
    )

    report = service.optimize(
        OptimizationProblem(
            problem_id="opt-3",
            objective_name="sharpe",
            experiments=experiments,
        )
    )

    assert report.ranking == ("working", "broken")
    assert report.status == "completed"
    assert report.winner_configuration == "working"
    assert report.best_objective_value == 0.5
    assert report.succeeded_candidates == 1
    assert report.failed_candidates == 1
    assert report.failure_messages == ("execution failed",)
    assert any(candidate.message == "execution failed" for candidate in report.candidates)


def test_optimization_service_disqualifies_candidates_that_violate_constraints():
    experiments = (
        _build_experiment("constrained-out"),
        _build_experiment("eligible"),
    )
    service = OptimizationService(
        runner=StubRunner(
            {
                "constrained-out": {"sharpe": 2.0, "drawdown": 0.3},
                "eligible": {"sharpe": 1.0, "drawdown": 0.1},
            }
        ),
        evaluator=ResearchEvaluator(),
    )

    report = service.optimize(
        OptimizationProblem(
            problem_id="opt-4",
            objective_name="sharpe",
            experiments=experiments,
            constraints=(OptimizationConstraint("drawdown", maximum=0.2),),
            assumptions=("Lower drawdown remains preferable.",),
        )
    )

    assert report.assumptions == ("Lower drawdown remains preferable.",)
    assert report.winner_configuration == "eligible"
    assert report.ranking == ("eligible", "constrained-out")
    violating_candidate = next(
        candidate
        for candidate in report.candidates
        if candidate.experiment.configuration.name == "constrained-out"
    )
    assert violating_candidate.constraint_violations == (
        "drawdown above maximum 0.2",
    )


def test_optimization_service_marks_run_failed_when_all_candidates_invalid():
    experiments = (
        _build_experiment("first"),
        _build_experiment("second"),
    )
    service = OptimizationService(
        runner=StubRunner(
            {
                "first": {"sharpe": 1.0, "drawdown": 0.4},
                "second": {"sharpe": 0.8, "drawdown": 0.5},
            }
        ),
        evaluator=ResearchEvaluator(),
    )

    report = service.optimize(
        OptimizationProblem(
            problem_id="opt-5",
            objective_name="sharpe",
            experiments=experiments,
            constraints=(OptimizationConstraint("drawdown", maximum=0.2),),
        )
    )

    assert report.status == "failed"
    assert report.winner_configuration is None
    assert report.best_objective_value is None


def test_optimization_problem_fingerprint_is_deterministic():
    experiments = (
        _build_experiment("baseline"),
        _build_experiment("improved"),
    )

    left = OptimizationProblem(
        problem_id="opt-fingerprint",
        objective_name="sharpe",
        experiments=experiments,
        constraints=(OptimizationConstraint("drawdown", maximum=0.2),),
        assumptions=("Assumption A",),
    )

    right = OptimizationProblem(
        problem_id="opt-fingerprint",
        objective_name="sharpe",
        experiments=experiments,
        constraints=(OptimizationConstraint("drawdown", maximum=0.2),),
        assumptions=("Assumption A",),
    )

    assert left.fingerprint == right.fingerprint
