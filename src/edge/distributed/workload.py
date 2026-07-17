from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from edge.application.research.session import ResearchSession


@dataclass(frozen=True, slots=True)
class DistributedResearchUnit:
    """One declared research execution inside a distributed workload."""

    unit_id: str
    session: ResearchSession
    dataset_request: dict[str, Any] | None = None
    execution_context: str | None = None


@dataclass(frozen=True, slots=True)
class DistributedResearchWorkload:
    """Deterministic declaration of multiple research execution units."""

    workload_id: str
    units: tuple[DistributedResearchUnit, ...]
    assumptions: tuple[str, ...] = ()

    @property
    def fingerprint(self) -> str:
        payload = {
            "workload_id": self.workload_id,
            "units": [
                {
                    "unit_id": unit.unit_id,
                    "session_id": unit.session.session_id,
                    "dataset_request": unit.dataset_request,
                    "execution_context": unit.execution_context,
                }
                for unit in self.units
            ],
            "assumptions": list(self.assumptions),
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()