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


def test_evidence_has_value_equality() -> None:
    first = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        }
    )

    second = Evidence(
        measurements={
            "profit_factor": 1.82,
            "win_rate": 0.61,
        }
    )

    assert first == second


def test_evidence_cannot_be_reassigned() -> None:
    evidence = Evidence(
        measurements={
            "profit_factor": 1.82,
        }
    )

    with pytest.raises(FrozenInstanceError):
        evidence.measurements = {}