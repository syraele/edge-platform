import pytest

from edge.data.providers import DatasetProviderDiscoveryError, DatasetProviderLoader


def test_loader_discovers_dataset_provider_from_entrypoint():
    loader = DatasetProviderLoader()

    provider = loader.load(
        {
            "entrypoint": (
                "tests.unit.providers.sample_dataset_providers:HistoricalArchiveProvider"
            ),
            "id": "historical-archive",
        }
    )

    assert provider.provider_id == "historical-archive"


def test_loader_rejects_invalid_entrypoint_format():
    loader = DatasetProviderLoader()

    with pytest.raises(DatasetProviderDiscoveryError):
        loader.load({"entrypoint": "invalid"})


def test_loader_rejects_non_provider_class():
    loader = DatasetProviderLoader()

    with pytest.raises(DatasetProviderDiscoveryError):
        loader.load(
            {
                "entrypoint": (
                    "tests.unit.providers.sample_dataset_providers:NotAProvider"
                )
            }
        )
