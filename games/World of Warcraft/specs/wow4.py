from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
from libs.logger import get_logger
from libs.wow_helpers import get_coord
import time
import keyboard

logger = get_logger('wow4')

# Constants
DEFAULT_COLOR = (0, 0, 0)

# WoW4 Rotation Logic
def wow4_rotation(stop_event):
    try:
        # Get interrupt coordinate from config
        interrupt_x, interrupt_y = get_coord('interrupt')
        logger.info(f"Using interrupt coordinate: ({interrupt_x}, {interrupt_y})")
        
        while not stop_event.is_set():
            # Check stop event first
            if stop_event.is_set():
                break
                
            # Only continue if key is still pressed
            if not keyboard.is_pressed(key_mapping['numpad4']):
                break
            # Check interrupt using abstraction layer
            interrupt_target = pixel_get_color(interrupt_x, interrupt_y)
            if interrupt_target and interrupt_target != DEFAULT_COLOR:
                press_and_release('=')

            # Default key press
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.2)  # Increased sleep to reduce CPU usage

    except Exception as e:
        logger.exception(f"An error occurred during wow4 rotation: {e}")

# Main run function
def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):
            wow4_rotation(stop_event)
        time.sleep(0.1)  # Sleep to avoid busy-waiting
