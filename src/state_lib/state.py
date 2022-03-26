import asyncio
from state_lib.event import Event
from typing import Callable, Optional, Set, Type, Any

import logger


class State:

    # for tracking active states
    _active_states: Set["State"] = set()

    def __init__(
        self,
        history: bool = False,
        initial: Optional["State"] = None,
        final: Optional["State"] = None,
        is_final: bool = False
    ) -> None:
        self.history = history
        self.initial = initial
        self.final = final
        self.is_final = is_final
        self.state: Optional["State"] = initial if initial else None
        self.do_task = None
        self.manage_task = None
        self.history_state: Optional["State"] = None
        self.event_queue: asyncio.Queue[Event] = asyncio.Queue()
        self.log = logger.init_logging(type(self).__name__)

    async def transition_to(
        self,
        new_state: "State",
        action: Optional[Callable[..., Any]] = None
    ) -> "State":        

        if self.state:            
            self.history_state = (
                self.state if self.history and not self.state.is_final else None
            )
            await self.state.exit()

        await self.exit()

        if action:
            action()

        new_state.enter()
        
        if not new_state.is_final:
            new_state.do()

        return new_state

    def enter(self) -> None:
        self.log.debug("")
        State._active_states.add(self)
        self._clear_event_queue()

    def _exit(self) -> None:
        if self.initial:
            self.state = self.initial

    async def exit(self) -> None:
        self.log.debug("")

        if self.do_task:
            self.do_task.cancel()

            try:
                await self.do_task
            except asyncio.CancelledError:
                pass

        self._exit()

        if self in State._active_states:
            State._active_states.remove(self)

    #default guard
    def guard(self) -> bool:
        return True

    #default action
    def action(self) -> None:
        pass

    def do(self) -> None:
        self.log.debug("")
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
        self.log.debug("")

        try:
            while True:
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            raise

    def _clear_event_queue(self) -> None:
        while not self.event_queue.empty():
            _ = self.event_queue.get_nowait()

    @staticmethod
    def active_states() -> Set[Type["State"]]:
        return {type(state) for state in State._active_states}
