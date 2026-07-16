"""
EDGE_ENGINE

Shared Services
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Services:
    """
    Runtime service container.

    Every component accesses shared infrastructure through:

        context.services.logger
        context.services.event_bus
        context.services.registry
        context.services.plugin_manager
        context.services.cache
        context.services.metrics
    """

    logger: Any = None

    event_bus: Any = None

    registry: Any = None

    plugin_manager: Any = None

    cache: Any = None

    metrics: Any = None