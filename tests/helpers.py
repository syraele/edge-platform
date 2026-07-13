"""
EDGE_ENGINE

Shared testing helpers.
"""

from edge.context import (
    ConfigContext,
    EdgeContext,
    MarketState,
    RuntimeState,
    SessionInfo,
    Services,
)


def create_test_context(
    *,
    symbol: str = "XAUUSD",
    mode: str = "TEST",
) -> EdgeContext:
    """
    Create a fully initialized EdgeContext for tests.
    """

    return EdgeContext(
    config=ConfigContext(
        symbol=symbol,
        timeframe="M1",
        mode=mode,
        data_source="TEST",
    ),
    market=MarketState(),
    runtime=RuntimeState(),
    session=SessionInfo(
        symbol=symbol,
        mode=mode,
    ),
    services=Services(),
)