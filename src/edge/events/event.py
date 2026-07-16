"""
EDGE_ENGINE

Domain Event
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class Event:
    """
    Immutable event exchanged through the EventBus.
    """

    name: str

    payload: dict[str, Any]

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))