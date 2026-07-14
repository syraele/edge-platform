from dataclasses import FrozenInstanceError

import pytest

from edge.domain import Knowledge


def test_knowledge_stores_statement() -> None:
    knowledge = Knowledge(
        statement="The hypothesis appears reproducible."
    )

    assert knowledge.statement == "The hypothesis appears reproducible."


def test_knowledge_has_value_equality() -> None:
    first = Knowledge(
        statement="Validated conclusion."
    )

    second = Knowledge(
        statement="Validated conclusion."
    )

    assert first == second


def test_knowledge_cannot_be_modified() -> None:
    knowledge = Knowledge(
        statement="Validated conclusion."
    )

    with pytest.raises(FrozenInstanceError):
        knowledge.statement = "Modified conclusion"