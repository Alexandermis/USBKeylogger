import logging
import socket


class Forwarder:

    def __init__(self,  network_ip: str = "192.168.0.101",
                 port: int = 1234) -> None:
        if network_ip:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Define server address and port
            server_address = (network_ip, port)
            # Bind the socket to the server address
            self.server_socket.bind(server_address)
            logging.info(f'Server created')
            self.listen()

    def send_over_network(self, data: str = None):
        self.client_socket.sendall(data.encode('utf-8'))

    def listen(self, network_ip: str = "192.168.0.101", port: int = 1234) -> str:
        server_address = (network_ip, port)
        # Listen for incoming connections
        self.server_socket.listen(1)
        logging.info('Server is listening on {}:{}'.format(*server_address))
        # Accept a client connection
        self.client_socket, client_address = self.server_socket.accept()
        logging.info('Client connected: {}:{}'.format(*client_address))
        return str(client_address)

