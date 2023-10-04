from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
import time
import keyboard

def condition_mechanist_rotation():
    while keyboard.is_pressed(79):  # Loop will break if NumPad1 is not pressed
        if not keyboard.is_pressed(79):
            break
        press_and_release('2')
        press_and_release('1')
        press_and_release('3')
        
        if pixel_search((255, 255, 255), 2170, 2045, 2205, 2080): # Grenade Kit
            sg = pixel_get_color(1425, 2025)
            pg = pixel_get_color(1755, 2026)
            signet = pixel_get_color(2285, 2026)
            fg = pixel_get_color(1644, 2022)
            
            if sg != (0, 0, 0):
                press(80)
                release(80)
                time.sleep(0.5)
                
            if pg != (0, 0, 0):
                press(76)
                release(76)
                time.sleep(0.5)
            
            if signet != (0, 0, 0):
                press(72)
                release(72)
                time.sleep(0.5)
            
            if fg != (0, 0, 0):
                press(75)
                release(75)
                time.sleep(0.5)
            
            if sg == (0, 0, 0) and pg == (0, 0, 0) and fg == (0, 0, 0):
                press(59)
                release(59)

            press(79)
            release(79)
        
        else:
            pdv = pixel_get_color(1425, 2025)
            bt = pixel_get_color(1644, 2022)
            ss = pixel_get_color(1530, 2025)
            
            if pdv != (0, 0, 0):
                press(80)
                release(80)
                time.sleep(0.5)
            
            if bt != (0, 0, 0):
                press(75)
                release(75)
                time.sleep(0.5)
            
            if ss != (0, 0, 0):
                press(81)
                release(81)
                time.sleep(0.5)
            
            if pdv == (0, 0, 0) and bt == (0, 0, 0) and ss == (0, 0, 0):
                press(71)
                release(71)
            
            press(79)
            release(79)

def run(stop_event):
    while not stop_event.is_set():
        while True:  # Main loop
            if keyboard.is_pressed(79):  
                condition_mechanist_rotation()
            time.sleep(0.1)  
