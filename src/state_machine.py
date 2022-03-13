from typing import *

import asyncio

async def tick():
    await asyncio.sleep(1)  # Pause 1s


def put_event(name: str, n: int):
    queue.put_nowait(n)
    print("EVENT PUT", name, n)


def reuse_event(n):
    queue.put_nowait(n)
#    print("Reuse EVENT", n)


async def get_event(name: str) -> int:    
    event: int = await queue.get()
    print("EVENT GET", name, event)
    return event


events = [False, False, False, False, False]

class State:

    def __init__(self, name, events):
        self.name = name
        self.task = asyncio.create_task(name()) if name is not None else None

    async def transition_to(self, new_state: Awaitable) -> None:
        if self.name is None:
            print("TRANSITION", "initial" , new_state.__name__)
        else:
            print("TRANSITION", self.name.__name__ , new_state.__name__)
            self.task.cancel()
            await self.task

        self.name = new_state
        self.task = asyncio.create_task(new_state())


def initial() -> State:
    return State(None)


async def state_machine() -> None:

    NAME = "SM"

    async def do() -> None:
        while True:
            print("DO", NAME)
            await tick()
            put_event(NAME, 2)

    async def manage():
        state = initial()
        await state.transition_to(state_machine_A)

        while True:
            event = await get_event(NAME)

            if state.name == state_machine_A:
                if event == 1:
                    await state.transition_to(state_machine_B)
                else:
                    reuse_event(event)
            elif state.name == state_machine_B:
                if event == 2:
                    await state.transition_to(state_machine_A)
                else:
                    reuse_event(event)

            await tick()


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
                    put_event(NAME, 1)
                    await tick()

            except asyncio.CancelledError:
                pass

        async def manage():
            state = initial()
            await state.transition_to(state_AA)

            try:
                while True:
                    event = await get_event(NAME)

                    if state == state_AA:
                        if event == 2:
                            await state.transition_to(state_AB)
                        else:
                            reuse_event(event)
                    elif state == state_AB:
                        if event == 2:
                            put_event(1)
                        elif event == 3:
                            await state.transition_to(state_AA)
                        else:
                            reuse_event(event)

                    await tick()

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
                        await tick()
                        put_event(3)
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
                    await tick()
                    put_event(NAME, 4)

            except asyncio.CancelledError:
                pass

        async def manage() -> int:
            state = initial()
            await state.transition_to(state_BA)

            try:
                while True:
                    event = await get_event(NAME)

                    if state == state_BA:
                        if event == 4:
                            await state.transition_to(state_BB)
                        elif event == 5:
                            put_event(NAME, 2)
                        else:
                            reuse_event(event)
                    elif state == state_BB:
                        if event == 4:
                            put_event(NAME, 2)
                        else:
                            reuse_event(event)

                    await tick()

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
                        print(NAME)
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

        async def state_BB():

            NAME = "BB"
            
            def entry():
                print("ENTRY", NAME)

            def exit_():
                print("EXIT", NAME)

            async def do():
                try:
                    while True:
                        print("DO", NAME)
                        await tick()
                        put_event(NAME, 3)

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
