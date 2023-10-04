from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def wow4_rotation():
    while True:  # Loop will break if NumPad4 is not pressed
        if not keyboard.is_pressed(key_mapping['numpad4']):
            break
        if pixel_get_color(1015, 1695) != (0, 0, 0): # Interupt target
            press_and_release('=')
        press(key_mapping['numpad4']) # Run GnomeSequence macro
        release(key_mapping['numpad4'])
        time.sleep(0.1)

def run(stop_event):
    while not stop_event.is_set():
        while True:  # Main loop
            if keyboard.is_pressed(key_mapping['numpad4']):  
                wow4_rotation()  
            time.sleep(0.1)
