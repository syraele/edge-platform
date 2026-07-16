from pathlib import Path

import yaml

from edge.application.bootstrap.startup import EdgeApplication


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")


def test_application_registers_dataset_providers_from_config(tmp_path):
    market_cfg = {
        "market": {
            "symbol": "XAUUSD",
            "timeframe": {"main": "H1", "execution": "M1"},
            "provider": {"name": "MT5"},
        }
    }

    engine_cfg = {
        "engine": {"name": "EDGE_ENGINE", "version": "1.0"},
        "mode": {"type": "BACKTEST"},
        "logging": {"level": "INFO"},
        "plugins": {"enabled": []},
        "dataset_providers": {
            "enabled": [
                {
                    "id": "historical-archive",
                    "entrypoint": (
                        "tests.unit.providers.sample_dataset_providers:"
                        "HistoricalArchiveProvider"
                    ),
                }
            ]
        },
    }

    market_path = tmp_path / "market.yaml"
    engine_path = tmp_path / "engine.yaml"

    _write_yaml(market_path, market_cfg)
    _write_yaml(engine_path, engine_cfg)

    app = EdgeApplication(
        market_config_path=str(market_path),
        engine_config_path=str(engine_path),
    )

    app.start()

    providers = app.context.services.dataset_provider_registry.list_providers()
    assert providers == ["historical-archive"]

    dataset_access_service = app.context.services.registry.get(
        "dataset_access_service"
    )
    result = dataset_access_service.request_dataset(
        symbol="XAUUSD",
        timeframe="H1",
    )

    assert result.dataset.metadata.symbol == "XAUUSD"
    assert result.provenance.provider_id == "historical-archive"

    app.stop()
