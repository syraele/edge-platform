"""
EDGE_ENGINE

Configuration Context

Immutable snapshot of engine configuration.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ConfigContext:
    """
    Immutable engine configuration.
    """

    symbol: str
    timeframe: str
    mode: str
    data_source: str