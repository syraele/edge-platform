from datetime import datetime

from edge.events.event import Event
from edge.events.event_bus import EventBus
from edge.events.event_types import EventType


def on_signal(event):
    print("EVENTO RICEVUTO")
    print(event.name)
    print(event.payload)


bus = EventBus()

bus.subscribe(EventType.SIGNAL, on_signal)

event = Event(
    name=EventType.SIGNAL,
    timestamp=datetime.now(),
    payload={
        "symbol": "XAUUSD",
        "direction": "BUY",
        "price": 3350.20,
    },
)

bus.publish(event)