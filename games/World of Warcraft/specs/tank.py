from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release
from libs.key_mapping import key_mapping
from PIL import ImageGrab
import time
import keyboard

# Constants
DEFAULT_COLOR = (0, 0, 0)

# Helper function for pixel actions
def handle_pixel_action(condition_color, key):
    if condition_color != DEFAULT_COLOR:
        press_and_release(key)

# Tank rotation logic
def tank_rotation(stop_event):
    try:
        while not stop_event.is_set():
            # Use an event-driven approach to detect key presses
            if keyboard.is_pressed(key_mapping['numpad4']):
                # Grab the entire screen region once
                screen_image = ImageGrab.grab()

                # Extract relevant pixel colors from the cached screen image
                interrupt = screen_image.getpixel((2345, 875))
                healerhealth = screen_image.getpixel((2345, 920))
                health50 = screen_image.getpixel((2375, 995))
                health35 = screen_image.getpixel((2405, 995))
                health25 = screen_image.getpixel((2440, 995))  
                health75 = screen_image.getpixel((2345, 995))

                # Handle actions based on pixel colors
                handle_pixel_action(interrupt, '=')
                handle_pixel_action(healerhealth, '5')
                handle_pixel_action(health50, '4')
                handle_pixel_action(health35, '5')
                handle_pixel_action(health25, '3')
                handle_pixel_action(health75, '0')

                # Repeat pressing numpad4 key after all actions
                press_and_release(key_mapping['numpad4'])
                
                time.sleep(0.2)

    except Exception as e:
        print(f"An error occurred during tank rotation: {e}")

# Main run function
def run(stop_event):
    while not stop_event.is_set():
        tank_rotation(stop_event)
        time.sleep(0.1)
