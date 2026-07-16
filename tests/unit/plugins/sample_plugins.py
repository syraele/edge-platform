from edge.plugins import EdgePlugin


class LifecycleProbePlugin(EdgePlugin):
    plugin_id = "lifecycle-probe"

    activated = 0
    deactivated = 0

    @classmethod
    def reset(cls) -> None:
        cls.activated = 0
        cls.deactivated = 0

    def activate(self, context=None) -> None:
        type(self).activated += 1

    def deactivate(self, context=None) -> None:
        type(self).deactivated += 1


class NotAPlugin:
    pass
