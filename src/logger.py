import logging

def init_logging(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    if (log.hasHandlers()):
        log.handlers.clear()

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log
