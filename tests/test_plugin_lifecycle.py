from pathlib import Path

import yaml

from edge.application.bootstrap.startup import EdgeApplication
from tests.unit.plugins.sample_plugins import LifecycleProbePlugin


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")


def test_application_plugin_lifecycle_from_config(tmp_path):
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
        "plugins": {
            "enabled": [
                {
                    "id": "lifecycle-probe",
                    "entrypoint": (
                        "tests.unit.plugins.sample_plugins:LifecycleProbePlugin"
                    ),
                }
            ]
        },
    }

    market_path = tmp_path / "market.yaml"
    engine_path = tmp_path / "engine.yaml"

    _write_yaml(market_path, market_cfg)
    _write_yaml(engine_path, engine_cfg)

    LifecycleProbePlugin.reset()

    app = EdgeApplication(
        market_config_path=str(market_path),
        engine_config_path=str(engine_path),
    )

    app.start()

    assert app.context.services.plugin_manager.is_active("lifecycle-probe") is True
    assert LifecycleProbePlugin.activated == 1

    app.stop()

    assert app.context.services.plugin_manager.is_active("lifecycle-probe") is False
    assert LifecycleProbePlugin.deactivated == 1
