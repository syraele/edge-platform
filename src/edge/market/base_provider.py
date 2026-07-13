from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def connect(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def tick(self):
        ...