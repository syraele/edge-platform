from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EdgePlugin(ABC):
    """Architectural contract for platform plugins."""

    plugin_id: str
    version: str = "0.0.0"

    @abstractmethod
    def activate(self, context: Any | None = None) -> None:
        """Activate plugin capabilities in a controlled way."""

    @abstractmethod
    def deactivate(self, context: Any | None = None) -> None:
        """Deactivate plugin capabilities and release resources."""
