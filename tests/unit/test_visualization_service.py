from edge.visualization import (
    VisualizationCapability,
    VisualizationDataReference,
    VisualizationService,
)


class StubRenderer:
    def __init__(self, output, should_raise: bool = False) -> None:
        self._output = output
        self._should_raise = should_raise

    def render(self, capability, payload, traceability):
        if self._should_raise:
            raise RuntimeError("renderer unavailable")
        return self._output


def test_visualization_service_returns_traceable_completed_report():
    capability = VisualizationCapability(
        capability_id="viz-session-overview",
        capability_name="Session Overview",
        required_sections=("summary", "evidence"),
        assumptions=("Evidence ordering remains stable.",),
    )
    service = VisualizationService(
        StubRenderer(output={"cards": [{"title": "Summary"}]})
    )

    report = service.render(
        capability=capability,
        payload={"summary": {"status": "completed"}, "evidence": {"count": 3}},
        traceability=(
            VisualizationDataReference(
                reference_type="pipeline_report",
                reference_id="session-1",
                fingerprint="run-1",
            ),
        ),
    )

    assert report.status == "completed"
    assert report.result.succeeded is True
    assert report.rendered_sections == ("summary", "evidence")
    assert report.traceability_count == 1
    assert report.assumption_count == 1
    assert report.failure_message is None
    assert report.result.snapshot == {"cards": [{"title": "Summary"}]}
    assert report.run_fingerprint


def test_visualization_service_fails_when_payload_sections_are_missing():
    capability = VisualizationCapability(
        capability_id="viz-session-overview",
        capability_name="Session Overview",
        required_sections=("summary", "evidence"),
    )
    service = VisualizationService(StubRenderer(output={"cards": []}))

    report = service.render(
        capability=capability,
        payload={"summary": {"status": "completed"}},
    )

    assert report.status == "failed"
    assert report.result.succeeded is False
    assert report.failure_message == "Missing payload sections: ['evidence']"
    assert report.rendered_sections == ()


def test_visualization_service_contains_renderer_failure():
    capability = VisualizationCapability(
        capability_id="viz-session-overview",
        capability_name="Session Overview",
        required_sections=("summary",),
    )
    service = VisualizationService(
        StubRenderer(output={}, should_raise=True)
    )

    report = service.render(
        capability=capability,
        payload={"summary": {"status": "completed"}},
    )

    assert report.status == "failed"
    assert report.failure_message == "renderer unavailable"
    assert report.result.message == "renderer unavailable"


def test_visualization_capability_fingerprint_is_deterministic():
    left = VisualizationCapability(
        capability_id="viz-session-overview",
        capability_name="Session Overview",
        required_sections=("summary", "evidence"),
        assumptions=("Evidence ordering remains stable.",),
    )
    right = VisualizationCapability(
        capability_id="viz-session-overview",
        capability_name="Session Overview",
        required_sections=("summary", "evidence"),
        assumptions=("Evidence ordering remains stable.",),
    )

    assert left.fingerprint == right.fingerprint
