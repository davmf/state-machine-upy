import asyncio

import events
import logger
import states
from state_lib.event import Event, publish, subscribe_to
from state_lib.state import State


class StateMachine(State):

    def __init__(self) -> None:
        super().__init__()
        self.state_A: State = states.S_A()
        self.state_B: State = states.S_B()
        self.state: State = states.SM_i()
        self.log = logger.init_logging(type(self).__name__)

        subscribe_to(
            {events.EV0, events.EV1, events.EVAF5, events.EVBF6},
            self.event_queue
        )

    async def run(self) -> None:
        self.log.debug("")
        asyncio.create_task(self.manage())
        DELAY = 1

        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AA}

        publish(events.EV0)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_B, states.S_BA}

        publish(events.EV1)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AA}

        publish(events.EV1)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AB}

        publish(events.EV1)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_B, states.S_BA}

        publish(events.EV3)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_B, states.S_BB}

        publish(events.EV1)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AA}

        publish(events.EV0)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_B, states.S_BB}

        publish(events.EV3)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AA}

        publish(events.EV1)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AB}

        publish(events.EV0)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_B, states.S_BA}

        publish(events.EV1)
        await asyncio.sleep(DELAY)
        assert State.active_states() == {states.S_A, states.S_AA}

        print("Done!")

    async def manage(self):
        self.log.debug("")
        self.state = await self.state.transition_to(self.state_A, self.action)

        while True:
            event: Event = await self.event_queue.get()
            self.log.debug(f"{event}")

            if self.state == self.state_A:
                if (event == events.EV0 and self.guard()) or event == events.EVAF5:
                    self.state = await self.state.transition_to(self.state_B, self.action)
            elif self.state == self.state_B:
                if (event == events.EV1 and self.guard()) or event == events.EVBF6:
                    self.state = await self.state.transition_to(self.state_A, self.action)   


asyncio.run(StateMachine().run())
