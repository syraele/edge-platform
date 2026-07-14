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