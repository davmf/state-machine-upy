from typing import Set, Dict
import logger
from asyncio import Queue

log = logger.init_logging("Event")


Event = int

_event_subscribers: Dict[Event, Set[Queue[Event]]] = dict()


def subscribe_to(events: Set[Event], event_queue: Queue[Event]) -> None:       
    for event in events:
        if event not in _event_subscribers:
            _event_subscribers[event] = set()
        _event_subscribers[event].add(event_queue)


def publish(event: Event) -> None:
    log.debug(f"publish {event}")
    for event_queue in _event_subscribers[event]:
        event_queue.put_nowait(event)
