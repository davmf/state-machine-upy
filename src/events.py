from typing import Set, Dict, cast
import logger
from asyncio import Queue

log = logger.init_logging("Event")


Event = int

class Events:
    EV0 = cast(Event, 0)
    EV1 = cast(Event, 1)
    EV2 = cast(Event, 2)
    EV3 = cast(Event, 3)
    EV4 = cast(Event, 4)
    EVAF5 = cast(Event, 5)
    EVBF6 = cast(Event, 6)
    LAST = EVBF6


_event_subscribers: Dict[Event, Set[Queue[Event]]] = dict()


def subscribe_to(events: Set[Event], event_queue: Queue[Event]) -> None:       
    for event in events:
        if event not in _event_subscribers:
            _event_subscribers[event] = set()
        _event_subscribers[event].add(event_queue)


def publish(event: Event) -> None:
    log.info(f"publish {event}")
    for event_queue in _event_subscribers[event]:
        event_queue.put_nowait(event)
