from libs.pixel_get_color import get_color as pixel_get_color, get_multiple_pixel_colors
from libs.keyboard_actions import press_and_release, press
from libs.key_mapping import key_mapping
from libs.logger import get_logger
from libs.wow_helpers import get_coords, log_coords_once
import time
import keyboard

logger = get_logger('druidheals')

# Constants
DEFAULT_COLOR = (0, 0, 0)

# Druid Heals Rotation Logic
def druidheals_rotation(stop_event):
    try:
        # Get coordinates from config
        druid_interrupt, druid_finish = get_coords('druid_interrupt', 'druid_finish')
        log_coords_once({'interrupt': druid_interrupt, 'finish': druid_finish})
        
        druid_interrupt_x, druid_interrupt_y = druid_interrupt
        
        while not stop_event.is_set():
            # NumPad4 behavior
            if keyboard.is_pressed(key_mapping['numpad4']):
                # Check interrupt using abstraction layer
                interrupt_target = pixel_get_color(druid_interrupt_x, druid_interrupt_y)
                if interrupt_target and interrupt_target != DEFAULT_COLOR:
                    press_and_release('=')

                # Default key press
                press_and_release(key_mapping['numpad4'])
                time.sleep(0.25)  # Sleep 250ms as per AHK script

            # NumPad5 behavior with a continuous loop while held
            if keyboard.is_pressed(key_mapping['numpad5']):
                while keyboard.is_pressed(key_mapping['numpad5']) and not stop_event.is_set():
                    # Get pixel colors efficiently
                    colors = get_multiple_pixel_colors([druid_interrupt, druid_finish])
                    
                    if len(colors) == 2:
                        interrupt_target, finish_color = colors
                        
                        # Check for interrupt
                        if interrupt_target and interrupt_target != DEFAULT_COLOR:
                            press_and_release('=')

                        # Combo bust
                        if finish_color and finish_color != DEFAULT_COLOR:
                            press_and_release('0')

                    # Sending a modified input equivalent to Control + NumPad4
                    press('ctrl')
                    press_and_release(key_mapping['numpad4'])
                    keyboard.release('ctrl')

                    time.sleep(0.25)  # Sleep 250ms as per AHK script

    except Exception as e:
        logger.exception(f"An error occurred during druid heals rotation: {e}")

# Main run function
def run(stop_event):
    while not stop_event.is_set():
        druidheals_rotation(stop_event)
        time.sleep(0.1)  # Sleep to avoid busy-waiting
