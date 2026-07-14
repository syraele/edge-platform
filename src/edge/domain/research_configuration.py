"""
EDGE_ENGINE

Research Configuration
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResearchConfiguration:
    """
    Immutable configuration describing how a research
    experiment is executed.

    This baseline version intentionally contains only the
    minimum information required by the Domain Model.
    Future milestones will extend it with experiment
    parameters without changing the Aggregate.
    """

    name: str

    version: str = "1.0"