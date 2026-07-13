"""
EDGE_ENGINE
Core Event Bus

Sistema centrale di comunicazione
tra i componenti del framework.
"""

from collections import defaultdict
from typing import Callable, Any


class EventBus:

    def __init__(self) -> None:

        self._listeners: dict[str, list[Callable]] = defaultdict(list)


    def subscribe(
        self,
        event_name: str,
        callback: Callable
    ) -> None:
        """
        Registra un ascoltatore per un evento.
        """

        self._listeners[event_name].append(callback)


    def publish(
        self,
        event_name: str,
        data: Any = None
    ) -> None:
        """
        Pubblica un evento.
        """

        listeners = self._listeners.get(
            event_name,
            []
        )

        for callback in listeners:
            callback(data)


    def unsubscribe(
        self,
        event_name: str,
        callback: Callable
    ) -> None:
        """
        Rimuove un ascoltatore.
        """

        if callback in self._listeners[event_name]:
            self._listeners[event_name].remove(callback)


    def clear(self) -> None:
        """
        Cancella tutti gli eventi.
        """

        self._listeners.clear()