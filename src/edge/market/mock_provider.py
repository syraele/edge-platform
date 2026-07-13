from .base_provider import BaseProvider


class MockProvider(BaseProvider):

    def connect(self):

        return True

    def disconnect(self):

        pass

    def tick(self):

        return None