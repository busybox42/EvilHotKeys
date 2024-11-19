import threading
import keyboard
import time

# Event to manage pause state
pause_event = threading.Event()

# Function to toggle the pause state
def toggle_pause():
    if pause_event.is_set():
        print("Script unpaused")
        pause_event.clear()
    else:
        print("Script paused")
        pause_event.set()

# Function to manage pausing based on the event
def pause():
    keyboard.add_hotkey('end', toggle_pause)

    # Keep the thread alive while listening for pause events
    while True:
        time.sleep(1)

# Start the pause thread
pause_thread = threading.Thread(target=pause, daemon=True)
pause_thread.start()
