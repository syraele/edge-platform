"""
EDGE_ENGINE

Application Startup
"""

from edge.application.lifecycle.manager import LifecycleManager
from edge.application.components.config_component import ConfigComponent
from edge.application.components.dataset_provider_component import DatasetProviderComponent
from edge.application.components.plugin_component import PluginComponent
from edge.application.research.dataset_access_service import DatasetAccessService

from edge.context import create_context
from edge.core.engine import EdgeEngine


class EdgeApplication:
    """
    Main application bootstrap.
    """

    def __init__(
        self,
        market_config_path: str = "config/market.yaml",
        engine_config_path: str = "config/engine.yaml",
    ):

        self.lifecycle = LifecycleManager()

        self.config = ConfigComponent(
            market_config_path
        )

        self.engine_config = ConfigComponent(
            engine_config_path
        )

        # Load configuration
        self.config.initialize()
        self.engine_config.initialize()

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

        self.plugins = PluginComponent(
            manager=self.context.services.plugin_manager,
            engine_config=self.engine_config.get_config(),
        )

        self.dataset_providers = DatasetProviderComponent(
            registry=self.context.services.dataset_provider_registry,
            engine_config=self.engine_config.get_config(),
        )

        self.dataset_access = DatasetAccessService(
            registry=self.context.services.dataset_provider_registry,
        )

        self.context.services.registry.register(
            "dataset_access_service",
            self.dataset_access,
        )

        self.lifecycle.register(
            self.config
        )

        self.lifecycle.register(
            self.engine
        )

        self.lifecycle.register(
            self.dataset_providers
        )

        self.lifecycle.register(
            self.plugins
        )


    def start(self):

        self.lifecycle.initialize()

        self.lifecycle.start()


    def stop(self):

        self.lifecycle.stop()