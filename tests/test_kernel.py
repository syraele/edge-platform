"""
EDGE_ENGINE

Kernel integration tests.
"""

from tests.helpers import create_test_context

from edge.events.event import Event
from edge.events.event_bus import EventBus
from edge.events.event_types import EventType


def test_kernel_context_creation():
    """
    Verify kernel context initialization.
    """

    ctx = create_test_context()

    assert ctx.config.symbol == "XAUUSD"

    assert ctx.market.connected is False

    assert ctx.runtime.started is False

    assert ctx.services is not None


def test_event_bus_registration():
    """
    Verify EventBus can be attached to services.
    """

    ctx = create_test_context()

    bus = EventBus()

    ctx.services.event_bus = bus

    assert ctx.services.event_bus is bus


def test_event_publication():

    received = []

    def handler(event):
        received.append(event)

    bus = EventBus()

    bus.subscribe(EventType.SIGNAL, handler)

    event = Event(
        name=EventType.SIGNAL,
        payload={
            "signal": "BUY",
        },
    )

    bus.publish(event)

    assert len(received) == 1

    assert received[0].payload["signal"] == "BUY"