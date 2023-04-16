import sys
import logging


class Logger:
    __slots__ = ['__root']

    def __init__(self) -> None:
        self.__root = logging.getLogger()
        self.__root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s : %(message)s')
        handler.setFormatter(formatter)
        self.__root.addHandler(handler)


class Setup:
    __slots__ = ['logger']

    def __init__(self):
        self.logger = Logger()