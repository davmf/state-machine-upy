from typing import *

import asyncio

async def tick():
    await asyncio.sleep(0.1)  # Pause 1s


class Events:

    EV1 = pow(2, 0)
    EV2 = pow(2, 1)
    EV3 = pow(2, 2)
    EV4 = pow(2, 3)
    EV5 = pow(2, 4)

    events: int = 0

    def set_(event: int) -> None:
        Events.events |= event
        print("SET EV", event)

    def is_set(event: int) -> bool:
        """Also clears the event if it is set.
        """        
        if Events.events & event:
            Events.clear(event)
            return True
        else:
            return False

    def clear(event: int) -> None:
        Events.events &= ~event

    def clear_all() -> None:
        Events.events = 0

    async def get(mask: int) -> None:
        while not (Events.events & mask):
            await tick()


class State:

    def __init__(self, name = None) -> None:
        self.name = name
        self.task = asyncio.create_task(name()) if name is not None else None

    async def transition_to(self, new_state: Awaitable) -> None:
        if self.name is None:
            print("TRANSITION", "initial" , new_state.__name__)
        else:
            print("TRANSITION", self.name.__name__ , new_state.__name__)
            self.task.cancel()
            await self.task

        self.name = new_state.__name__
        self.task = asyncio.create_task(new_state())


async def state_machine() -> None:

    NAME = "SM"

    async def do() -> None:
        print("DO", NAME)
        await asyncio.sleep(5)
        Events.set_(Events.EV2)

        while True:
            await asyncio.sleep(1)


    async def manage():
        state = State()
        await state.transition_to(state_machine_A)

        while True:
            await Events.get(Events.EV1 | Events.EV2)

            if state.name == state_machine_A:
                if Events.is_set(Events.EV1):
                    await state.transition_to(state_machine_B)
            elif state.name == state_machine_B:
                if Events.is_set(Events.EV2):
                    await state.transition_to(state_machine_A)

    async def state_machine_A():

        NAME = "A"

        def entry():
            print("ENTRY", NAME)

        def exit_():
            print("EXIT", NAME)

        async def do():
            try:
                while True:                
                    print("DO", NAME)
                    Events.set_(Events.EV1)
                    await tick()

            except asyncio.CancelledError:
                pass

        async def manage():
            state = State()
            await state.transition_to(state_AA)

            try:
                while True:
                    await Events.get(Events.EV2 | Events.EV3)

                    if state == state_AA:
                        if Events.is_set(Events.EV2):
                            await state.transition_to(state_AB)
                    elif state == state_AB:
                        if Events.is_set(Events.EV2):
                            Events.set_(Events.EV1)
                        elif Events.is_set(Events.EV3):
                            await state.transition_to(state_AA)

            except asyncio.CancelledError:
                state.task.cancel()
                await state.task

        async def state_AA():

            NAME = "AA"

            def entry():
                print("ENTRY", NAME)

            def exit_():
                print("EXIT", NAME)

            async def do():
                try:
                    while True:
                        print("DO", NAME)
                        await asyncio.sleep(1)
                except asyncio.CancelledError:
                    pass

            entry()
            do_task = asyncio.create_task(do())

            try:
                await do_task

            except asyncio.CancelledError:
                do_task.cancel()

            exit_()

        async def state_AB():

            NAME = "AB"
            
            def entry():
                print("ENTRY", NAME)

            def exit_():
                print("EXIT", NAME)

            async def do():
                try:
                    while True:
                        print("DO", NAME)
                        Events.set_(Events.EV3)
                        await tick()
                except asyncio.CancelledError:
                    pass

            entry()
            do_task = asyncio.create_task(do())

            try:
                await do_task

            except asyncio.CancelledError:
                do_task.cancel()

            exit_()

        entry()
        do_task = asyncio.create_task(do())
        manage_task = asyncio.create_task(manage())

        try:
            await asyncio.gather(do_task, manage_task)

        except asyncio.CancelledError:
            do_task.cancel()
            manage_task.cancel()

        exit_()

    async def state_machine_B():

        NAME = "B"
        
        def entry():
            print("ENTRY", NAME)

        def exit_():
            print("EXIT", NAME)

        async def do():
            try:
                while True:                
                    print("DO", NAME)
                    Events.set_(Events.EV4)
                    await tick()

            except asyncio.CancelledError:
                pass

        async def manage() -> int:
            state = State()
            await state.transition_to(state_BA)

            try:
                while True:
                    await Events.get(Events.EV4 | Events.EV5)

                    if state == state_BA:
                        if Events.is_set(Events.EV4):
                            await state.transition_to(state_BB)
                        elif Events.is_set(Events.EV5):
                            Events.set_(Events.EV2)

                    elif state == state_BB:
                        if Events.is_set(Events.EV4):
                            Events.set_(Events.EV2)

            except asyncio.CancelledError:
                state.task.cancel()
                await state.task

        async def state_BA():

            NAME = "BA"
            
            def entry():
                print("ENTRY", NAME)

            def exit_():
                print("EXIT", NAME)

            async def do():
                try:
                    while True:
                        await asyncio.sleep(5)

                except asyncio.CancelledError:
                    pass

            entry()
            do_task = asyncio.create_task(do())

            try:
                await do_task

            except asyncio.CancelledError:
                do_task.cancel()

            exit_()

        async def state_BB():

            NAME = "BB"
            
            def entry():
                print("ENTRY", NAME)

            def exit_():
                print("EXIT", NAME)

            async def do():
                try:
                    while True:
                        Events.set_(Events.EV4)
                        await asyncio.sleep(5)

                except asyncio.CancelledError:
                    pass

            entry()
            do_task = asyncio.create_task(do())

            try:
                await do_task

            except asyncio.CancelledError:
                do_task.cancel()

            exit_()

        entry()
        do_task = asyncio.create_task(do())
        manage_task = asyncio.create_task(manage())

        try:
            await asyncio.gather(do_task, manage_task)

        except asyncio.CancelledError:
            do_task.cancel()
            manage_task.cancel()

        exit_()

    do_task = asyncio.create_task(do())
    manage_task = asyncio.create_task(manage())
    await asyncio.gather(do_task, manage_task)
     

async def main():
    asyncio.create_task(state_machine())

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
