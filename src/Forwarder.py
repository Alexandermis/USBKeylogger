import logging

import usb.core
from typing import Optional
import socket


class Forwarder:
    # __slots__ = ["device", "server_socket ", "client_socket"]

    def __init__(self, device: Optional[usb.core.Device] = None, network_ip: str = "192.168.0.101",
                 port: int = 1234) -> None:
        self.device: Optional[usb.core.Device] = device
        if network_ip:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Define server address and port
            server_address = (network_ip, port)
            # Bind the socket to the server address
            self.server_socket.bind(server_address)
            logging.INFO(f'Server created')
            self.listen()
    #
    # def send_data(self, endpoint, data):
    #     for i in range(5):
    #         try:
    #             self.device.write(endpoint.bEndpointAddress, data)
    #         except usb.core.USBError as e:
    #             print("Error sending data: {}".format(str(e)))
    #     raise usb.core.USBError(error_code=42)

    def send_over_network(self, data: str = None):
        if data:
            print(data)
        else:
            print("None")
        self.client_socket.sendall(data.encode('utf-8'))

    def listen(self, network_ip: str = "192.168.0.101", port: int = 1234):
        server_address = (network_ip, port)
        # Listen for incoming connections
        self.server_socket.listen(1)
        print('Server is listening on {}:{}'.format(*server_address))
        # Accept a client connection
        self.client_socket, client_address = self.server_socket.accept()
        print(f'Client connected: {str(client_address)}')
