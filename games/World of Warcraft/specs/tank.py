from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def tank_rotation(stop_event):
    while not stop_event.is_set():
       
        if keyboard.is_pressed(key_mapping['numpad4']):
            interrupt = pixel_get_color(2345, 875)
            healerhealth = pixel_get_color(2345, 920)
            health50 = pixel_get_color(2375, 995)
            health35 = pixel_get_color(2405, 995)
            health25 = pixel_get_color(2440, 995)  
            health75 = pixel_get_color(2345, 995)

            if interrupt != (0, 0, 0):
                press_and_release('=')
            if healerhealth != (0, 0, 0):
                press_and_release('5')
            if health50 != (0, 0, 0):
                press_and_release('4')
            if health35 != (0, 0, 0):
                press_and_release('5')
            if health25 != (0, 0, 0):
                press_and_release('3')
            if health75 != (0, 0, 0):
                press_and_release('0')

            press_and_release(key_mapping['numpad4'])
            
            time.sleep(0.01) 

def run(stop_event):
    while not stop_event.is_set():
        tank_rotation(stop_event)
        time.sleep(0.1)  
