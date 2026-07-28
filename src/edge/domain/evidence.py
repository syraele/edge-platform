"""
EDGE_ENGINE

Evidence
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class Evidence:
    """
    Immutable objective measurements produced by an Experiment.

    Evidence represents objective quantitative observations.
    It does not constitute validated Knowledge.
    """

    measurements: Mapping[str, float]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Normalize mutable inputs to immutable read-only mappings.
        object.__setattr__(
            self,
            "measurements",
            MappingProxyType(dict(self.measurements)),
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )

    def __hash__(self) -> int:
        measurements_items = tuple(sorted(self.measurements.items()))
        metadata_items = tuple(sorted(self.metadata.items()))
        return hash((measurements_items, metadata_items))