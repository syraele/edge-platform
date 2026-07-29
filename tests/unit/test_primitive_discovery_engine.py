from edge.domain.services.hypothesis_factory import HypothesisFactory
from edge.domain.services.primitive_discovery_engine import PrimitiveDiscoveryEngine
from edge.domain.market_description import MarketDescription
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.research_hypothesis import ResearchHypothesis


def test_primitive_engine_generates_unique_primitive_hypotheses() -> None:
    engine = PrimitiveDiscoveryEngine()
    market_description = MarketDescription(
        dataset=None,
        metadata=DescriptorMetadata(created_at=None, builder_version="test"),
        descriptors=(),
    )

    hypotheses = engine.generate_hypotheses(market_description)

    statements = [hypothesis.statement for hypothesis in hypotheses]
    assert len(hypotheses) == len(set(statements))
    assert "close > open" in statements
    assert "close < open" in statements
    assert "close > previous_close" in statements
    assert "close < previous_close" in statements
    assert "high > previous_high" in statements
    assert "low < previous_low" in statements


def test_hypothesis_factory_uses_primitive_engine() -> None:
    factory = HypothesisFactory()
    market_description = MarketDescription(
        dataset=None,
        metadata=DescriptorMetadata(created_at=None, builder_version="test"),
        descriptors=(),
    )

    hypotheses = factory.create_hypotheses(market_description)

    assert len(hypotheses) > 6
    assert isinstance(hypotheses[0], ResearchHypothesis)


def test_primitive_engine_includes_range_and_volatility_hypotheses() -> None:
    engine = PrimitiveDiscoveryEngine()
    market_description = MarketDescription(
        dataset=None,
        metadata=DescriptorMetadata(created_at=None, builder_version="test"),
        descriptors=(),
    )

    hypotheses = engine.generate_hypotheses(market_description)
    statements = [hypothesis.statement for hypothesis in hypotheses]

    assert "range > previous_range" in statements
    assert "range < previous_range" in statements
    assert "body > half_range" in statements
    assert "body < half_range" in statements
    assert "volatility > previous_volatility" in statements
    assert "volatility < previous_volatility" in statements
