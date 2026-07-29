from dataclasses import FrozenInstanceError

import pytest

from edge.domain import Knowledge


def test_knowledge_stores_statement() -> None:
    knowledge = Knowledge(
        statement="The hypothesis appears reproducible."
    )

    assert knowledge.statement == "The hypothesis appears reproducible."


def test_knowledge_tracks_evidence_reference_and_metadata() -> None:
    knowledge = Knowledge(
        statement="Validated conclusion.",
        evidence_reference="evidence-001",
        metadata={"source": "research_evaluator"},
    )

    assert knowledge.evidence_reference == "evidence-001"
    assert knowledge.metadata["source"] == "research_evaluator"


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