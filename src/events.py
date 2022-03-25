from typing import Set, Dict, cast
import logger
from asyncio import Queue

log = logger.init_logging("Event")


Event = int

class Events:
    EV1 = cast(Event, 0)
    EV2 = cast(Event, 1)
    EV3 = cast(Event, 2)
    EV4 = cast(Event, 3)
    EV5 = cast(Event, 4)
    EVAF = cast(Event, 5)
    EVBF = cast(Event, 6)
    LAST = EVBF


_event_subscribers: Dict[Event, Set[Queue[Event]]] = dict()


def subscribe_to(events: Set[Event], event_queue: Queue[Event]) -> None:       
    for event in events:
        if event not in _event_subscribers:
            _event_subscribers[event] = set()
        _event_subscribers[event].add(event_queue)


def publish(event: Event) -> None:
    log.info("publish", event)
    for event_queue in _event_subscribers[event]:
        event_queue.put_nowait(event)
