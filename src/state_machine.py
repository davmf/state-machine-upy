import asyncio
from typing import *
from state import State


class StateMachine(State):

    async def run(self, enter, do, manage, exit_):
        enter()
        do_task = asyncio.create_task(do())
        manage_task = asyncio.create_task(manage())

        try:
            await asyncio.gather(do_task, manage_task)

        except asyncio.CancelledError:
            do_task.cancel()
            manage_task.cancel()

        exit_()
