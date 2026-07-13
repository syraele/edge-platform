"""
EDGE_ENGINE
Core Kernel

Il Kernel rappresenta il cuore dell'intero framework.
Da qui verranno inizializzati tutti i componenti del sistema.
"""

from edge.core.config import Config


class Kernel:
    """
    Cuore di EDGE_ENGINE.

    Responsabilità:
    - avviare il sistema
    - mantenere lo stato
    - gestire la configurazione
    - coordinare tutti i servizi
    """

    def __init__(self) -> None:
        self._started = False
        self._services = {}

        # Configurazione centralizzata
        self.config = Config()

    @property
    def started(self) -> bool:
        return self._started

    def start(self) -> None:
        if self._started:
            return

        self._started = True

        print("EDGE_ENGINE Kernel started")

    def stop(self) -> None:
        if not self._started:
            return

        self._started = False

        print("EDGE_ENGINE Kernel stopped")