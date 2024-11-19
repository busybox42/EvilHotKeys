from PIL import ImageGrab

# Define a function to get the color of a pixel at the specified coordinates
def get_color(x, y, img=None):
    try:
        if img is None:
            # Grab the screen if no image is provided
            img = ImageGrab.grab()
        return img.getpixel((x, y))
    except Exception as e:
        print(f"Error getting pixel color at ({x}, {y}): {e}")
        return None

# Example of how to reuse the image if you need multiple pixel colors in one run
def get_multiple_pixel_colors(coordinates):
    img = ImageGrab.grab()
    colors = []
    for (x, y) in coordinates:
        color = get_color(x, y, img)
        if color is not None:
            colors.append(color)
    return colors
