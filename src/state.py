import asyncio
from modulefinder import Module
from typing import *


class State:

    def __init__(self, name = None) -> None:
        self.label = ""
        self.name = name
        self.task = asyncio.create_task(name()) if name is not None else None        

    async def transition_to(self, new_state) -> "State":
        self.exit()
        new_state.enter()
        new_state.do()

    def enter(self):
        print("ENTRY", self.__name__)

    def exit(self):
        self.do_task.cancel()
        print("EXIT", self.__name__)

    def do(self):
        self.do_task = asyncio.create_task(self._do())

    async def _do(self):
        try:
            print("DO", self.__name__)

            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
