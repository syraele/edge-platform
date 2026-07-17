from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .capability import VisualizationCapability
from .projection import VisualizationProjection
from .report import VisualizationDataReference


class VisualizationCompositionError(ValueError):
    """Raised when a projection cannot satisfy a visualization capability."""


@dataclass(frozen=True, slots=True)
class VisualizationComposition:
    """Immutable renderer input selected from a visualization projection."""

    session_id: str
    projection_fingerprint: str
    payload: Mapping[str, Any]
    traceability: tuple[VisualizationDataReference, ...]
    fingerprint: str

    @classmethod
    def from_projection(
        cls,
        capability: VisualizationCapability,
        projection: VisualizationProjection,
    ) -> VisualizationComposition:
        selected_sections: dict[str, Any] = {}
        missing_sections: list[str] = []
        unavailable_sections: list[str] = []

        for section_id in capability.required_sections:
            try:
                section = projection.section(section_id)
            except KeyError:
                missing_sections.append(section_id)
                continue

            if section.availability != "available":
                unavailable_sections.append(section_id)
                continue

            selected_sections[section_id] = deepcopy(section.data)

        if missing_sections:
            raise VisualizationCompositionError(
                f"Missing projection sections: {missing_sections}"
            )
        if unavailable_sections:
            raise VisualizationCompositionError(
                f"Unavailable projection sections: {unavailable_sections}"
            )

        frozen_payload = MappingProxyType(selected_sections)
        return cls(
            session_id=projection.session_id,
            projection_fingerprint=projection.fingerprint,
            payload=frozen_payload,
            traceability=projection.traceability,
            fingerprint=cls._build_fingerprint(
                capability,
                projection,
                selected_sections,
            ),
        )

    def to_payload(self) -> dict[str, Any]:
        """Return an isolated payload for a renderer invocation."""

        return deepcopy(dict(self.payload))

    @staticmethod
    def _build_fingerprint(
        capability: VisualizationCapability,
        projection: VisualizationProjection,
        payload: dict[str, Any],
    ) -> str:
        fingerprint_payload = {
            "capability_fingerprint": capability.fingerprint,
            "projection_fingerprint": projection.fingerprint,
            "payload": payload,
            "traceability": [
                {
                    "reference_type": reference.reference_type,
                    "reference_id": reference.reference_id,
                    "fingerprint": reference.fingerprint,
                }
                for reference in projection.traceability
            ],
        }
        encoded = json.dumps(fingerprint_payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()