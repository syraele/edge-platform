from dataclasses import FrozenInstanceError

import pytest

from edge.domain import Knowledge, KnowledgeCollection


def test_collection_stores_knowledge() -> None:
    first = Knowledge("First conclusion")
    second = Knowledge("Second conclusion")

    collection = KnowledgeCollection(
        knowledge=(first, second)
    )

    assert len(collection.knowledge) == 2
    assert collection.knowledge[0] == first
    assert collection.knowledge[1] == second


def test_collection_has_value_equality() -> None:
    first = Knowledge("Validated conclusion")

    left = KnowledgeCollection(
        knowledge=(first,)
    )

    right = KnowledgeCollection(
        knowledge=(Knowledge("Validated conclusion"),)
    )

    assert left == right


def test_collection_can_be_empty() -> None:
    collection = KnowledgeCollection()

    assert collection.knowledge == ()


def test_collection_is_immutable() -> None:
    collection = KnowledgeCollection()

    with pytest.raises(FrozenInstanceError):
        collection.knowledge = ()