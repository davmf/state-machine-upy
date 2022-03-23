import asyncio
from typing import *

import logger
from events import Events


class State:

    def __init__(self) -> None:
        self.initial = None
        self.state = None
        self.do_task = None
        self.manage_task = None
        self.is_final = False
        self.log = logger.init_logging(type(self).__name__)

    async def transition_to(self, new_state) -> "State":
        if self.state:
            await self.state.exit()

        await self.exit()
        new_state.enter()
        
        if not new_state.is_final:
            new_state.do()
        return new_state

    def enter(self):
        self.log.info("")

    def _exit(self):
        if self.initial:
            self.state = self.initial

        Events.clear_all()

    async def exit(self):
        self.log.info("")

        if self.do_task:
            self.do_task.cancel()
            await self.do_task

        self._exit()

    def do(self):
        self.log.info("")
        self.do_task = asyncio.create_task(self._do())

    async def _do(self):
        self.manage_task = asyncio.create_task(self.manage())

        try:
            await self.manage_task
        except asyncio.CancelledError:
            self.manage_task.cancel()
            await self.manage_task

    async def manage(self):
        self.log.info("")

        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
