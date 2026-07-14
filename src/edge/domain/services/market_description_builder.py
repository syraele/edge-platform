"""
EDGE_ENGINE

Market Description Builder
"""

from datetime import datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.domain.descriptor_metadata import DescriptorMetadata
from edge.domain.market_description import MarketDescription


class MarketDescriptionBuilder:
    """
    Domain Service responsible for transforming a HistoricalDataset
    into a MarketDescription.

    This baseline implementation creates a valid immutable
    MarketDescription without extracting descriptors.
    Future milestones will enrich the generated description
    by adding market feature extraction.
    """

    VERSION = "1.0"

    def build(self, dataset: HistoricalDataset) -> MarketDescription:
        """
        Build a MarketDescription from a HistoricalDataset.
        """
        metadata = DescriptorMetadata(
            created_at=datetime.utcnow(),
            builder_version=self.VERSION,
            description_type="baseline",
        )

        return MarketDescription(
            dataset=dataset,
            metadata=metadata,
            descriptors=(),
        )