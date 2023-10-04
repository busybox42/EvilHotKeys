import keyboard
# Define a dictionary for key mappings
key_mapping = {
    'numpad0': 82,
    'numpad1': 79,
    'numpad2': 80,
    'numpad3': 81,
    'numpad4': 75,
    'numpad5': 76,
    'numpad6': 77,
    'numpad7': 71,
    'numpad8': 72,
    'numpad9': 73,
    'numpad+': 78,  # Plus key on the numpad
    'numpad-': 74,  # Minus key on the numpad
    'f1': 59,
    'f2': 60,
    'f3': 61,
    'f4': 62,
    'f5': 63,
    'f6': 64,
    'f7': 65,
    'f8': 66,
    'f9': 67,
    'f10': 68,
    'f11': 87,
    'f12': 88,
}

# Function to press and release keys using the mapping
def press_and_release_mapped(key_name):
    if key_name in key_mapping:
        key_code = key_mapping[key_name]
        keyboard.press(key_code)
        keyboard.release(key_code)