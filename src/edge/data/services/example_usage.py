from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.models.dataset_metadata import DatasetMetadata
from edge.data.services.timeframe_aggregation_service import TimeframeAggregationService


def build_aggregated_dataset(dataset: HistoricalDataset, target_timeframe: str) -> HistoricalDataset:
    service = TimeframeAggregationService()
    return service.aggregate(dataset, target_timeframe)
