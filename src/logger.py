import logging

class LoggingHandler:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
