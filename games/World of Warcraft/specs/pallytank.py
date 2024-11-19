from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
import time
import keyboard

def pallytank_rotation(stop_event):
    while not stop_event.is_set():
        if not keyboard.is_pressed(key_mapping['numpad4']):
            break

        while keyboard.is_pressed(key_mapping['numpad4']) and not stop_event.is_set():
            # Interrupt target
            if pixel_get_color(2345, 875) != (0, 0, 0):  
                press_and_release('=')

            if pixel_get_color(2440, 995) != (0, 0, 0):  
                press_and_release('5')

            if pixel_get_color(2440, 995) != (0, 0, 0):  
                press_and_release('4')

            # Continue with default key press
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.1)

def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):
            pallytank_rotation(stop_event)
        time.sleep(0.1)

