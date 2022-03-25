import asyncio
from typing import Any

import logger
from events import Events, subscribe_to, Event, publish
from state import State
from states import MainA, MainB, MainInitial


class Main(State):

    def __init__(self) -> None:
        super().__init__()
        self.state_A: State = MainA()
        self.state_B: State = MainB()
        self.state: State = MainInitial()
        events = {Events.EV1, Events.EV2, Events.EVAF, Events.EVBF}
        subscribe_to(events, self.event_queue)
        self.log = logger.init_logging(type(self).__name__)

    async def run(self) -> None:
        self.log.info("")
        asyncio.create_task(self.manage())
        DELAY = 1

        while True:
            await asyncio.sleep(DELAY)
            publish(Events.EV1)
            await asyncio.sleep(DELAY)
            publish(Events.EV2)
            await asyncio.sleep(DELAY)
            publish(Events.EV2)
            await asyncio.sleep(DELAY)
            publish(Events.EV2)
            await asyncio.sleep(DELAY)
            publish(Events.EV4)
            await asyncio.sleep(DELAY)
            publish(Events.EV4)

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_A)

        while True:
            event: Event = await self.event_queue.get()
            self.log.info(f"{event}")

            if self.state == self.state_A:
                if event in {Events.EV1, Events.EVAF}:
                    self.state = await self.state.transition_to(self.state_B)
            elif self.state == self.state_B:
                if event in {Events.EV2, Events.EVBF}:
                    self.state = await self.state.transition_to(self.state_A)   


def start(state_machine: Main) -> asyncio.Task[Any]:
    return asyncio.create_task(state_machine.run())


async def main():
    state_machine_task: asyncio.Task[Any] = start(Main())
    await state_machine_task


asyncio.run(main())
