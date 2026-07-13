import logging

from .state import LifecycleState


class LifecycleManager:

    def __init__(self):
        self.state = LifecycleState.CREATED
        self.components = []

        self.logger = logging.getLogger(
            "EDGE.LIFECYCLE"
        )


    def register(self, component):
        self.components.append(component)


    def initialize(self):

        self.logger.info(
            "Lifecycle initialization started"
        )

        self.state = LifecycleState.INITIALIZING


        try:

            for component in self.components:

                if hasattr(component, "initialize"):
                    component.initialize()


            self.state = LifecycleState.READY

            self.logger.info(
                "System ready"
            )


        except Exception as e:

            self.state = LifecycleState.FAILED

            self.logger.exception(
                e
            )

            raise



    def start(self):

        if self.state != LifecycleState.READY:
            raise RuntimeError(
                "System not ready"
            )


        self.logger.info(
            "Starting EDGE_ENGINE"
        )


        for component in self.components:

            if hasattr(component, "start"):
                component.start()


        self.state = LifecycleState.RUNNING


        self.logger.info(
            "EDGE_ENGINE RUNNING"
        )



    def stop(self):

        self.logger.info(
            "Stopping EDGE_ENGINE"
        )


        self.state = LifecycleState.STOPPING


        for component in reversed(self.components):

            if hasattr(component, "stop"):
                component.stop()


        self.state = LifecycleState.STOPPED


        self.logger.info(
            "EDGE_ENGINE stopped"
        )