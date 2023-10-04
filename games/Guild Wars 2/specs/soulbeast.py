import time
import keyboard
from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press, release, press_and_release
from libs.key_mapping import key_mapping

def soulbeast_rotation():
    while True:
        if not keyboard.is_pressed(key_mapping['numpad1']):
            break
        press(key_mapping['numpad1'])
        release(key_mapping['numpad1'])
        px, py, _, _ = pixel_search(0x86E75D, 1283, 1901, 1331, 1952, 5, 'fast', 'rgb', 'relative')
        if px != -1 and py != -1: # Keep beast mode up
            press_and_release('5')
            time.sleep(0.1)
            axe = pixel_get_color(1328, 2037)
            if axe != (0, 0, 0): # Are we using an Axe or Bow?
                barrage = pixel_get_color(1755, 2026)
                if barrage != (0, 0, 0):
                    press(key_mapping['numpad5'])
                    release(key_mapping['numpad5'])
                    time.sleep(0.1)
                frosttrap = pixel_get_color(2395, 2026)
                if frosttrap != (0, 0, 0):
                    press(key_mapping['numpad9'])
                    release(key_mapping['numpad9'])
                    time.sleep(0.1)
                sicem = pixel_get_color(2286, 2026)
                if sicem != (0, 0, 0):
                    press(key_mapping['numpad8'])
                    release(key_mapping['numpad8'])
                    time.sleep(0.1)
                pbshot = pixel_get_color(1644, 2026)
                if pbshot != (0, 0, 0):
                    press(key_mapping['numpad4'])
                    release(key_mapping['numpad4'])
                    time.sleep(0.1)
                owp = pixel_get_color(2505, 2026)
                if owp != (0, 0, 0):
                    press(key_mapping['numpad0'])
                    release(key_mapping['numpad0'])
                    time.sleep(0.1)
                rfire = pixel_get_color(1425, 2025)
                if rfire != (0, 0, 0):
                    press(key_mapping['numpad2'])
                    release(key_mapping['numpad2'])
                    time.sleep(0.1)
                swap = pixel_get_color(1220, 2020)
                if swap != (0, 0, 0):
                    if (barrage == (0, 0, 0) and frosttrap == (0, 0, 0) and sicem == (0, 0, 0) and pbshot == (0, 0, 0)):
                        press(key_mapping['f1'])
                        release(key_mapping['f1'])
                        time.sleep(0.1)
            else:
                splinterblade = pixel_get_color(1425, 2025)
                if splinterblade != (0, 0, 0):
                    press(key_mapping['numpad2'])
                    release(key_mapping['numpad2'])
                    time.sleep(0.1)
                wbite = pixel_get_color(1530, 2025)
                if wbite != (0, 0, 0):
                    press(key_mapping['numpad3'])
                    release(key_mapping['numpad3'])
                    time.sleep(0.1)
                scars = pixel_get_color(1644, 2022)
                if scars != (0, 0, 0):
                    press(key_mapping['numpad4'])
                    release(key_mapping['numpad4'])
                    time.sleep(0.1)
                wdef = pixel_get_color(1755, 2026)
                if wdef != (0, 0, 0):
                    press(key_mapping['numpad5'])
                    release(key_mapping['numpad4'])
                    time.sleep(0.1)
                swap = pixel_get_color(1220, 2020)
                if swap != (0, 0, 0):
                    if (splinterblade == (0, 0, 0) and wbite == (0, 0, 0) and scars == (0, 0, 0)):
                        press(key_mapping['f1'])
                        release(key_mapping['f1'])
                        time.sleep(0.1)
        else:
            impact = pixel_get_color(1649, 1911)
            if impact != (0, 0, 0):
                press(key_mapping['numpad3'])
                release(key_mapping['numpad3'])
                time.sleep(0.1)
            else:
                impact = pixel_get_color(1547, 1912)
                if impact != (0, 0, 0):
                    press(key_mapping['numpad2'])
                    release(key_mapping['numpad2'])
                    time.sleep(0.1)
        press(key_mapping['numpad1'])
        release(key_mapping['numpad1'])

def run(stop_event):
    while not stop_event.is_set():
        while True:  # Main loop
            if keyboard.is_pressed(key_mapping['numpad1']):  
                soulbeast_rotation()  
            time.sleep(0.1) 