from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MachineLearningValidationRule:
    """Declarative validation rule for ML-assisted outputs."""

    minimum_output: float | None = None
    maximum_output: float | None = None


@dataclass(frozen=True, slots=True)
class MachineLearningCapability:
    """Declarative ML-assisted capability used within research workflows."""

    capability_id: str
    capability_name: str
    input_metric_names: tuple[str, ...]
    output_name: str
    assumptions: tuple[str, ...] = ()
    validation_rule: MachineLearningValidationRule | None = None

    @property
    def fingerprint(self) -> str:
        payload = {
            "capability_id": self.capability_id,
            "capability_name": self.capability_name,
            "input_metric_names": list(self.input_metric_names),
            "output_name": self.output_name,
            "assumptions": list(self.assumptions),
            "validation_rule": None
            if self.validation_rule is None
            else {
                "minimum_output": self.validation_rule.minimum_output,
                "maximum_output": self.validation_rule.maximum_output,
            },
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
