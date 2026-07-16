"""
EDGE_ENGINE

Market Package Validation
"""

from datetime import UTC, datetime

from edge.context import create_context
from edge.market import (
    MarketDataEngine,
    MarketDataProvider,
    Tick,
)


def test_market_package():

    print("=" * 50)
    print("EDGE_ENGINE - MARKET VALIDATION")
    print("=" * 50)

    # --------------------------------------------------
    # Tick
    # --------------------------------------------------

    tick = Tick(
        bid=2300.0,
        ask=2300.5,
        last=2300.2,
        time=datetime.now(UTC),
    )

    assert tick.last == 2300.2

    print("[OK] Tick created")


    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    context = create_context(
        symbol="XAUUSD",
        timeframe="H1",
        mode="test",
        data_source="mock",
    )

    assert context.config.symbol == "XAUUSD"

    print("[OK] EdgeContext created")


    # --------------------------------------------------
    # Provider
    # --------------------------------------------------

    provider = MarketDataProvider()

    assert provider.connect() is True

    print("[OK] Provider created")


    # --------------------------------------------------
    # Engine
    # --------------------------------------------------

    engine = MarketDataEngine(
        context=context,
        provider=provider,
    )

    assert engine.initialize() is True

    print("[OK] Engine created")


    print("ALL MARKET TESTS PASSED")