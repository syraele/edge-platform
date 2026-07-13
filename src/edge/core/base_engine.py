"""
EDGE_ENGINE

Base Engine Contract
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from edge.context import EdgeContext


class BaseEngine(ABC):
    """
    Base class for every engine inside EDGE_ENGINE.
    """

    def __init__(self, context: EdgeContext):

        self.context = context

        self.initialized = False
        self.running = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize engine resources."""
        ...

    @abstractmethod
    def start(self) -> bool:
        """Start engine."""
        ...

    @abstractmethod
    def update(self) -> None:
        """Execute one update cycle."""
        ...

    @abstractmethod
    def stop(self) -> None:
        """Stop engine."""
        ...

    @abstractmethod
    def health(self) -> dict:
        """Return engine health."""
        ...