"""
EDGE_ENGINE

Strategy validation test.
"""

from edge.context.config_context import ConfigContext
from edge.context.market_state import MarketState
from edge.context.runtime_state import RuntimeState
from edge.context.session_state import SessionInfo
from edge.context.services_context import Services
from edge.context.edge_context import EdgeContext


class DummyStrategy:

    def execute(self, context: EdgeContext):

        context.runtime.running = True

        context.market.bid = 3350.10
        context.market.ask = 3350.30
        context.market.last_price = 3350.20


def test_dummy_strategy():

    context = EdgeContext(
        config=ConfigContext(
            symbol="XAUUSD",
            timeframe="M1",
            mode="LIVE",
            data_source="MT5",
        ),
        market=MarketState(),
        runtime=RuntimeState(),
        session=SessionInfo(
            symbol="XAUUSD",
            mode="LIVE",
        ),
        services=Services(),
    )

    strategy = DummyStrategy()

    strategy.execute(context)

    assert context.runtime.running is True

    assert context.market.last_price == 3350.20