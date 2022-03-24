import asyncio

from events import EV2, EV3, EV4, EV5, EVAF, EVBF, wait_for_any, Event
import logger
from state import State


class MainA(State):

    def __init__(self):
        super().__init__()
        self.initial: State = MainAInitial()
        self.final: State = MainAFinal()
        self.state_AA: State = MainAA()
        self.state_AB: State = MainAB()
        self.state: State = self.initial
        self.log = logger.init_logging(type(self).__name__)

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_AA)

        try:
            while True:
                event: Event = await wait_for_any(EV2, EV3)
                self.log.info(f"{event}")

                if self.state == self.state_AA:
                    if event == EV2:
                        self.state = await self.state.transition_to(self.state_AB)
                elif self.state == self.state_AB:
                    if event == EV2:
                        self.state = await self.state.transition_to(self.final)
                    elif event == EV3:
                        self.state = await self.state.transition_to(self.state_AA)

        except asyncio.CancelledError:
            pass


class MainB(State):

    def __init__(self):
        super().__init__()
        self.initial: State = MainBInitial()
        self.final: State = MainBFinal()
        self.state_BA: State = MainBA()
        self.state_BB: State = MainBB()
        self.state: State = self.initial
        self.log = logger.init_logging(type(self).__name__)

    async def manage(self):
        self.log.info("")
        self.state = await self.state.transition_to(self.state_BA)

        try:
            while True:
                event: Event = await wait_for_any(EV4, EV5)
                self.log.info(f"{event}")

                if self.state == self.state_BA:
                    if event == EV4:
                        self.state = await self.state.transition_to(self.state_BB)
                    elif event == EV5:
                        self.state = await self.state.transition_to(self.final)
                elif self.state == self.state_BB:
                    if event == EV4:
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
        EVAF.set()


class MainBFinal(State):

    def __init__(self):
        super().__init__()
        self.is_final = True

    def enter(self) -> None:
        super().enter()
        EVBF.set()


class MainAA(State):
    pass


class MainAB(State):
    pass


class MainBA(State):
    pass


class MainBB(State):
    pass
