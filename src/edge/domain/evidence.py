"""
EDGE_ENGINE

Evidence
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Evidence:
    """
    Immutable objective measurements produced by an Experiment.

    Evidence represents objective quantitative observations.
    It does not constitute validated Knowledge.
    """

    measurements: dict[str, float]