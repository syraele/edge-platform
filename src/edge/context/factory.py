"""
EDGE_ENGINE

Context Factory
"""

from __future__ import annotations

from edge.events.event_bus import EventBus
from edge.core.logger import Logger
from edge.core.registry import ServiceRegistry
from edge.data.providers import DatasetProviderRegistry
from edge.plugins import PluginManager

from .config_context import ConfigContext
from .edge_context import EdgeContext
from .market_state import MarketState
from .runtime_state import RuntimeState
from .services_context import Services
from .session_state import SessionInfo


def create_context(
    *,
    symbol: str,
    timeframe: str,
    mode: str,
    data_source: str,
) -> EdgeContext:
    """
    Build a fully initialized EdgeContext.
    """

    logger = Logger()

    event_bus = EventBus()

    registry = ServiceRegistry()

    plugin_manager = PluginManager()

    dataset_provider_registry = DatasetProviderRegistry()

    services = Services(
        logger=logger,
        event_bus=event_bus,
        registry=registry,
        plugin_manager=plugin_manager,
        dataset_provider_registry=dataset_provider_registry,
    )

    registry.register(
        "logger",
        logger,
    )

    registry.register(
        "event_bus",
        event_bus,
    )

    registry.register(
        "services",
        services,
    )

    registry.register(
        "plugin_manager",
        plugin_manager,
    )

    registry.register(
        "dataset_provider_registry",
        dataset_provider_registry,
    )

    config = ConfigContext(
        symbol=symbol,
        timeframe=timeframe,
        mode=mode,
        data_source=data_source,
    )

    market = MarketState()

    runtime = RuntimeState()

    session = SessionInfo(
        symbol=symbol,
        mode=mode,
    )

    return EdgeContext(
        config=config,
        market=market,
        runtime=runtime,
        session=session,
        services=services,
    )