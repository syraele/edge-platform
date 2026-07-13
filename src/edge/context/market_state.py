"""
EDGE_ENGINE

Market State
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class MarketState:
    """
    Current market snapshot.
    """

    bid: float = 0.0
    ask: float = 0.0
    spread: float = 0.0

    last_price: float = 0.0

    timestamp: datetime = field(default_factory=datetime.utcnow)

    connected: bool = False