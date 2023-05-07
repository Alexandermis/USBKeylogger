import usb.core
from typing import Optional


class USBForwarder:
    __slots__ = ["device"]

    def __init__(self, device: Optional[usb.core.Device]) -> None:
        self.device: Optional[usb.core.Device] = device

    def send_data(self, endpoint, data):
        for i in range(5):
            try:
                self.device.write(endpoint.bEndpointAddress, data)
            except usb.core.USBError as e:
                print("Error sending data: {}".format(str(e)))
        raise usb.core.USBError(error_code=42)
