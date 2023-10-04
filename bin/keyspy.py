import keyboard

def print_event(e):
    print(e.name, e.scan_code, e.time)

keyboard.hook(print_event)
keyboard.wait('esc')