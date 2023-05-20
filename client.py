import usb.core
import keyboard
import socket
import pyautogui
def client(server_ip: str ='192.168.0.101', server_port: int = 1234):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define server address and port
    server_address = (server_ip, server_port)

    # Connect to the server
    client_socket.connect(server_address)
    print('Connected to {}:{}'.format(*server_address))
    data = None
    while True:
        # Receive data from the server
        data: str = client_socket.recv(1024).decode('utf-8')
        for char in data:
            if not data:
                pass
            elif data == "]":
                pass
            else:
                pyautogui.keyDown(char)
                pyautogui.keyUp(char)

        # Print the received data
        print('Received from server:', data)

        if data.lower() == 'exit':
            break

    # Close the client socket
    client_socket.close()
#
if __name__ == "__main__":
    client()
    # # find the USB device
    # dev = usb.core.find(idVendor=0x247d, idProduct=0x0242)
    # backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\PATH\\libusb-1.0.20\\MS32\\dll\\libusb-1.0.dll")
    # usb_devices = usb.core.find(backend=backend, find_all=True)
    # # set the configuration
    # dev.set_configuration()
    # while True:
    #     data = keyboard.read(8)  # Read an 8-byte HID report
    #     if data:
    #         key_code = data[2]  # The key code is in byte 2
    #         if key_code < 30:
    #             char = chr(key_code + 93)  # Convert the key code to a character
    #         elif 30 <= key_code and key_code < 49:
    #             char = chr(key_code + 19)
    #         elif key_code == 39:
    #             char = chr(39 + 9)
    #         else:
    #             char = "Not FOUND"
    #         keyboard.press_and_release(f'{char}')



