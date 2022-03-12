import asyncio

async def tick():
    await asyncio.sleep(1)  # Pause 1s


queue = asyncio.Queue()


def put_event(n):
    queue.put_nowait(n)
    print("Put EVENT", n)


async def get_event() -> int:    
    event: int = await queue.get()
    print("Get EVENT", event)
    return event


async def transition_to(new_state, current_state_task = None):
    if current_state_task is not None:
        current_state_task.cancel()
        await current_state_task

    state = new_state
    return state, asyncio.create_task(state())


async def state_machine():

    name = "state_machine"

    async def do():
        while True:
            print("state_machine do")
            await tick()
            put_event(2)

    async def manage():
        state, state_task = await transition_to(state_machine_A)

        while True:
            event = await get_event()
            print(name, "gets event", event)

            if state == state_machine_A:
                if event == 1:
                    print("A -> B")
                    state, state_task = await transition_to(state_machine_B, state_task)
                else:
                    put_event(event)
            elif state == state_machine_B:
                if event == 2:
                    print("B -> A")
                    state, state_task = await transition_to(state_machine_A, state_task)
                else:
                    put_event(event)

            await tick()


    async def state_machine_A():

        name = "state_machine_A"

        def entry():
            print(name, "entry")

        def exit_():
            print(name, "exit")

        async def do():
            try:
                while True:                
                    print(name, "do")
                    put_event(1)
                    await tick()

            except asyncio.CancelledError:
                pass

        async def manage() -> int:
            state, state_task = await transition_to(state_AA)

            try:
                while True:
                    event = await get_event()
                    print(name, "gets event", event)

                    if state == state_AA:
                        if event == 2:
                            print("AA -> AB")
                            state, state_task = await transition_to(state_AB, state_task)
                        else:
                            put_event(event)
                    elif state == state_AB:
                        if event == 2:
                            put_event(1)
                        elif event == 3:
                            print("AB -> AA")
                            state, state_task = await transition_to(state_AA, state_task)
                        else:
                            put_event(event)

                    await tick()

            except asyncio.CancelledError:
                state_task.cancel()
                await state_task

        async def state_AA():

            def entry():
                print("state_AA entry")

            def exit_():
                print("state_AA exit")

            async def do():
                try:
                    while True:
                        print("state_AA do")
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

            cancel = False
            
            def entry():
                print("state_AB entry")

            def exit_():
                print("state_AB exit")

            async def do():
                try:
                    while True:
                        print("state_AB do")
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
            print("Cancel", name)
            do_task.cancel()
            manage_task.cancel()

        exit_()

    async def state_machine_B():

        name = "state_machine_B"

        def entry():
            print("state_machine_B entry")

        def exit_():
            print("state_machine_B exit")

        async def do():
            try:
                while True:                
                    print("state_machine_B do")
                    await tick()
                    put_event(4)
            finally:
                pass

        async def manage() -> int:
            state, state_task = await transition_to(state_BA)

            while True:
                event = await get_event()
                print(name, "gets event", event)

                if state == state_BA:
                    if event == 4:
                        state, state_task = await transition_to(state_BB, state_task)
                    elif event == 5:
                        put_event(2)
                    else:
                        put_event(event)
                elif state == state_BB:
                    if event == 4:
                        put_event(2)
                    else:
                        put_event(event)

                await tick()

        async def state_BA():

            def entry():
                print("state_BA entry")

            def exit_():
                print("state_BA exit")

            async def do():
                try:
                    while True:
                        print("state_BA do")
                        await tick()
                finally:
                    pass

            entry()
            do_task = asyncio.create_task(do())

            try:
                await do_task

            except asyncio.CancelledError:
                do_task.cancel()

            exit_()

        async def state_AB():

            def entry():
                print("state_BB entry")

            def exit_():
                print("state_BB exit")

            async def do():
                try:
                    while True:
                        print("state_BB do")
                        await tick()
                        put_event(3)
                finally:
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
