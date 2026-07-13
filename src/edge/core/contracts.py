"""
EDGE_ENGINE
Core Contracts

Definisce le interfacce fondamentali del framework.
"""

from abc import ABC, abstractmethod
from typing import Any


class IServiceRegistry(ABC):
    """
    Contratto del registro servizi.
    """

    @abstractmethod
    def register(self, name: str, service: Any) -> None:
        ...

    @abstractmethod
    def get(self, name: str) -> Any:
        ...

    @abstractmethod
    def has(self, name: str) -> bool:
        ...

    @abstractmethod
    def unregister(self, name: str) -> None:
        ...


class IConfig(ABC):
    """
    Contratto della configurazione.
    """

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        ...

    @abstractmethod
    def has(self, key: str) -> bool:
        ...