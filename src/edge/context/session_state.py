"""
EDGE_ENGINE

Session Information
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(slots=True, frozen=True)
class SessionInfo:
    """
    Information about current engine session.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    engine_version: str = "0.1.0"

    symbol: str = ""

    mode: str = ""