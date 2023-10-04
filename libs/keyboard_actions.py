import keyboard
import time

def press_and_release(key, delay=0.5):
    keyboard.press_and_release(key)
    time.sleep(delay)

def hold_key_while_pressed(hotkey, keys_to_press, delay=0.5):
    while keyboard.is_pressed(hotkey):
        for key in keys_to_press:
            press_and_release(key, delay)

def press(key):
    keyboard.press(key)

def release(key):
    keyboard.release(key)
