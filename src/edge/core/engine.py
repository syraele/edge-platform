"""
EDGE_ENGINE

Core Engine
"""

from __future__ import annotations

from edge.context.edge_context import EdgeContext

from .base_engine import BaseEngine


class EdgeEngine(BaseEngine):
    """
    Main application engine.
    """

    def __init__(self, context: EdgeContext) -> None:

        super().__init__(context)

        self.running = False

    def initialize(self) -> bool:

        logger = self.context.services.logger

        if logger:
            logger.info("EdgeEngine initialized")

        self.initialized = True

        return True

    def start(self) -> bool:

        if not self.initialized:
            self.initialize()

        self.running = True

        logger = self.context.services.logger

        if logger:
            logger.info("EdgeEngine started")

        return True

    def update(self) -> None:
        """
        Main engine loop.

        Research Pipeline will arrive in Sprint 002.
        """
        pass

    def stop(self) -> None:

        self.running = False

        logger = self.context.services.logger

        if logger:
            logger.info("EdgeEngine stopped")

    def health(self) -> dict:

        return {
            "initialized": self.initialized,
            "running": self.running,
        }