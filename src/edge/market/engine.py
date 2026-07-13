"""
EDGE_ENGINE

Market Data Engine
"""

from edge.context import EdgeContext
from edge.core import BaseEngine

from .provider import MarketDataProvider


class MarketDataEngine(BaseEngine):
    """
    Market engine responsible for receiving market data
    from the configured provider.
    """

    def __init__(
        self,
        context: EdgeContext,
        provider: MarketDataProvider,
    ):

        super().__init__(context)

        self.provider = provider

    def initialize(self) -> bool:

        self.initialized = self.provider.connect()

        return self.initialized

    def start(self) -> bool:

        self.running = True

        return True

    def update(self) -> None:
        """
        Market update loop.

        (Implementation will arrive in Sprint 003)
        """
        pass

    def stop(self) -> None:

        self.provider.disconnect()

        self.running = False

    def health(self) -> dict:

        return {
            "initialized": self.initialized,
            "running": self.running,
            "provider": self.provider.__class__.__name__,
        }