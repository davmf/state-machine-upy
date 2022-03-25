import asyncio
from events import Event, Events, subscribe_to, publish
from typing import Optional, Set

import logger


class State:

    def __init__(self) -> None:
        self.initial = None
        self.state: Optional["State"] = None
        self.do_task = None
        self.manage_task = None
        self.is_final = False
        self.event_queue: asyncio.Queue[Event] = asyncio.Queue()
        self.log = logger.init_logging(type(self).__name__)

    async def transition_to(self, new_state: "State") -> "State":
        if self.state:
            await self.state.exit()

        await self.exit()
        new_state.enter()
        
        if not new_state.is_final:
            new_state.do()
        return new_state

    def enter(self) -> None:
        self.log.info("")
        self._clear_event_queue()

    def _exit(self) -> None:
        if self.initial:
            self.state = self.initial

    async def exit(self) -> None:
        self.log.info("")

        if self.do_task:
            self.do_task.cancel()

            try:
                await self.do_task
            except asyncio.CancelledError:
                pass

        self._exit()

    def do(self) -> None:
        self.log.info("")
        self.do_task = asyncio.create_task(self._do())

    async def _do(self) -> None:
        self.manage_task = asyncio.create_task(self.manage())

        try:
            await self.manage_task
        except asyncio.CancelledError:
            self.manage_task.cancel()

            try:
                await self.manage_task
            except asyncio.CancelledError:
                raise

    async def manage(self) -> None:
        self.log.info("")

        try:
            while True:
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            raise

    def _clear_event_queue(self) -> None:
        while not self.event_queue.empty():
            _ = self.event_queue.get_nowait()
