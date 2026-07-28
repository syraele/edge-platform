from dataclasses import FrozenInstanceError

import pytest

from edge.domain import Evidence


def test_evidence_stores_measurements() -> None:
    evidence = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        }
    )

    assert evidence.measurements["profit_factor"] == 1.82
    assert evidence.measurements["win_rate"] == 0.61


def test_evidence_supports_optional_metadata() -> None:
    evidence = Evidence(
        measurements={
            "profit_factor": 1.82,
        },
        metadata={
            "dataset": "EURUSD-H1",
            "executor": "baseline",
        },
    )

    assert evidence.metadata["dataset"] == "EURUSD-H1"
    assert evidence.metadata["executor"] == "baseline"


def test_evidence_defaults_metadata_to_empty_mapping() -> None:
    evidence = Evidence(
        measurements={
            "profit_factor": 1.82,
        }
    )

    assert evidence.metadata == {}


def test_evidence_has_value_equality() -> None:
    first = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        },
        metadata={
            "dataset": "EURUSD-H1",
        },
    )

    second = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        },
        metadata={
            "dataset": "EURUSD-H1",
        },
    )

    assert first == second


def test_evidence_is_hashable_and_hash_is_stable_for_equal_values() -> None:
    first = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        },
        metadata={
            "dataset": "EURUSD-H1",
            "executor": "baseline",
        },
    )
    second = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        },
        metadata={
            "dataset": "EURUSD-H1",
            "executor": "baseline",
        },
    )

    assert hash(first) == hash(second)


def test_evidence_cannot_be_reassigned() -> None:
    evidence = Evidence(
        measurements={
            "profit_factor": 1.82,
        }
    )

    with pytest.raises(FrozenInstanceError):
        evidence.measurements = {}


def test_evidence_mappings_cannot_be_mutated() -> None:
    evidence = Evidence(
        measurements={
            "profit_factor": 1.82,
        },
        metadata={
            "dataset": "EURUSD-H1",
        },
    )

    with pytest.raises(TypeError):
        evidence.measurements["profit_factor"] = 2.0

    with pytest.raises(TypeError):
        evidence.metadata["dataset"] = "GBPUSD-H1"