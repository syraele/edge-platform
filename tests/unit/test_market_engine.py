"""
EDGE_ENGINE

MarketDataEngine unit test.
"""

from edge.context import create_context
from edge.market import MarketDataEngine, MarketDataProvider


class DummyProvider(MarketDataProvider):

    def connect(self):

        return True


    def disconnect(self):

        pass


    def tick(self):

        return None



def test_market_engine():

    context = create_context(
        symbol="XAUUSD",
        timeframe="H1",
        mode="test",
        data_source="mock",
    )

    provider = DummyProvider()

    engine = MarketDataEngine(
        context=context,
        provider=provider,
    )

    assert engine.initialize() is True

    assert engine.start() is True

    assert engine.running is True

    health = engine.health()

    assert health["initialized"] is True

    assert health["running"] is True

    engine.stop()

    assert engine.running is False