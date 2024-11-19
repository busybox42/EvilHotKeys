import pyautogui
import time
import threading
import keyboard

# Tool to spy on the pixel color at the current cursor position
def pixel_spy():
    prev_x, prev_y = None, None
    try:
        while True:
            # Get the current position of the cursor
            x, y = pyautogui.position()

            # Only fetch the color and print if the cursor has moved
            if (x, y) != (prev_x, prev_y):
                # Get the color of the pixel at the cursor position
                pixel_color = pyautogui.pixel(x, y)

                # Print the cursor position and color
                print(f"Cursor Position: ({x}, {y}) - Pixel Color (RGB): {pixel_color}")

                # Update previous coordinates
                prev_x, prev_y = x, y

            # Add a delay to prevent excessive CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting pixel spy gracefully.")

# Function to monitor for exit key
def exit_listener():
    keyboard.wait('esc')
    print("\nExit key pressed. Stopping pixel spy.")
    # Exit the program
    raise KeyboardInterrupt

# Start the pixel spy in a separate thread
pixel_spy_thread = threading.Thread(target=pixel_spy, daemon=True)
pixel_spy_thread.start()

# Start the exit listener in the main thread
exit_listener()
