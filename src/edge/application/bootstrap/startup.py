"""
EDGE_ENGINE

Application Startup
"""

from edge.application.lifecycle.manager import LifecycleManager
from edge.application.components.config_component import ConfigComponent

from edge.context import create_context
from edge.core.engine import EdgeEngine


class EdgeApplication:
    """
    Main application bootstrap.
    """

    def __init__(self):

        self.lifecycle = LifecycleManager()

        self.config = ConfigComponent(
            "config/market.yaml"
        )

        # Load configuration
        self.config.initialize()

        cfg = self.config.get_config()

        market_cfg = cfg["market"]

        self.context = create_context(
            symbol=market_cfg["symbol"],
            timeframe=market_cfg["timeframe"]["main"],
            mode="live",
            data_source=market_cfg["provider"]["name"],
        )

        self.engine = EdgeEngine(
            self.context
        )

        self.lifecycle.register(
            self.config
        )

        self.lifecycle.register(
            self.engine
        )


    def start(self):

        self.lifecycle.initialize()

        self.lifecycle.start()


    def stop(self):

        self.lifecycle.stop()