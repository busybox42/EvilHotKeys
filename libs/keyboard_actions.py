import keyboard
import time

# Define a function to press and release a key with an optional delay
def press_and_release(key, delay=0.02):
    keyboard.press_and_release(key)
    if delay > 0:
        time.sleep(delay)

# Define a function to hold down a key while a hotkey is pressed
def hold_key_while_pressed(hotkey, keys_to_press, delay=0.02):
    while keyboard.is_pressed(hotkey):
        for key in keys_to_press:
            press_and_release(key, delay)
        time.sleep(0.05)  # Add a small delay to reduce CPU usage

# Define a function to press a key
def press(key):
    try:
        keyboard.press(key)
    except ValueError:
        print(f"Error: Key '{key}' is not recognized.")

# Define a function to release a key
def release(key):
    try:
        keyboard.release(key)
    except ValueError:
        print(f"Error: Key '{key}' is not recognized.")
