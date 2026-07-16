from edge.application.research.dataset_access_service import DatasetAccessService
from edge.data import DatasetProviderRegistry
from tests.unit.providers.sample_dataset_providers import HistoricalArchiveProvider


class BackupArchiveProvider(HistoricalArchiveProvider):
    provider_id = "backup-archive"


class FailingArchiveProvider(HistoricalArchiveProvider):
    provider_id = "failing-archive"

    def load(self, query):
        raise RuntimeError("archive unavailable")


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


def test_dataset_access_service_uses_fallback_provider_when_primary_fails():
    registry = DatasetProviderRegistry()
    registry.register(FailingArchiveProvider())
    registry.register(BackupArchiveProvider())

    service = DatasetAccessService(registry)

    result = service.request_dataset(
        symbol="XAUUSD",
        timeframe="H1",
        provider_id="failing-archive",
        fallback_provider_ids=["backup-archive"],
    )

    assert result.provenance.provider_id == "backup-archive"
