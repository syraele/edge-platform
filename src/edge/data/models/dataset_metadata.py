"""
EDGE_ENGINE

Historical Dataset Metadata
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatasetMetadata:
    """
    Immutable metadata describing a historical dataset.
    """

    symbol: str
    timeframe: str

    source: str = "unknown"

    timezone: str = "UTC"

    asset_class: str = "unknown"

    exchange: str = ""

    currency: str = ""