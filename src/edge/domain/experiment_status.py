"""
EDGE_ENGINE

Experiment Status
"""

from enum import Enum


class ExperimentStatus(Enum):
    """
    Lifecycle states of an Experiment.
    """

    CREATED = "created"

    RUNNING = "running"

    COMPLETED = "completed"

    ARCHIVED = "archived"