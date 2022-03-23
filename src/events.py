import asyncio
from typing import *


class Events:

    EV1 = pow(2, 0)
    EV2 = pow(2, 1)
    EV3 = pow(2, 2)
    EV4 = pow(2, 3)
    EV5 = pow(2, 4)
    MainAFinal = pow(2, 5)
    MainBFinal = pow(2, 6)

    events: int = 0

    def set_(event: int) -> None:
        Events.events |= event
        print("SET EV", event)

    def is_set(event_mask: int) -> bool:
        """Also clears the event(s) if set.
        """        
        if Events.events & event_mask:
            Events.clear(event_mask)
            return True
        else:
            return False

    def clear(event_mask: int) -> None:
        Events.events &= ~event_mask

    def clear_all() -> None:
        Events.events = 0

    async def get(mask: int) -> None:
        while (Events.events & mask):
            await asyncio.sleep(0.1)
        while not (Events.events & mask):
            await asyncio.sleep(0.1)
