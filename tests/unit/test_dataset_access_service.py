from edge.application.research.dataset_access_service import DatasetAccessService
from edge.data import DatasetProviderRegistry
from edge.data.providers.query import DatasetQuery
from tests.unit.providers.sample_dataset_providers import HistoricalArchiveProvider


class BackupArchiveProvider(HistoricalArchiveProvider):
    provider_id = "backup-archive"


def test_dataset_access_service_requests_provenanced_dataset():
    registry = DatasetProviderRegistry()
    registry.register(HistoricalArchiveProvider())

    service = DatasetAccessService(registry)

    result = service.request_dataset(symbol="XAUUSD", timeframe="H1")

    assert result.dataset.metadata.symbol == "XAUUSD"
    assert result.provenance.provider_id == "historical-archive"


def test_dataset_access_service_honors_explicit_provider_id():
    registry = DatasetProviderRegistry()
    registry.register(HistoricalArchiveProvider())
    registry.register(BackupArchiveProvider())

    service = DatasetAccessService(registry)

    result = service.request_dataset(
        symbol="XAUUSD",
        timeframe="H1",
        provider_id="backup-archive",
    )

    assert result.provenance.provider_id == "backup-archive"
