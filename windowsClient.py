import pyautogui
import time
from pynput import keyboard


# Delay for a few seconds to give time to focus on the desired window
time.sleep(2)

# Simulate key press event for "a"


def on_press(key):
    try:
        print('Key pressed: {0}'.format(key.char))
        pyautogui.press(key.char)
    except AttributeError:
        print('Special key pressed: {0}'.format(key))

def on_release(key):
    print('Key released: {0}'.format(key))
    if key == keyboard.Key.esc:
        # Stop the listener
        return False

# Create a listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# Start the listener in a separate thread
listener.start()

while True:
    pass