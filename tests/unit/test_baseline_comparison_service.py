from edge.domain.knowledge import Knowledge
from edge.domain.services.baseline_comparison import (
    BaselineComparisonConfig,
    BaselineComparisonService,
)
from edge.domain.services.candidate_edge_selection import (
    CandidateEdgeSelectionConfig,
    CandidateEdgeSelectionService,
)


def test_baseline_comparison_rejects_hypothesis_without_significant_difference() -> None:
    service = BaselineComparisonService(
        BaselineComparisonConfig(min_effect_size=0.1, min_occurrences=3)
    )

    metadata = {
        "hypothesis_occurrences": "5",
        "hypothesis_average_return": "0.001",
        "average_return": "0.001",
        "hypothesis_average_return_10": "0.001",
        "average_return_10": "0.001",
    }

    result = service.compare(metadata)

    assert result.is_significant is False
    assert result.reason == "baseline_not_significant"


def test_candidate_edge_selection_rejects_when_baseline_is_not_significant() -> None:
    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )

    knowledge = Knowledge(
        statement="baseline-like hypothesis",
        metadata={
            "hypothesis_occurrences": "5",
            "hypothesis_average_return": "0.001",
            "average_return": "0.001",
            "hypothesis_average_return_10": "0.001",
            "average_return_10": "0.001",
        },
    )

    selected, discarded = selection_service.select([knowledge])

    assert selected == []
    assert len(discarded) == 1
    assert discarded[0].reason == "baseline_not_significant"


def test_candidate_edge_selection_accepts_when_baseline_difference_is_significant() -> None:
    selection_service = CandidateEdgeSelectionService(
        CandidateEdgeSelectionConfig(min_occurrences=1, min_average_return_abs=0.0)
    )

    knowledge = Knowledge(
        statement="significant hypothesis",
        metadata={
            "hypothesis_occurrences": "5",
            "hypothesis_average_return": "0.002",
            "average_return": "0.001",
            "hypothesis_average_return_10": "0.003",
            "average_return_10": "0.001",
        },
    )

    selected, discarded = selection_service.select([knowledge])

    assert selected == [knowledge]
    assert discarded == []
