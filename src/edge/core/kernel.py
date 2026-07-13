"""
EDGE_ENGINE
Core Kernel

Il Kernel rappresenta il cuore dell'intero framework.
Da qui verranno inizializzati tutti i componenti del sistema.
"""


class Kernel:
    """
    Cuore di EDGE_ENGINE.

    Responsabilità:
    - avviare il sistema
    - mantenere lo stato
    - registrare i moduli
    - coordinare tutti i servizi
    """

    def __init__(self):

        self._started = False
        self._services = {}

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