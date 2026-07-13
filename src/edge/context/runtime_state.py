"""
EDGE_ENGINE

Runtime State
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeState:
    """
    Runtime execution state.
    """

    started: bool = False

    running: bool = False

    paused: bool = False

    shutdown_requested: bool = False

    error: bool = False