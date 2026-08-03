import hashlib
import json
from pathlib import Path
from typing import Any

from edge.data.connectors.first_poc import FirstDatasetConnectorProofOfConcept, main
from edge.data.dataset.historical_dataset import HistoricalDataset
from edge.data.providers.local_dataset_registry import LocalDatasetRegistry


def test_first_dataset_connector_poc_writes_manifest_and_checksum(tmp_path: Path) -> None:
    payload = (
        "timestamp,open,high,low,close,volume\n"
        "2024-01-01T00:00:00,1.1000,1.1010,1.0990,1.1005,100\n"
        "2024-01-01T01:00:00,1.2000,1.2050,1.1950,1.2012,110\n"
    )

    connector = FirstDatasetConnectorProofOfConcept(output_root=tmp_path)
    dataset, dataset_dir, manifest = connector.import_dataset(
        symbol="EURUSD",
        timeframe="M1",
        version="v2026-08-03",
        source_name="sample-csv",
        raw_payload=payload,
    )

    assert isinstance(dataset, HistoricalDataset)
    assert dataset.metadata.symbol == "EURUSD"
    assert dataset.metadata.timeframe == "M1"
    assert dataset.metadata.source == "sample-csv"
    assert len(dataset.bars) == 2

    assert dataset_dir == tmp_path / "eurusd" / "m1" / "v2026-08-03"
    assert (dataset_dir / "manifest.json").exists()
    assert (dataset_dir / "bars.csv").exists()
    assert (dataset_dir / "checksum.sha256").exists()

    manifest_payload = json.loads((dataset_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest_payload["dataset_id"] == "eurusd-m1-v2026-08-03"
    assert manifest_payload["bars_count"] == 2
    assert manifest_payload["created_at"] is not None
    assert manifest_payload["checksum"] is not None

    checksum = (dataset_dir / "checksum.sha256").read_text(encoding="utf-8").strip()
    expected_checksum = hashlib.sha256((dataset_dir / "bars.csv").read_bytes()).hexdigest()
    assert checksum == expected_checksum
    assert manifest_payload["checksum"] == expected_checksum

    registry = LocalDatasetRegistry(base_path=tmp_path)
    verified = registry.verify(dataset_dir)
    assert verified["dataset_id"] == "eurusd-m1-v2026-08-03"
    assert verified["bars_count"] == 2
    assert manifest.dataset_id == manifest_payload["dataset_id"]


def test_first_dataset_connector_poc_parses_yahoo_finance_payload(tmp_path: Path) -> None:
    payload = json.dumps(
        {
            "chart": {
                "result": [
                    {
                        "timestamp": [1717200000, 1717286400, 1717372800],
                        "indicators": {
                            "quote": [
                                {
                                    "open": [1.1000, 1.1010, 1.1020],
                                    "high": [1.1010, 1.1025, 1.1030],
                                    "low": [1.0990, 1.1005, 1.1015],
                                    "close": [1.1005, 1.1018, 1.1022],
                                    "volume": [100.0, 110.0, 120.0],
                                }
                            ]
                        },
                    }
                ],
                "error": None,
            }
        }
    )

    connector = FirstDatasetConnectorProofOfConcept(output_root=tmp_path)
    dataset, _, manifest = connector.import_dataset(
        symbol="EURUSD",
        timeframe="D1",
        version="v2026-08-03",
        source_name="yahoo-finance",
        raw_payload=payload,
    )

    assert len(dataset.bars) == 3
    assert dataset.metadata.source == "yahoo-finance"
    assert manifest.bars_count == 3
    assert (tmp_path / "eurusd" / "d1" / "v2026-08-03" / "bars.csv").exists()


def test_first_dataset_connector_poc_fetches_from_yahoo_finance(monkeypatch: Any, tmp_path: Path) -> None:
    payload = {
        "chart": {
            "result": [
                {
                    "timestamp": [1717200000, 1717286400],
                    "indicators": {
                        "quote": [
                            {
                                "open": [1.1000, 1.1010],
                                "high": [1.1010, 1.1020],
                                "low": [1.0990, 1.1005],
                                "close": [1.1005, 1.1012],
                                "volume": [100.0, 110.0],
                            }
                        ]
                    },
                }
            ],
            "error": None,
        }
    }

    class FakeResponse:
        def __init__(self, body: bytes) -> None:
            self._body = body

        def read(self) -> bytes:
            return self._body

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
            return False

    def fake_urlopen(request: Any, timeout: int = 30) -> FakeResponse:
        return FakeResponse(json.dumps(payload).encode("utf-8"))

    monkeypatch.setattr("edge.data.connectors.first_poc.urlopen", fake_urlopen)

    connector = FirstDatasetConnectorProofOfConcept(output_root=tmp_path)
    dataset, _, manifest = connector.import_from_source(
        symbol="EURUSD",
        timeframe="D1",
        version="v2026-08-03",
    )

    assert len(dataset.bars) == 2
    assert dataset.metadata.source == "yahoo-finance"
    assert manifest.bars_count == 2


def test_cli_entrypoint_creates_dataset_artifact(monkeypatch: Any, tmp_path: Path) -> None:
    payload = {
        "chart": {
            "result": [
                {
                    "timestamp": [1717200000],
                    "indicators": {
                        "quote": [
                            {
                                "open": [1.1000],
                                "high": [1.1010],
                                "low": [1.0990],
                                "close": [1.1005],
                                "volume": [100.0],
                            }
                        ]
                    },
                }
            ],
            "error": None,
        }
    }

    class FakeResponse:
        def __init__(self, body: bytes) -> None:
            self._body = body

        def read(self) -> bytes:
            return self._body

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
            return False

    def fake_urlopen(request: Any, timeout: int = 30) -> FakeResponse:
        return FakeResponse(json.dumps(payload).encode("utf-8"))

    monkeypatch.setattr("edge.data.connectors.first_poc.urlopen", fake_urlopen)

    exit_code = main(
        [
            "--symbol",
            "XAUUSD",
            "--timeframe",
            "D1",
            "--version",
            "cli-test",
            "--from",
            "2024-01-01",
            "--to",
            "2024-01-02",
            "--output-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    dataset_dir = tmp_path / "xauusd" / "d1" / "cli-test"
    assert (dataset_dir / "manifest.json").exists()
    assert (dataset_dir / "bars.csv").exists()
