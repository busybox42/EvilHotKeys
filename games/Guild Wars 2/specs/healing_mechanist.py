from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
import time
import keyboard

def healing_mechanist_rotation():
    while True:  # You'll control this loop from your main program
        if not keyboard.is_pressed(79):
            break
        press(79)
        release(79)
        press_and_release('1')
        press_and_release('2')
        press_and_release('3')
        time.sleep(0.5)
        
        if pixel_search((255, 255, 255), 2170, 2045, 2205, 2080):
            if pixel_get_color(1644, 2022) != (0, 0, 0):
                press(75)
                release(75)
                time.sleep(0.5)
                press(59)
                release(59)
                continue
            
            if pixel_get_color(1755, 2026) != (0, 0, 0):
                press(76)
                release(76)
                time.sleep(0.5)
                continue
            
            press(82)
            release(82)
            time.sleep(1)
        
        elif pixel_search((255, 255, 255), 2500, 2055, 2530, 2080):
            if pixel_get_color(1755, 2026) != (0, 0, 0):
                press(76)
                release(76)
            else:
                press(77)
                release(77)
            time.sleep(1)
        
        elif pixel_search((255, 255, 255), 2055, 2045, 2095, 2080):
            if pixel_get_color(1755, 2026) != (0, 0, 0):
                press(77)
                release(77)
            else:
                press(59)
                release(59)
            time.sleep(1)
        
        else:
            if pixel_get_color(1644, 2022) != (0, 0, 0):
                press(75)
                release(75)
            elif pixel_get_color(1755, 2026) != (0, 0, 0):
                press(76)
                release(76)
                press(71)
                release(71)
            else:
                press(78)
                release(78)
            time.sleep(1)
        
        press(80)
        release(80)
        time.sleep(0.5)
def run(stop_event):
    while not stop_event.is_set():
        while True:  # Main loop
            if keyboard.is_pressed(79):  # Check if numpad1 is being held down
                healing_mechanist_rotation()  # Run your existing function
            time.sleep(0.1)  # Sleep for a brief moment to reduce CPU usage
