"""
EDGE_ENGINE
Core Kernel
"""

from edge.core.config import Config
from edge.core.logger import Logger
from edge.core.registry import ServiceRegistry


class Kernel:

    def __init__(self) -> None:

        self._started = False

        self.config = Config()

        self.logger = Logger()

        self.registry = ServiceRegistry()

        self.registry.register(
            "config",
            self.config
        )

        self.registry.register(
            "logger",
            self.logger
        )

    @property
    def started(self) -> bool:
        return self._started

    def start(self) -> None:

        if self._started:
            return

        self._started = True

        self.logger.info(
            "Kernel started."
        )

    def stop(self) -> None:

        if not self._started:
            return

        self._started = False

        self.logger.info(
            "Kernel stopped."
        )