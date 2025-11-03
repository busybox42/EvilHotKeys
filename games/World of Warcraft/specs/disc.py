from libs.pixel_get_color import get_color as pixel_get_color, get_multiple_pixel_colors
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
from libs.logger import get_logger
from libs.wow_helpers import get_coords, log_coords_once
import time
import keyboard

logger = get_logger('disc')

# Constants
DEFAULT_COLOR = (0, 0, 0)

# Helper function for pixel actions
def handle_pixel_action(condition_color, key):
    if condition_color and condition_color != DEFAULT_COLOR:
        press_and_release(key)

# Disc rotation logic for numpad4
def wow4_rotation(stop_event):
    try:
        # Get coordinates from config
        focus_health, health_below_50 = get_coords('focus_health', 'health_below_50')
        log_coords_once({'focus_health': focus_health, 'health_below_50': health_below_50})
        
        while not stop_event.is_set() and keyboard.is_pressed(key_mapping['numpad4']):
            # Get pixel colors efficiently
            colors = get_multiple_pixel_colors([focus_health, health_below_50])
            
            if len(colors) == 2:
                focus_health, health_below_50 = colors
                
                # Handle actions based on pixel colors
                handle_pixel_action(focus_health, '=')
                handle_pixel_action(health_below_50, '-')

            # Default key press
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.2)  

    except Exception as e:
        logger.exception(f"An error occurred during wow4 rotation: {e}")

# Disc rotation logic for numpad7
def wow7_rotation(stop_event):
    try:
        # Get coordinates from config
        focus_health, health_below_50 = get_coords('focus_health', 'health_below_50')
        
        while not stop_event.is_set() and keyboard.is_pressed(key_mapping['numpad7']):
            # Get pixel colors efficiently
            colors = get_multiple_pixel_colors([focus_health, health_below_50])
            
            if len(colors) == 2:
                focus_health, health_below_50 = colors
                
                # Handle actions based on pixel colors
                handle_pixel_action(focus_health, '=')
                handle_pixel_action(health_below_50, '-')

            # Default key press
            press_and_release(key_mapping['numpad7'])
            time.sleep(0.2)  

    except Exception as e:
        logger.exception(f"An error occurred during wow7 rotation: {e}")

# Main run function
def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):
            wow4_rotation(stop_event)
        elif keyboard.is_pressed(key_mapping['numpad7']):
            wow7_rotation(stop_event)
        time.sleep(0.1)  # Sleep to avoid busy-waiting
