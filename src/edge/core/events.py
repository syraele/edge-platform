from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class Event:

    name: EventType

    payload: dict

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))