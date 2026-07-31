from edge.domain import Evidence, Knowledge
from edge.domain.services import (
    CandidateEdgeSelectionConfig,
    CandidateEdgeSelectionService,
    ResearchEvaluator,
)


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


def test_candidate_edge_selection_filters_on_occurrences_and_return() -> None:
    evaluator = ResearchEvaluator()
    service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(
            min_occurrences=5,
            min_average_return_abs=0.01,
        )
    )

    evidence = Evidence(
        measurements={
            "hypothesis_occurrences": 4,
            "hypothesis_average_return": 0.02,
        }
    )

    knowledge = evaluator.evaluate(evidence)
    assert knowledge is not None

    selected, discarded = service.select([knowledge])

    assert selected == []
    assert len(discarded) == 1
    assert "min_occurrences" in discarded[0].reason


def test_candidate_edge_selection_uses_dataset_size_for_large_samples() -> None:
    evaluator = ResearchEvaluator()
    service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(
            min_occurrences=1,
            min_average_return_abs=0.0,
        )
    )

    evidence = Evidence(
        measurements={
            "bars_processed": 1000.0,
            "hypothesis_occurrences": 1,
            "hypothesis_average_return": 0.000001,
        }
    )

    knowledge = evaluator.evaluate(evidence)
    assert knowledge is not None

    selected, discarded = service.select([knowledge])

    assert selected == []
    assert len(discarded) == 1
    assert discarded[0].reason in {"min_occurrences", "min_average_return_abs"}