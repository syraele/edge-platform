from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Tick:

    bid: float

    ask: float

    last: float

    time: datetime