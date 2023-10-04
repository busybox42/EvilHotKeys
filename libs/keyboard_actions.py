import keyboard
import time

# Define a function to press and release a key with an optional delay
def press_and_release(key, delay=0.5):
    keyboard.press_and_release(key)  
    time.sleep(delay)  

# Define a function to hold down a key while a hotkey is pressed
def hold_key_while_pressed(hotkey, keys_to_press, delay=0.5):
    while keyboard.is_pressed(hotkey):  
        for key in keys_to_press:  
            press_and_release(key, delay)  

# Define a function to press a key
def press(key):
    keyboard.press(key)  

# Define a function to release a key
def release(key):
    keyboard.release(key)  