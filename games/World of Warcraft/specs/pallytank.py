from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
from PIL import ImageGrab
import time
import keyboard

# Constants
DEFAULT_COLOR = (0, 0, 0)

# Pally Tank Rotation Logic
def pallytank_rotation(stop_event):
    try:
        while not stop_event.is_set() and keyboard.is_pressed(key_mapping['numpad4']):
            # Grab the entire screen region once
            screen_image = ImageGrab.grab()

            # Extract pixel colors for checks
            interrupt_target = screen_image.getpixel((2345, 875))
            health_check_1 = screen_image.getpixel((2440, 995))
            
            # Interrupt target
            if interrupt_target != DEFAULT_COLOR:
                press_and_release('=')

            # Health checks for abilities
            if health_check_1 != DEFAULT_COLOR:
                press_and_release('5')
                press_and_release('4')

            # Default key press
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.2)  # Increased sleep to reduce CPU usage

    except Exception as e:
        print(f"An error occurred during pally tank rotation: {e}")

# Main run function
def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):
            pallytank_rotation(stop_event)
        time.sleep(0.1)  # Sleep to avoid busy-waiting