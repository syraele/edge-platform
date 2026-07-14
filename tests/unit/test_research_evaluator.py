from edge.domain import Evidence, Knowledge
from edge.domain.services import ResearchEvaluator


def test_evaluator_produces_knowledge_when_measurements_exist() -> None:
    evaluator = ResearchEvaluator()

    evidence = Evidence(
        measurements={
            "profit_factor": 1.80,
        }
    )

    knowledge = evaluator.evaluate(evidence)

    assert isinstance(knowledge, Knowledge)
    assert knowledge.statement == "Evidence successfully validated."


def test_evaluator_returns_none_when_measurements_are_empty() -> None:
    evaluator = ResearchEvaluator()

    evidence = Evidence(
        measurements={}
    )

    knowledge = evaluator.evaluate(evidence)

    assert knowledge is None