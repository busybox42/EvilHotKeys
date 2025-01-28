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
            # Define the bounding box for your screen region (adjust based on your screen)
            monitor = {"top": 800, "left": 2300, "width": 200, "height": 250}
            
            while not stop_event.is_set():
                if keyboard.is_pressed(key_mapping['numpad4']):
                    # Capture the defined region
                    screen_image = sct.grab(monitor)
                    pixels = screen_image.pixels  # Access pixel data

                    # Get colors of specific pixels (adjust offsets for your coordinates)
                    interrupt = pixels[75][45]   # (2345, 875) relative to top-left of monitor
                    healerhealth = pixels[120][45]  # (2345, 920)
                    health50 = pixels[195][75]  # (2375, 995)
                    health35 = pixels[195][105]  # (2405, 995)
                    health25 = pixels[195][140]  # (2440, 995)
                    health75 = pixels[195][45]  # (2345, 995)

                    # Perform actions based on pixel colors
                    handle_pixel_action(interrupt, '=')
                    handle_pixel_action(healerhealth, '5')
                    handle_pixel_action(health50, '4')
                    handle_pixel_action(health35, '5')
                    handle_pixel_action(health25, '3')
                    handle_pixel_action(health75, '0')

                    press_and_release(key_mapping['numpad4'])

                # Adjust sleep for minimal delay without excessive CPU usage
                time.sleep(0.05)
    except Exception as e:
        print(f"An error occurred during tank rotation: {e}")

def run(stop_event):
    tank_rotation(stop_event)
