import socket
import pyautogui


class Client:
    def __init__(self, server_ip: str = '192.168.0.101', server_port: int = 1234) -> None:
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Define server address and port
        self.server_address = (server_ip, server_port)
    # close socket after client closed
    def __del__(self):
        self.client_socket.close()

    def run(self, debug_mode: bool = False):
        data: str = None
        while True:
            data: str = self.client_socket.recv(1024).decode('utf-8')
            # Print the received data
            if debug_mode:
                print('Received from server:', data)
            for char in data:
                if not data:
                    pass
                elif char == "]":
                    pass
                else:
                    pyautogui.keyDown(char)
                    pyautogui.keyUp(char)
            if data.lower() == 'exit':
                break

    def reconnect(self, debug_mode: bool = False):
        # Connect to the server
        self.client_socket.connect(self.server_address)
        if debug_mode:
            print('Connected to {}:{}'.format(*self.server_address))


if __name__ == "__main__":
    debugs = True
    c = Client()
    while True:
        try:
            c.run(debug_mode=debugs)
        except Exception as e:
            print(e)
            c.reconnect(debug_mode=debugs)
