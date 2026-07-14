from edge.domain import Evidence
from edge.domain.services import ResearchEvaluator


def test_evaluator_returns_true_when_measurements_exist() -> None:
    evaluator = ResearchEvaluator()

    evidence = Evidence(
        measurements={
            "profit_factor": 1.80,
        }
    )

    assert evaluator.evaluate(evidence) is True


def test_evaluator_returns_false_when_measurements_are_empty() -> None:
    evaluator = ResearchEvaluator()

    evidence = Evidence(
        measurements={}
    )

    assert evaluator.evaluate(evidence) is False