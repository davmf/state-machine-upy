from typing import *
from state_machines import StateMachineA, StateMachineB
from events import Events
from state_machine import StateMachine
from state import State

import asyncio


class Main(StateMachine):

    def __init__(self) -> None:
        initial = State()
        state_machine_A = StateMachineA()
        state_machine_B = StateMachineB()
        self.state = initial

    async def run(self) -> None:
        do_task = asyncio.create_task(self._do())
        manage_task = asyncio.create_task(self._manage())
        await asyncio.gather(do_task, manage_task)

    async def _do(self) -> None:
        print("DO", self.name)
        await asyncio.sleep(4)
        Events.set_(Events.EV2)
        await asyncio.sleep(4)
        Events.set_(Events.EV2)
        await asyncio.sleep(4)
        Events.set_(Events.EV4)
        await asyncio.sleep(4)
        Events.set_(Events.EV4)

        while True:
            await asyncio.sleep(1)

    async def _manage(self):
        print("MANAGE", NAME)
        self.state.transition_to(self.state_machine_A)

        while True:
            await Events.get(Events.EV1 | Events.EV2)

            if self.state == self.state_machine_A:
                if Events.is_set(Events.EV1):
                    await self.state.transition_to(self.state_machine_B)
            elif self.state == self.state_machine_B:
                if Events.is_set(Events.EV2):
                    await self.state.transition_to(self.state_machine_A)
     

async def main():
    state_machine = StateMachine()
    asyncio.create_task(state_machine.run())

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
