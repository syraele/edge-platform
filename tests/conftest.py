"""
Shared pytest fixtures for EDGE_ENGINE.
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
    Create a fully initialized EdgeContext for unit tests.

    Every test should use this helper instead of manually
    creating ConfigContext, RuntimeState, MarketState, etc.
    """

    return EdgeContext(
        config=ConfigContext(),
        market=MarketState(),
        runtime=RuntimeState(),
        session=SessionInfo(
            symbol=symbol,
            mode=mode,
        ),
        services=Services(),
    )
