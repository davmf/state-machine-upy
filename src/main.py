import asyncio
from typing import *
from events import Events
from state import State
from state_machine import StateMachine
from state_machines import StateMachineA, StateMachineB


class Main(State):

    def __init__(self) -> None:
        super().__init__()
        self.state_machine_A = StateMachineA()
        self.state_machine_B = StateMachineB()
        self.state = State()

    def enter(self):
        pass

    async def do(self) -> None:
        self.log.info("")
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

    async def manage(self):
        self.log.info("")
        self.state.transition_to(self.state_machine_A)

        while True:
            await Events.get(Events.EV1 | Events.EV2)

            if self.state == self.state_machine_A:
                if Events.is_set(Events.EV1):
                    await self.state.transition_to(self.state_machine_B)
            elif self.state == self.state_machine_B:
                if Events.is_set(Events.EV2):
                    await self.state.transition_to(self.state_machine_A)
    
    def exit(self):
        pass


async def main():
    state_machine = Main()
    asyncio.create_task(state_machine.run())

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
