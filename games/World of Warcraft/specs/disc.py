from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
import time
import keyboard

def wow4_rotation(stop_event):
    while not stop_event.is_set():
        if not keyboard.is_pressed(key_mapping['numpad4']):
            break

        while keyboard.is_pressed(key_mapping['numpad4']) and not stop_event.is_set():
            # Check focus health
            if pixel_get_color(2345, 915) != (0, 0, 0):
                press_and_release('=')

            # Check health below 50%
            if pixel_get_color(2375, 995) != (0, 0, 0):
                press_and_release('-')

            # Default key press
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.1)

def wow7_rotation(stop_event):
    while not stop_event.is_set():
        if not keyboard.is_pressed(key_mapping['numpad7']):
            break

        while keyboard.is_pressed(key_mapping['numpad7']) and not stop_event.is_set():
            # Check focus health
            if pixel_get_color(2345, 915) != (0, 0, 0):
                press_and_release('=')

            # Check health below 50%
            if pixel_get_color(2375, 995) != (0, 0, 0):
                press_and_release('-')

            # Default key press
            press_and_release(key_mapping['numpad7'])
            time.sleep(0.1)

def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):
            wow4_rotation(stop_event)
        elif keyboard.is_pressed(key_mapping['numpad7']):
            wow7_rotation(stop_event)
        time.sleep(0.1)

