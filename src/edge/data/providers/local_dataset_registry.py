from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class DatasetManifest:
    """Manifest metadata for a locally stored dataset."""

    dataset_id: str
    symbol: str
    timeframe: str
    version: str
    source: str
    file: str
    bars_count: int
    range_start: str | None = None
    range_end: str | None = None
    schema_version: str = "1.0"

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "DatasetManifest":
        return cls(
            dataset_id=str(payload.get("dataset_id", "")),
            symbol=str(payload.get("symbol", "")),
            timeframe=str(payload.get("timeframe", "")),
            version=str(payload.get("version", "")),
            source=str(payload.get("source", "unknown")),
            file=str(payload.get("file", "bars.csv")),
            bars_count=int(payload.get("bars_count", 0)),
            range_start=payload.get("range_start"),
            range_end=payload.get("range_end"),
            schema_version=str(payload.get("schema_version", "1.0")),
        )


class LocalDatasetRegistry:
    """Resolve local datasets from a filesystem layout backed by manifest.json."""

    def __init__(self, base_path: str | Path | None = None) -> None:
        self.base_path = Path(base_path or "data/datasets")

    def resolve(self, symbol: str, timeframe: str, version: str | None = None) -> tuple[Path, DatasetManifest]:
        symbol_dir = self.base_path / symbol.lower() / timeframe.lower()
        if not symbol_dir.exists():
            raise FileNotFoundError(f"No local dataset directory found for {symbol}/{timeframe}")

        candidates = sorted(
            [path for path in symbol_dir.iterdir() if path.is_dir()],
            key=lambda path: path.name,
        )
        if version is not None:
            selected = symbol_dir / version
            if not selected.exists():
                raise FileNotFoundError(f"Requested dataset version '{version}' was not found")
            candidates = [selected]

        if not candidates:
            raise FileNotFoundError(f"No dataset versions found for {symbol}/{timeframe}")

        selected_dir = candidates[-1]
        manifest = self._read_manifest(selected_dir / "manifest.json")
        return selected_dir, manifest

    def verify(self, path: str | Path) -> dict[str, Any]:
        dataset_dir = Path(path)
        manifest_path = dataset_dir / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found at {manifest_path}")

        manifest = self._read_manifest(manifest_path)
        data_file = dataset_dir / manifest.file
        if not data_file.exists():
            raise FileNotFoundError(f"Dataset file not found at {data_file}")

        bars_count = self._count_bars(data_file)
        return {
            "dataset_id": manifest.dataset_id,
            "symbol": manifest.symbol,
            "timeframe": manifest.timeframe,
            "version": manifest.version,
            "source": manifest.source,
            "file": manifest.file,
            "bars_count": bars_count,
            "range_start": manifest.range_start,
            "range_end": manifest.range_end,
            "schema_version": manifest.schema_version,
        }

    def list_datasets(self) -> list[str]:
        if not self.base_path.exists():
            return []

        datasets: list[str] = []
        for symbol_dir in sorted(self.base_path.iterdir(), key=lambda path: path.name):
            if not symbol_dir.is_dir():
                continue
            for timeframe_dir in sorted(symbol_dir.iterdir(), key=lambda path: path.name):
                if not timeframe_dir.is_dir():
                    continue
                for version_dir in sorted(timeframe_dir.iterdir(), key=lambda path: path.name):
                    if not version_dir.is_dir():
                        continue
                    manifest_path = version_dir / "manifest.json"
                    if not manifest_path.exists():
                        continue
                    manifest = self._read_manifest(manifest_path)
                    datasets.append(
                        f"{manifest.symbol}\t{manifest.timeframe}\t{manifest.version}\t{manifest.dataset_id}"
                    )

        return datasets

    @staticmethod
    def _read_manifest(path: Path) -> DatasetManifest:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return DatasetManifest.from_mapping(payload)

    @staticmethod
    def _count_bars(path: Path) -> int:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return sum(1 for _ in handle) - 1
