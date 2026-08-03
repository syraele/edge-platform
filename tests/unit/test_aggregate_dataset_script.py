from __future__ import annotations

import importlib.util
from pathlib import Path


def test_aggregate_dataset_script_writes_canonical_output(tmp_path: Path) -> None:
    registry_root = tmp_path / "registry"
    output_root = tmp_path / "out"
    dataset_dir = registry_root / "xauusd" / "m1" / "v2024-01"
    dataset_dir.mkdir(parents=True)

    bars_csv = """timestamp,open,high,low,close,volume
2024-01-01T00:00:00+00:00,1.0,1.2,0.9,1.1,100
2024-01-01T00:01:00+00:00,1.1,1.3,1.0,1.2,110
2024-01-01T00:02:00+00:00,1.2,1.4,1.1,1.3,120
2024-01-01T00:03:00+00:00,1.3,1.5,1.2,1.4,130
"""
    (dataset_dir / "bars.csv").write_text(bars_csv, encoding="utf-8")
    (dataset_dir / "manifest.json").write_text(
        '{"dataset_id":"xauusd-m1-v2024-01","symbol":"XAUUSD","timeframe":"M1","version":"v2024-01","source":"mt5","file":"bars.csv","bars_count":4,"range_start":"2024-01-01T00:00:00+00:00","range_end":"2024-01-01T00:03:00+00:00","schema_version":"1.0","created_at":"2024-01-01T00:00:00+00:00","checksum":"dummy"}',
        encoding="utf-8",
    )

    module_path = Path(__file__).resolve().parents[1] / ".." / "tools" / "aggregate_dataset.py"
    spec = importlib.util.spec_from_file_location("aggregate_dataset", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    exit_code = module.main([
        "--symbol",
        "XAUUSD",
        "--version",
        "v2024-01",
        "--target-timeframe",
        "M15",
        "--registry-root",
        str(registry_root),
        "--output-root",
        str(output_root),
    ])

    assert exit_code == 0
    output_dir = output_root / "xauusd" / "m15" / "v2024-01"
    assert (output_dir / "bars.csv").exists()
    assert (output_dir / "manifest.json").exists()
    assert (output_dir / "checksum.sha256").exists()
    manifest_payload = (output_dir / "manifest.json").read_text(encoding="utf-8")
    assert '"timeframe": "M15"' in manifest_payload
    assert '"dataset_id": "xauusd-m15-v2024-01"' in manifest_payload
