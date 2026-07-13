"""
EDGE_ENGINE
Core - Service Registry

Registro centrale dei servizi del framework.
"""

from typing import Any


class ServiceRegistry:
    """
    Registro centrale dei servizi.

    Permette di registrare e recuperare
    componenti condivisi dell'applicazione.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Registra un servizio.
        """

        if name in self._services:
            raise ValueError(
                f"Service '{name}' already registered."
            )

        self._services[name] = service

    def get(self, name: str) -> Any:
        """
        Restituisce un servizio.
        """

        if name not in self._services:
            raise KeyError(
                f"Unknown service '{name}'."
            )

        return self._services[name]

    def has(self, name: str) -> bool:
        """
        Verifica l'esistenza del servizio.
        """

        return name in self._services

    def unregister(self, name: str) -> None:
        """
        Rimuove un servizio.
        """

        self._services.pop(name, None)

    def clear(self) -> None:
        """
        Cancella il registro.
        """

        self._services.clear()