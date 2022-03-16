import asyncio
from typing import *


class Events:

    EV1 = pow(2, 0)
    EV2 = pow(2, 1)
    EV3 = pow(2, 2)
    EV4 = pow(2, 3)
    EV5 = pow(2, 4)

    events: int = 0

    def set_(event: int) -> None:
        Events.events |= event
        print("SET EV", event)

    def is_set(event: int) -> bool:
        """Also clears the event if it is set.
        """        
        if Events.events & event:
            Events.clear(event)
            return True
        else:
            return False

    def clear(event: int) -> None:
        Events.events &= ~event

    def clear_all() -> None:
        Events.events = 0

    async def get(mask: int) -> None:
        while not (Events.events & mask):
            await asyncio.sleep(1)
