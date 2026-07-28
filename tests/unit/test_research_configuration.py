from dataclasses import FrozenInstanceError

import pytest

from edge.domain.research_configuration import ResearchConfiguration


def test_research_configuration_is_backwards_compatible() -> None:
    configuration = ResearchConfiguration(name="baseline")

    assert configuration.name == "baseline"
    assert configuration.version == "1.0"
    assert configuration.dataset_symbol is None
    assert configuration.dataset_timeframe is None


def test_research_configuration_supports_dataset_descriptor_fields() -> None:
    configuration = ResearchConfiguration(
        name="baseline",
        version="2.0",
        dataset_symbol="EURUSD",
        dataset_timeframe="H1",
    )

    assert configuration.name == "baseline"
    assert configuration.version == "2.0"
    assert configuration.dataset_symbol == "EURUSD"
    assert configuration.dataset_timeframe == "H1"


def test_research_configuration_is_immutable() -> None:
    configuration = ResearchConfiguration(name="baseline")

    with pytest.raises(FrozenInstanceError):
        configuration.name = "updated"


def test_research_configuration_has_value_equality() -> None:
    first = ResearchConfiguration(
        name="baseline",
        dataset_symbol="EURUSD",
        dataset_timeframe="H1",
    )
    second = ResearchConfiguration(
        name="baseline",
        dataset_symbol="EURUSD",
        dataset_timeframe="H1",
    )

    assert first == second


def test_research_configuration_is_hashable() -> None:
    first = ResearchConfiguration(
        name="baseline",
        dataset_symbol="EURUSD",
        dataset_timeframe="H1",
    )
    second = ResearchConfiguration(
        name="baseline",
        dataset_symbol="EURUSD",
        dataset_timeframe="H1",
    )

    assert hash(first) == hash(second)