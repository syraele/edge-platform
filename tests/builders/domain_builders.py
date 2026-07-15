"""
EDGE_ENGINE

Domain Test Builders
"""

from __future__ import annotations

from datetime import datetime

from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.bar import Bar
from edge.data.models.dataset_metadata import DatasetMetadata


def create_test_dataset() -> HistoricalDataset:
    """
    Create a minimal valid HistoricalDataset for unit tests.
    """

    metadata = DatasetMetadata(
        symbol="XAUUSD",
        timeframe="M1",
        source="TEST",
    )

    bar = Bar(
        timestamp=datetime(2024, 1, 1),
        open=2000.0,
        high=2001.0,
        low=1999.0,
        close=2000.5,
        volume=100.0,
    )

    return HistoricalDataset(
        metadata=metadata,
        bars=(bar,),
    )