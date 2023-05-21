import socket
import time
import pyautogui


class Client:
    def __init__(
        self, server_ip: str = "192.168.0.101", server_port: int = 1234
    ) -> None:
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Define server address and port
        self.server_address = (server_ip, server_port)

    # close socket after client closed
    def __del__(self) -> None:
        self.client_socket.close()

    def run(self, debug_mode: bool = False) -> None:
        while True:
            data: str = self.client_socket.recv(512).decode("utf-8")
            # Print the received data
            if not data:
                raise ConnectionError
            if debug_mode:
                print("Received from server:", data)
            char: chr
            for char in data:
                pyautogui.keyDown(char)
                pyautogui.keyUp(char)

    def reconnect(self, debug_mode: bool = False) -> None:
        # Connect to the server
        i: int
        for i in range(10000):
            try:
                self.client_socket.connect(self.server_address)
                break
            except Exception as e:
                print(e)
                if debug_mode:
                    adr: str = "{}:{}".format(*self.server_address)
                    print(f"No connection to {adr} try reconnecting in {i}sec")
                time.sleep(i)

        if debug_mode:
            print("Connected to {}:{}".format(*self.server_address))


if __name__ == "__main__":
    debugs: bool = True
    c: Client = Client(server_ip="192.168.0.101", server_port=1234)
    while True:
        try:
            c.run(debug_mode=debugs)
        except Exception as e:
            print(e)
            c.reconnect(debug_mode=debugs)
