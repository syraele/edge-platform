"""
EDGE_ENGINE

Edge State
"""

from enum import Enum


class EdgeState(str, Enum):
    """
    Lifecycle states of an Edge.
    """

    CANDIDATE = "candidate"

    VALIDATED = "validated"

    ACTIVE = "active"

    RETIRED = "retired"