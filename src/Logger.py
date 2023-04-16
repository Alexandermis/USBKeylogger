import usb.core, usb.util


class Logger:
    __slots__ = ['vendor_ids']

    def __init__(self) -> None:
        self.vendor_ids: list[int] = self.get_vendor_id()

    def __del__(self):
        pass

    @staticmethod
    def get_vendor_id() -> list[int]:
        devices = usb.core.find(find_all=True)
        vendor_ids: list[int] = []
        # Enumerate over all USB devices
        for device in devices:
            try:
                vendor_ids.append(device.idVendor)
            except usb.core.USBError as e:
                print(f"Error reading Vendor ID: {e}")
        return vendor_ids

    # TODO: Rewrite this code
    def run(self):
        # Geräteinformationen
        vendor_id: int = 0x1234  # Beispiel-Vendor-ID, bitte durch die richtige ID ersetzen
        product_id: int = 0x5678  # Beispiel-Product-ID, bitte durch die richtige ID ersetzen

        # USB-Gerät finden
        dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        if dev is None:
            raise ValueError("USB-Gerät nicht gefunden.")

        # USB-Gerät öffnen
        dev.set_configuration()
        usb.util.claim_interface(dev, 0)
        try:
            # Endlosschleife zum Abhören des USB-Verkehrs
            while True:
                data = dev.read(0x81, 64)  # Endpoint-Adresse und Puffergröße anpassen
                # Hier können Sie mit den USB-Daten weiterarbeiten
                print("Empfangene Daten: ", data)
        except KeyboardInterrupt:
            pass
        finally:
            usb.util.release_interface(dev, 0)
            dev.reset()


if __name__ == "__main__":
    pass
