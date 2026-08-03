"""
EDGE_ENGINE

Domain Services
"""

from .baseline_comparison import (
    BaselineComparisonConfig,
    BaselineComparisonResult,
    BaselineComparisonService,
)
from .candidate_edge_selection import (
    CandidateEdgeSelectionConfig,
    CandidateEdgeSelectionResult,
    CandidateEdgeSelectionService,
)
from .discovery_report import DiscoveryReport, DiscoveryReportRow, DiscoveryReportService, DiscoveryReportSummary
from .edge_classifier import EdgeClassifier
from .edge_manager import EdgeManager
from .edge_scoring import EdgeScoringService, RankedEdge
from .experiment_executor import ExperimentExecutor
from .hypothesis_factory import HypothesisFactory
from .market_description_builder import MarketDescriptionBuilder
from .research_evaluator import ResearchEvaluator

__all__ = [
    "BaselineComparisonConfig",
    "BaselineComparisonResult",
    "BaselineComparisonService",
    "CandidateEdgeSelectionConfig",
    "CandidateEdgeSelectionResult",
    "CandidateEdgeSelectionService",
    "DiscoveryReport",
    "DiscoveryReportRow",
    "DiscoveryReportService",
    "EdgeClassifier",
    "EdgeManager",
    "ExperimentExecutor",
    "HypothesisFactory",
    "MarketDescriptionBuilder",
    "ResearchEvaluator",
]