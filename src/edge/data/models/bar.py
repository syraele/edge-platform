"""
EDGE_ENGINE

Market Bar Domain Model
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Bar:
    """
    Immutable market bar.

    Represents a single observation of the market
    during a fixed time interval.
    """

    timestamp: datetime

    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    open_interest: float | None = None
    tick_volume: float | None = None
    spread: float | None = None
    body: float | None = None
    range: float | None = None
    body_to_range_ratio: float | None = None
    close_change: float | None = None
    open_change: float | None = None
    high_change: float | None = None
    low_change: float | None = None
    close_return: float | None = None
    volume_change: float | None = None