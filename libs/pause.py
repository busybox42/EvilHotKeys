import threading
import keyboard
import time

# Define a global flag to pause the script
pause_flag = False

def pause():
    global pause_flag
    pause_state = False
    while True:
        if keyboard.is_pressed('end'):
            pause_flag = not pause_flag
            if pause_flag != pause_state:
                pause_state = pause_flag
                if pause_flag:
                    print('Script paused')
                else:
                    print('Script unpaused')
            time.sleep(0.05)

# Start the pause thread
pause_thread = threading.Thread(target=pause, daemon=True)
pause_thread.start()