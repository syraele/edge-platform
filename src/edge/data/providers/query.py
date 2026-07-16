from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DatasetQuery:
    """Normalized request model for provider dataset loading."""

    symbol: str
    timeframe: str
    start: datetime | None = None
    end: datetime | None = None
    source: str | None = None
    provider_id: str | None = None
