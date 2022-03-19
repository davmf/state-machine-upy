import asyncio
from typing import *
from logger import LoggingHandler


class State(LoggingHandler):

    def __init__(self) -> None:
        super().__init__()

    def transition_to(self, new_state) -> None:
        self.exit()
        new_state.enter()
        new_state.do()

    def enter(self):
        self.log.info("")

    def exit(self):
        self.do_task.cancel()
        self.log.info("")

    def do(self):
        self.do_task = asyncio.create_task(self._do())

    async def _do(self):
        try:
            print("DO")

            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
