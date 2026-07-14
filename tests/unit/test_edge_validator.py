from edge.domain.knowledge import Knowledge
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
