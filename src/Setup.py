import sys
import logging
import argparse


class Logger:
    __slots__ = ['__main_logger', '__mode']

    def __init__(self, mode: str | None) -> None:
        self.__mode = mode
        self.__main_logger = logging.getLogger()
        if mode == "debug" or mode == "d":
            self.__main_logger.setLevel(logging.DEBUG)
        elif mode is None or mode == "production" or mode == "p":
            self.__main_logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s : %(message)s')
        handler.setFormatter(formatter)
        self.__main_logger.addHandler(handler)


class Setup:
    __slots__ = ['logger']

    def __init__(self, args):
        self.logger = Logger((lambda m: m if m else None)(args.mode))
