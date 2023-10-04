import keyboard

# Tool to spy on the keyboard events
def print_event(e):
    print(e.name, e.scan_code, e.time)
# Hook the print_event function to the keyboard events
keyboard.hook(print_event)
# Wait for the 'esc' key to be pressed
keyboard.wait('esc')