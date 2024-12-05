import pynput
from time import sleep
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Controller, KeyCode

controller = Controller()

def on_press(key):
    if key == KeyCode.from_char(','):
        controller.press(pynput.keyboard.Key.enter)
        controller.release(pynput.keyboard.Key.enter)

def on_click(x, y, button, pressed):
    if pressed and button == pynput.mouse.Button.left:
        controller.press(pynput.keyboard.Key.enter)
        controller.release(pynput.keyboard.Key.enter)
    elif pressed and button == pynput.mouse.Button.right:
        controller.press(pynput.keyboard.Key.esc)
        controller.release(pynput.keyboard.Key.esc)
        sleep(0.05)
        controller.press('m')
        controller.release('m')
    elif pressed and button == pynput.mouse.Button.middle:
        controller.press('v')
        controller.release('v')

try:
    # Setup the listener threads
    keyboard_listener = KeyboardListener(on_press=on_press)
    mouse_listener = MouseListener(on_click=on_click)

    # Start the threads
    keyboard_listener.start()
    mouse_listener.start()

    # Keep the script running until interrupted
    while True:
        sleep(1)

except KeyboardInterrupt:
    # Clean up and exit gracefully
    keyboard_listener.stop()
    mouse_listener.stop()
