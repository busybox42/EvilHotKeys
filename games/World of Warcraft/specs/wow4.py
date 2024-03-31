from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def wow4_rotation(stop_event):
    while not stop_event.is_set():  
        if not keyboard.is_pressed(key_mapping['numpad4']):  
            break
        
        while keyboard.is_pressed(key_mapping['numpad4']) and not stop_event.is_set():  
            if pixel_get_color(1015, 1695) != (0, 0, 0):  # Interupt target
                press_and_release('=')  
            press_and_release(key_mapping['numpad4'])  
            time.sleep(0.1)

def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):  
            wow4_rotation(stop_event)  
        time.sleep(0.1)  
