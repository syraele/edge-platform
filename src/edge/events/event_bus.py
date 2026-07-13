from collections import defaultdict

class EventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):

        self._subscribers[event_name].append(callback)

    def publish(self, event):

        callbacks = self._subscribers.get(event.name, [])

        for callback in callbacks:

            callback(event)