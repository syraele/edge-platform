from __future__ import annotations

import hashlib
import json
from typing import Any

from .capability import VisualizationCapability
from .report import (
    VisualizationDataReference,
    VisualizationReport,
    VisualizationResult,
)


class VisualizationError(ValueError):
    """Raised when visualization generation cannot be executed."""


class VisualizationService:
    """Application-facing service for deterministic research visualizations."""

    def __init__(self, renderer: Any) -> None:
        self._renderer = renderer

    def render(
        self,
        capability: VisualizationCapability,
        payload: dict[str, Any],
        traceability: tuple[VisualizationDataReference, ...] = (),
    ) -> VisualizationReport:
        missing_sections = [
            section
            for section in capability.required_sections
            if section not in payload
        ]

        if missing_sections:
            result = VisualizationResult(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                rendered_sections=(),
                snapshot={},
                traceability=traceability,
                assumptions=capability.assumptions,
                message=f"Missing payload sections: {missing_sections}",
            )
            return VisualizationReport(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                status="failed",
                result=result,
                rendered_sections=result.rendered_sections,
                traceability_count=len(result.traceability),
                assumption_count=len(result.assumptions),
                failure_message=result.message,
                run_fingerprint=self._build_run_fingerprint(result),
            )

        try:
            snapshot = self._renderer.render(capability, payload, traceability)
            result = VisualizationResult(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                rendered_sections=tuple(capability.required_sections),
                snapshot=snapshot,
                traceability=traceability,
                assumptions=capability.assumptions,
            )
            status = "completed"
        except Exception as exc:  # noqa: BLE001 - failures must be contained.
            result = VisualizationResult(
                capability_id=capability.capability_id,
                capability_fingerprint=capability.fingerprint,
                rendered_sections=(),
                snapshot={},
                traceability=traceability,
                assumptions=capability.assumptions,
                message=str(exc),
            )
            status = "failed"

        return VisualizationReport(
            capability_id=capability.capability_id,
            capability_fingerprint=capability.fingerprint,
            status=status,
            result=result,
            rendered_sections=result.rendered_sections,
            traceability_count=len(result.traceability),
            assumption_count=len(result.assumptions),
            failure_message=result.message,
            run_fingerprint=self._build_run_fingerprint(result),
        )

    @staticmethod
    def _build_run_fingerprint(result: VisualizationResult) -> str:
        payload = {
            "capability_id": result.capability_id,
            "capability_fingerprint": result.capability_fingerprint,
            "rendered_sections": list(result.rendered_sections),
            "snapshot": result.snapshot,
            "traceability": [
                {
                    "reference_type": reference.reference_type,
                    "reference_id": reference.reference_id,
                    "fingerprint": reference.fingerprint,
                }
                for reference in result.traceability
            ],
            "assumptions": list(result.assumptions),
            "message": result.message,
        }
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
