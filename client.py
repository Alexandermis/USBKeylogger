import usb.core
import keyboard

if __name__ == "__main__":
    # find the USB device
    dev = usb.core.find(idVendor=0x0000, idProduct=0x0000)

    # set the configuration
    dev.set_configuration()
    while True:
        data = keyboard.read(8)  # Read an 8-byte HID report
        if data:
            key_code = data[2]  # The key code is in byte 2
            if key_code < 30:
                char = chr(key_code + 93)  # Convert the key code to a character
            elif 30 <= key_code and key_code < 49:
                char = chr(key_code + 19)
            elif key_code == 39:
                char = chr(39 + 9)
            else:
                char = "Not FOUND"
            keyboard.press_and_release(f'{char}')



