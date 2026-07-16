from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VisualizationCapability:
    """Declarative visualization capability for research-facing dashboards."""

    capability_id: str
    capability_name: str
    required_sections: tuple[str, ...]
    assumptions: tuple[str, ...] = ()

    @property
    def fingerprint(self) -> str:
        payload = {
            "capability_id": self.capability_id,
            "capability_name": self.capability_name,
            "required_sections": list(self.required_sections),
            "assumptions": list(self.assumptions),
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
