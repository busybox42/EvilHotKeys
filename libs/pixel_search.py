from PIL import ImageGrab

def pixel_search(color, x1, y1, x2, y2):
    image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    return any(image.getpixel((x, y)) == color for y in range(image.size[1]) for x in range(image.size[0]))
