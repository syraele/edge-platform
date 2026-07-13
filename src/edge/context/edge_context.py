"""
EDGE_ENGINE

Main Engine Context
"""

from dataclasses import dataclass

from .config_context import ConfigContext
from .market_state import MarketState
from .runtime_state import RuntimeState
from .session_state import SessionInfo
from .services_context import Services


@dataclass(slots=True)
class EdgeContext:
    """
    Central context shared by every engine component.
    """

    config: ConfigContext

    market: MarketState

    runtime: RuntimeState

    session: SessionInfo

    services: Services