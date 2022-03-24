import asyncio
from typing import Set
import logger


class Event(asyncio.Event):

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.log = logger.init_logging(type(self).__name__)
    
    def set(self) -> None:
        super().set()
        self.log.info(self.name)

    def __str__(self) -> str:
        return self.name



EV1 = Event("EV1")
EV2 = Event("EV2")
EV3 = Event("EV3")
EV4 = Event("EV4")
EV5 = Event("EV5")
EVAF = Event("EVAF")
EVBF = Event("EVBF")


events: Set[Event] = {EV1, EV2, EV3, EV4, EV5, EVAF, EVBF}


async def wait_for_any(*events: Event) -> Event:

    while True:
        for event in events:
            if event.is_set():
                _clear_all()
                return event

        await asyncio.sleep(0.01)


def _clear_all() -> None:

    for event in events:
        event.clear()
