from PIL import ImageGrab

# Define a function to get the color of a pixel at the specified coordinates
def get_color(x, y):
    # Use the ImageGrab module to grab a screenshot and get the pixel color at the specified coordinates
    return ImageGrab.grab().getpixel((x, y))