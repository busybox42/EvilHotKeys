from PIL import ImageGrab

# Define a function to search for a pixel of a specific color in a region of the screen
def pixel_search(color, x1, y1, x2, y2):
    # Use the ImageGrab module to grab a screenshot of the specified region
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    # Check if any pixel in the screenshot matches the specified color
    return any(image.getpixel((x, y)) == color for y in range(image.size[1]) for x in range(image.size[0]))