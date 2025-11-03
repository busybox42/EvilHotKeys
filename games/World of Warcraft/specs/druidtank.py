import time  # Import the time module
import mss
import keyboard
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping

DEFAULT_COLOR = (0, 0, 0)

def handle_pixel_action(condition_color, key):
    if condition_color != DEFAULT_COLOR:
        press_and_release(key)

def tank_rotation(stop_event):
    try:
        with mss.mss() as sct:
            
            while not stop_event.is_set():
                if keyboard.is_pressed(key_mapping['numpad4']):

                    # Get colors of specific pixels (adjust offsets for your coordinates)
                    interrupt = pixels[2456][2015]   # (2505, 970) relative to top-left of monitor
                    health50 = pixels[2483][1047]  # (2530, 998)
                    health75 = pixels[2554][1047]  # (2505, 998)

                    # Perform actions based on pixel colors
                    handle_pixel_action(interrupt, '=')
                    handle_pixel_action(health50, '5')
                    handle_pixel_action(health75, '4')

                    press_and_release(key_mapping['numpad4'])

                # Adjust sleep for minimal delay without excessive CPU usage
                time.sleep(0.1)
    except Exception as e:
        print(f"An error occurred during tank rotation: {e}")

def run(stop_event):
    tank_rotation(stop_event)
