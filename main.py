import logging
import argparse


from src.Setup import Setup
from src.Logger import Logger

def main(args: argparse.ArgumentParser) -> None:
    setup: Setup = Setup(args)
    logging.info("Starting")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Python Hardware Keylogger')
    parser.add_argument('-m', '--mode', type=str, help='This Logger level d=debug, p=production')
    args = parser.parse_args()
    main(args)
