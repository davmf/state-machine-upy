import asyncio

import events
import logger
from state_lib.event import Event, publish, subscribe_to
from state_lib.state import State


class S_A(State):

    def __init__(self):
        super().__init__(initial=S_Ai(), final=S_Af())
        self.state_A: State = S_AA()
        self.state_B: State = S_AB()
        self.log = logger.init_logging(type(self).__name__)
        subscribe_to({events.EV1, events.EV2}, self.event_queue)

    async def manage(self):
        self.log.debug("")

        if self.state and self.final:
            destination: State = self.history_state if self.history_state else self.state_A
            self.state = await self.state.transition_to(destination)

            try:
                while True:
                    event: Event = await self.event_queue.get()
                    self.log.debug(f"{event}")

                    if self.state == self.state_A:
                        if event == events.EV1:
                            self.state = await self.state.transition_to(self.state_B, self.action)
                    elif self.state == self.state_B:
                        if event == events.EV1:
                            self.state = await self.state.transition_to(self.final, self.action)
                        elif event == events.EV2:
                            self.state = await self.state.transition_to(self.state_A, self.action)

            except asyncio.CancelledError:
                pass


class S_B(State):

    def __init__(self):
        super().__init__(initial=S_Bi(), final=S_Bf(), history=True)
        self.state_A: State = S_BA()
        self.state_B: State = S_BB()
        subscribe_to({events.EV3, events.EV4}, self.event_queue)
        self.log = logger.init_logging(type(self).__name__)

    async def manage(self):
        self.log.debug("")

        if self.state and self.final:
            destination: State = self.history_state if self.history_state else self.state_A
            self.state = await self.state.transition_to(destination)

            try:
                while True:
                    event: Event = await self.event_queue.get()
                    self.log.debug(f"{event}")

                    if self.state == self.state_A:
                        if event == events.EV3:
                            self.state = await self.state.transition_to(self.state_B, self.action)
                        elif event == events.EV4:
                            self.state = await self.state.transition_to(self.final, self.action)
                    elif self.state == self.state_B:
                        if event == events.EV3:
                            self.state = await self.state.transition_to(self.final, self.action)

            except asyncio.CancelledError:
                pass


class SM_i(State):

    def __init__(self):
        super().__init__()


class S_Ai(State):

    def __init__(self):
        super().__init__()


class S_Bi(State):

    def __init__(self):
        super().__init__()


class S_Af(State):

    def __init__(self):
        super().__init__(is_final=True)

    def enter(self) -> None:
        super().enter()
        publish(events.EVAF)


class S_Bf(State):

    def __init__(self):
        super().__init__(is_final=True)

    def enter(self) -> None:
        super().enter()
        publish(events.EVBF)


class S_AA(State):
    pass


class S_AB(State):
    pass


class S_BA(State):
    pass


class S_BB(State):
    pass
