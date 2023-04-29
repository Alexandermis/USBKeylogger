import sys
import logging
import argparse
from src.DataHandler import DataHandler


class Logger:
    __slots__ = ['root_handler', 'stream_handler', '__mode']

    def __init__(self, mode: str | None) -> None:
        self.__mode = mode
        self.root_handler = logging.getLogger()
        if mode == "debug" or mode == "d":
            self.root_handler.setLevel(logging.DEBUG)
        elif mode is None or mode == "production" or mode == "p":
            self.root_handler.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s : %(message)s')
        handler.setFormatter(formatter)
        self.root_handler.addHandler(handler)
        logging.info("Starting Python Hardware Keylogger")




class Setup:
    __slots__ = ['logger', 'dataHandler']

    def __init__(self, args):
        self.logger = Logger((lambda m: m if m else None)(args.mode))
        self.dataHandler = DataHandler()
        logging.info("Setup Complete")
