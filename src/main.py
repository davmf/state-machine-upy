import asyncio
from typing import *
from events import Events
from state import State
from states import MainInitial, MainA, MainB


class Main(State):

    def __init__(self) -> None:
        super().__init__()
        self.state_A = MainA()
        self.state_B = MainB()
        self.state = MainInitial()

    async def do(self) -> None:
        self.log.info("")
        asyncio.create_task(self.manage())

        while True:
            await asyncio.sleep(2)
            Events.set_(Events.EV2)
            await asyncio.sleep(2)
            Events.set_(Events.EV1)

        while True:
            await asyncio.sleep(1)

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_A)

        while True:
            await Events.get(Events.EV1 | Events.EV2)

            if self.state == self.state_A:
                if Events.is_set(Events.EV1):
                    self.state = await self.state.transition_to(self.state_B)
            elif self.state == self.state_B:
                if Events.is_set(Events.EV2):
                    self.state = await self.state.transition_to(self.state_A)   


def start(state_machine) -> asyncio.Task:
    return asyncio.create_task(state_machine.do())


async def main():
    state_machine_task = start(Main())
    await state_machine_task


asyncio.run(main())