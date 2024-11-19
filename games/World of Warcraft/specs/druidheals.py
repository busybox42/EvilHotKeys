import time
import keyboard
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press
from libs.key_mapping import key_mapping

def wow_rotation(stop_event):
    # Watch for specific keys and respond accordingly
    while not stop_event.is_set():
        # NumPad4 behavior
        if keyboard.is_pressed(key_mapping['numpad4']):  # Using scan code for NumPad4
            interupt_color = pixel_get_color(2345, 875)
            if interupt_color != (0, 0, 0):  # Equivalent to checking if color is not black
                press_and_release('=')
            press_and_release(key_mapping['numpad4'])  # Use the mapped scan code
            time.sleep(0.25)  # Sleep 250ms as per AHK script

        # NumPad7 behavior with a continuous loop while held
        if keyboard.is_pressed(key_mapping['numpad5']):  # Using scan code for NumPad7
            while keyboard.is_pressed(key_mapping['numpad5']):  # Loop as long as NumPad7 is held down
                interupt_color = pixel_get_color(2345, 875)
                if interupt_color != (0, 0, 0):  # Check for interrupt
                    press_and_release('=')

                finish_color = pixel_get_color(2378, 878)
                if finish_color != (0, 0, 0):  # Check for another action
                    press_and_release('0')

                # Sending a modified input equivalent to Control + NumPad4
                press('ctrl')
                press_and_release(key_mapping['numpad4'])  # Use scan code for Ctrl + NumPad4
                keyboard.release('ctrl')

                time.sleep(0.25)  # Sleep 250ms as per AHK script

        # Exit the loop if the stop_event is set
        if stop_event.is_set():
            break

def run(stop_event):
    while not stop_event.is_set():
        wow_rotation(stop_event)
        time.sleep(0.1)  # Sleep 100ms between rotations

