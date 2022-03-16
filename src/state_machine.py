import asyncio
from typing import *
from state import State


class StateMachine(State):

    def __init__(self, name = None) -> None:
        self.name = name
        self.task = asyncio.create_task(name()) if name is not None else None        

    async def run(self):
        self.enter()
        do_task = asyncio.create_task(self.do())
        manage_task = asyncio.create_task(self.manage())

        try:
            await asyncio.gather(do_task, manage_task)

        except asyncio.CancelledError:
            do_task.cancel()
            manage_task.cancel()

        self.exit_()
