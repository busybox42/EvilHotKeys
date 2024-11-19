from PIL import ImageGrab
import numpy as np

# Define a function to search for a pixel of a specific color in a region of the screen
def pixel_search(color, x1, y1, x2, y2):
    try:
        # Use the ImageGrab module to grab a screenshot of the specified region
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # Convert the image to a numpy array for faster processing
        image_np = np.array(image)

        # Iterate over the array to find matching pixels
        for y in range(image_np.shape[0]):
            for x in range(image_np.shape[1]):
                if tuple(image_np[y, x]) == color:
                    # Return the coordinates of the found pixel
                    return (x1 + x, y1 + y)
        
        # If no matching pixel is found, return None
        return None
    except Exception as e:
        print(f"Error during pixel search: {e}")
        return None
