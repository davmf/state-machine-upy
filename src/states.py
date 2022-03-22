import asyncio
from typing import *

from events import Events

import logger
from state import State


class MainA(State):

    def __init__(self):
        super().__init__()
        self.initial = MainAInitial()
        self.final = MainAFinal()
        self.state_AA = MainAA()
        self.state_AB = MainAB()
        self.state = self.initial
        self.log = logger.init_logging(type(self).__name__)

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_AA)

        try:
            while True:
                await Events.get(Events.EV2 | Events.EV3)

                if self.state == self.state_AA:
                    if Events.is_set(Events.EV2):
                        self.state = await self.state.transition_to(self.state_AB)
                elif self.state == self.state_AB:
                    if Events.is_set(Events.EV2):
                        self.state = await self.state.transition_to(self.final)
                    elif Events.is_set(Events.EV3):
                        self.state = await self.state.transition_to(self.state_AA)

        except asyncio.CancelledError:
            pass


class MainB(State):

    def __init__(self):
        super().__init__()
        self.initial = MainBInitial()
        self.final = MainBFinal()
        self.state_BA= MainBA()
        self.state_BB = MainBB()
        self.state = self.initial
        self.log = logger.init_logging(type(self).__name__)

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_BA)

        try:
            while True:
                await Events.get(Events.EV4 | Events.EV5)

                if self.state == self.state_BA:
                    if Events.is_set(Events.EV4):
                        self.state = await self.state.transition_to(self.state_BB)
                    elif Events.is_set(Events.EV5):
                        Events.set_(Events.EV2)
                elif self.state == self.state_BB:
                    if Events.is_set(Events.EV4):
                        self.state = await self.state.transition_to(self.final)

        except asyncio.CancelledError:
            pass


class MainInitial(State):

    def __init__(self):
        super().__init__()


class MainAInitial(State):

    def __init__(self):
        super().__init__()


class MainBInitial(State):

    def __init__(self):
        super().__init__()


class MainAFinal(State):

    def __init__(self):
        super().__init__()
        self.is_final = True

    def enter(self) -> None:
        super().enter()
        Events.set_(Events.MainAFinal)


class MainBFinal(State):

    def __init__(self):
        super().__init__()
        self.is_final = True

    def enter(self) -> None:
        super().enter()
        Events.set_(Events.MainBFinal)

class MainAA(State):
    pass    


class MainAB(State):
    pass


class MainBA(State):
    pass    


class MainBB(State):
    pass
