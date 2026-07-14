"""
EDGE_ENGINE

Experiment
"""

from dataclasses import dataclass

from edge.domain.experiment_status import ExperimentStatus
from edge.domain.research_configuration import ResearchConfiguration
from edge.domain.research_hypothesis import ResearchHypothesis


@dataclass(frozen=True, slots=True)
class Experiment:
    """
    Immutable research experiment.

    An Experiment represents the execution of exactly one
    ResearchHypothesis under exactly one
    ResearchConfiguration.

    The experiment lifecycle is represented by
    ExperimentStatus.
    """

    hypothesis: ResearchHypothesis

    configuration: ResearchConfiguration

    status: ExperimentStatus = ExperimentStatus.CREATED