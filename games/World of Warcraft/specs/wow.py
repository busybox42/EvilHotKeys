from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def wow_rotation(keys_to_watch, stop_event):
    while not stop_event.is_set():  
        for key in keys_to_watch:
            if not keyboard.is_pressed(key_mapping[key]):
                continue

            if pixel_get_color(2345, 875) != (0, 0, 0): # Interupt target
                press_and_release('=')
            press(key_mapping[key])
            release(key_mapping[key])
            time.sleep(0.1)
            if stop_event.is_set():  
                break

def run(stop_event):
    keys_to_watch = ['numpad4', 'numpad5', 'numpad7']  
    while not stop_event.is_set():
        wow_rotation(keys_to_watch, stop_event)
        time.sleep(0.1)  
