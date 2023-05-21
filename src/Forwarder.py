import logging
import socket
import ipaddress

class Forwarder:
    def __init__(self, server_ip: str = "192.168.0.101", port: int = 1234) -> None:
        if server_ip:
            self.server_ip=server_ip
            self.port = port
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # socket can be reopened imminently
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Define server address and port
            # server_address = (server_ip, port)
            server_address = (server_ip, 1234)
            # Bind the socket to the server address
            self.server_socket.bind(server_address)
            logging.info(f"Server created")
            self.listen()

    # close all the sockets
    def __del__(self) -> None:
        self.server_socket.close()
        self.client_socket.close()

    def send_over_network(self, data: str = None) -> None:
        self.client_socket.sendall(data.encode("utf-8"))

    def listen(self, network_ip: str = None, port: int = 1234) -> str:
        server_address = ((lambda i: i if i else self.server_ip)(network_ip), (lambda p: p if p else self.port)(port))
        # Listen for incoming connections
        self.server_socket.listen(1)
        logging.info("Server is listening on {}:{}".format(*server_address))
        # Accept a client connection
        self.client_socket, client_address = self.server_socket.accept()
        logging.info("Client connected: {}:{}".format(*client_address))
        return str(client_address)
