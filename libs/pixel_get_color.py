from PIL import ImageGrab

def get_color(x, y):
    return ImageGrab.grab().getpixel((x, y))
