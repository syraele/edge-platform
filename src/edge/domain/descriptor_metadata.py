"""
EDGE_ENGINE

Descriptor Metadata
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DescriptorMetadata:
    """
    Immutable metadata describing a MarketDescription.

    Stores contextual information about how and when the
    description was generated.
    """

    created_at: datetime

    builder_version: str

    description_type: str = "baseline"