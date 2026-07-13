"""
EDGE_ENGINE

Market Data Provider
"""

from __future__ import annotations

from .base_provider import BaseProvider


class MarketDataProvider(BaseProvider):
    """
    Base implementation for a concrete market data provider.

    Live providers (MT5, Binance, Interactive Brokers, etc.)
    will inherit from this class.
    """

    def __init__(self) -> None:
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def tick(self):
        """
        Return the next market tick.

        Concrete providers will override this method.
        """
        return None