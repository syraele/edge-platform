from edge.domain.knowledge import Knowledge
from edge.domain.services.edge_classifier import EdgeClassifier
from edge.domain.services.edge_validator import EdgeValidator


def test_valid_knowledge_passes_validation():
    validator = EdgeValidator()

    knowledge = Knowledge(
        statement="Momentum persists after breakout."
    )

    result = validator.validate(knowledge)

    assert result.is_valid
    assert result.error_count == 0


def test_none_knowledge_fails_validation():
    validator = EdgeValidator()

    result = validator.validate(None)

    assert not result.is_valid
    assert result.error_count == 1
    assert result.errors == (
        "Knowledge is required to create an Edge.",
    )


def test_classifier_marks_high_confidence_edge_from_quantitative_metrics() -> None:
    classifier = EdgeClassifier()

    knowledge = Knowledge(
        statement="Momentum persists after breakout.",
        metadata={
            "hypothesis_occurrences": "18",
            "hypothesis_win_rate": "0.67",
            "hypothesis_expectancy": "0.023",
            "hypothesis_profit_factor": "1.65",
            "hypothesis_payoff": "0.012",
            "hypothesis_drawdown": "0.03",
        },
    )

    result = classifier.classify(knowledge)

    assert result.is_valid
    assert result.label == "high_confidence"
    assert result.score >= 0.8


def test_classifier_marks_weak_edge_when_metrics_are_insufficient() -> None:
    classifier = EdgeClassifier()

    knowledge = Knowledge(
        statement="The pattern is too noisy to trust.",
        metadata={
            "hypothesis_occurrences": "2",
            "hypothesis_win_rate": "0.45",
            "hypothesis_expectancy": "0.001",
            "hypothesis_profit_factor": "1.02",
        },
    )

    result = classifier.classify(knowledge)

    assert not result.is_valid
    assert result.label == "weak"
    assert result.score < 0.5
