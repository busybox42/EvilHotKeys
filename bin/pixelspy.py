import pyautogui

# Tool to spy on the pixel color at the current cursor position
while True:
    # Get the current position of the cursor
    x, y = pyautogui.position()

    # Get the color of the pixel at the cursor position
    pixel_color = pyautogui.pixel(x, y)

    # Convert the color values to RGB format
    rgb_color = (pixel_color[0], pixel_color[1], pixel_color[2])

    # Print the cursor position and color
    print(f"Cursor Position: ({x}, {y})")
    print(f"Pixel Color (RGB): {rgb_color}")
    
    # Add a delay to prevent excessive CPU usage
    pyautogui.sleep(1)  
