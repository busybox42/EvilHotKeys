import time
import keyboard
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
from libs.pixel_get_color import get_multiple_pixel_colors
from libs.logger import get_logger
from libs.wow_helpers import get_coords, log_coords_once

logger = get_logger('tank')

DEFAULT_COLOR = (0, 0, 0)

def handle_pixel_action(condition_color, key):
    if condition_color != DEFAULT_COLOR:
        press_and_release(key)

def tank_rotation(stop_event):
    try:
        # Load coordinates from config
        interrupt, health50, health35, health25, health75 = get_coords(
            'interrupt', 'health_50', 'health_35', 'health_25', 'health_75'
        )
        
        # Log once for debugging
        log_coords_once({
            'interrupt': interrupt,
            'health_50': health50,
            'health_35': health35,
            'health_25': health25,
            'health_75': health75
        })
        
        while not stop_event.is_set():
            # Check stop event first
            if stop_event.is_set():
                break
                
            if keyboard.is_pressed(key_mapping['numpad4']):
                # Get all pixel colors using config coordinates
                coords = [interrupt, health50, health35, health25, health75]
                
                # Get all pixel colors efficiently in one call
                colors = get_multiple_pixel_colors(coords)
                
                if len(colors) == 5:
                    interrupt_color, health50_color, health35_color, health25_color, health75_color = colors
                    
                    # Perform actions based on pixel colors
                    handle_pixel_action(interrupt_color, '=')
                    handle_pixel_action(health50_color, '4')
                    handle_pixel_action(health35_color, '5')
                    handle_pixel_action(health25_color, '3')
                    handle_pixel_action(health75_color, '1')

                press_and_release(key_mapping['numpad4'])
                time.sleep(0.2)  # Sleep after action

            # Always sleep to prevent busy-waiting
            time.sleep(0.05)
    except Exception as e:
        logger.exception(f"An error occurred during tank rotation: {e}")

def run(stop_event):
    tank_rotation(stop_event)
