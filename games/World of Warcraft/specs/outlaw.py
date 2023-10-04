from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def outlaw_rotation():
    while True:
        if not keyboard.is_pressed(key_mapping['numpad4']):
            continue

        stealth = pixel_get_color(1145, 1950)
        if stealth != 0x000000:
            interupt = pixel_get_color(1015, 1695)
            if interupt != 0x000000:
                press_and_release('=')
            finish = pixel_get_color(1375, 2010)
            if finish != 0x000000:
                slice = pixel_get_color(1200, 2010)
                if slice != 0x000000:
                    press_and_release('8')
                else:
                    eyes = pixel_get_color(1140, 2010)
                    if eyes != 0x000000:
                        press_and_release('9')
                    else:
                        finish = pixel_get_color(1375, 1960)
                        if finish != 0x000000:
                            press_and_release('0')
            rush = pixel_get_color(1255, 2010)
            if rush != 0x000000:
                press(key_mapping['numpad9'])
                release(key_mapping['numpad9'])
            shoot = pixel_get_color(1310, 2010)
            if shoot != 0x000000:
                press_and_release('5')
            fient = pixel_get_color(1010, 1975)
            if fient != 0x000000:
                press(key_mapping['numpad6'])
                release(key_mapping['numpad6'])
            pot = pixel_get_color(1010, 2020)
            if pot != 0x000000:
                press_and_release('-')
            evade = pixel_get_color(1010, 1920)
            if evade != 0x000000:
                press(key_mapping['numpad6'])
                release(key_mapping['numpad6'])
 
        press(key_mapping['numpad4'])
        release(key_mapping['numpad4'])
        time.sleep(0.25)

def run(stop_event):
    while not stop_event.is_set():
        while True:  # Main loop
            if keyboard.is_pressed(key_mapping['numpad4']):  
                outlaw_rotation()  
            time.sleep(0.1) 