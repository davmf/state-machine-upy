import asyncio

from events import Events
from state_machine import StateMachine
from state import State
from states import StateAA, StateAB, StateBA, StateBB



class StateMachineA(StateMachine):

    def __init__(self):
        self.state_AA = StateAA()
        self.state_AB = StateAB()
        self.state = State()

    async def manage(self):
        super().manage()
        self.initial.transition_to(self.state_AA)

        try:
            while True:
                await Events.get(Events.EV2 | Events.EV3)

                if self.state == self.state_AA:
                    if Events.is_set(Events.EV2):
                        self.state.transition_to(self.state_AB)
                elif self.state == self.state_AB:
                    if Events.is_set(Events.EV2):
                        Events.set_(Events.EV1)
                    elif Events.is_set(Events.EV3):
                        self.state.transition_to(self.state_AA)

        except asyncio.CancelledError:
            pass


class StateMachineB(StateMachine):

    def __init__(self):
        self.state_BA= StateBA()
        self.state_BB = StateBB()
        self.state = State()

    async def manage(self):
        super().manage()
        self.state.transition_to(self.state_AA)

        try:
            while True:
                await Events.get(Events.EV2 | Events.EV3)

                if self.state == self.state_AA:
                    if Events.is_set(Events.EV2):
                        self.state.transition_to(self.state_AB)
                elif self.state == self.state_AB:
                    if Events.is_set(Events.EV2):
                        Events.set_(Events.EV1)
                    elif Events.is_set(Events.EV3):
                        self.state.transition_to(self.state_AA)

        except asyncio.CancelledError:
            pass

