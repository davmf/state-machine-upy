from typing import *

import asyncio
import state_BA
import state_BB
from events import Events
from state import State


NAME = "B"

def entry():
    print("ENTRY", NAME)

def exit_():
    print("EXIT", NAME)

async def do():
    try:
        while True:                
            print("DO", NAME)
#                    Events.set_(Events.EV4)
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass

async def manage() -> int:
    state = State()
    state = await state.transition_to(state_BA)

    try:
        while True:
            await Events.get(Events.EV4 | Events.EV5)

            if state == state_BA:
                if Events.is_set(Events.EV4):
                    state = await state.transition_to(state_BB)
                elif Events.is_set(Events.EV5):
                    Events.set_(Events.EV2)

            elif state == state_BB:
                if Events.is_set(Events.EV4):
                    Events.set_(Events.EV2)

    except asyncio.CancelledError:
        state.task.cancel()
        await state.task


async def state():

    entry()
    do_task = asyncio.create_task(do())
    manage_task = asyncio.create_task(manage())

    try:
        await asyncio.gather(do_task, manage_task)

    except asyncio.CancelledError:
        do_task.cancel()
        manage_task.cancel()

    exit_()
