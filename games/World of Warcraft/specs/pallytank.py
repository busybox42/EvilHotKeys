from libs.pixel_get_color import get_color as pixel_get_color, get_multiple_pixel_colors
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
from libs.logger import get_logger
from libs.wow_helpers import get_coords, log_coords_once
import time
import keyboard

logger = get_logger('pallytank')

# Constants
DEFAULT_COLOR = (0, 0, 0)

# Pally Tank Rotation Logic
def pallytank_rotation(stop_event):
    try:
        # Get coordinates from config
        pally_interrupt, pally_h3, pally_h4, pally_h5, pally_h6 = get_coords(
            'pally_interrupt', 'pally_health_3', 'pally_health_4', 'pally_health_5', 'pally_health_6'
        )
        log_coords_once({
            'interrupt': pally_interrupt,
            'health_3': pally_h3,
            'health_4': pally_h4,
            'health_5': pally_h5,
            'health_6': pally_h6
        })
        
        while not stop_event.is_set() and keyboard.is_pressed(key_mapping['numpad4']):
            # Get all pixel colors efficiently
            coords = [pally_interrupt, pally_h3, pally_h4, pally_h5, pally_h6]
            colors = get_multiple_pixel_colors(coords)

            if len(colors) == 5:
                interrupt_target, health_check_3, health_check_4, health_check_5, health_check_6 = colors
                
                # Interrupt target
                if interrupt_target and interrupt_target != DEFAULT_COLOR:
                    press_and_release('=')

                # Health checks for abilities
                if health_check_3 and health_check_3 != DEFAULT_COLOR:
                    press_and_release('3')

                if health_check_4 and health_check_4 != DEFAULT_COLOR:
                    press_and_release('4')

                if health_check_5 and health_check_5 != DEFAULT_COLOR:
                    press_and_release('5')

                if health_check_6 and health_check_6 != DEFAULT_COLOR:
                    press_and_release('6')

            # Default key press
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.2)  # Increased sleep to reduce CPU usage

    except Exception as e:
        logger.exception(f"An error occurred during pally tank rotation: {e}")

# Main run function
def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad4']):
            pallytank_rotation(stop_event)
        time.sleep(0.1)  # Sleep to avoid busy-waiting
