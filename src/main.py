import asyncio
from typing import Any

import logger
from events import EV1, EV2, EV4, Event, EVAF, EVBF, wait_for_any
from state import State
from states import MainA, MainB, MainInitial


class Main(State):

    def __init__(self) -> None:
        super().__init__()
        self.state_A: State = MainA()
        self.state_B: State = MainB()
        self.state: State = MainInitial()
        self.log = logger.init_logging(type(self).__name__)

    async def run(self) -> None:
        self.log.info("")
        asyncio.create_task(self.manage())
        DELAY = 1

        while True:
            await asyncio.sleep(DELAY)
            EV1.set()
            await asyncio.sleep(DELAY)
            EV2.set()
            await asyncio.sleep(DELAY)
            EV2.set()
            await asyncio.sleep(DELAY)
            EV2.set()
            await asyncio.sleep(DELAY)
            EV4.set()
            await asyncio.sleep(DELAY)
            EV4.set()

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_A)

        while True:
            event: Event = await wait_for_any(EV1, EV2, EVAF, EVBF)
            self.log.info(f"{event}")

            if self.state == self.state_A:
                if event in {EV1, EVAF}:
                    self.state = await self.state.transition_to(self.state_B)
            elif self.state == self.state_B:
                if event in {EV2, EVBF}:
                    self.state = await self.state.transition_to(self.state_A)   


def start(state_machine: Main) -> asyncio.Task[Any]:
    return asyncio.create_task(state_machine.run())


async def main():
    state_machine_task: asyncio.Task[Any] = start(Main())
    await state_machine_task


asyncio.run(main())
