import signal
import sys
import threading
import time
import os
from importlib import import_module
import keyboard  # For non-blocking user input

# Function to run the spec
def run_spec(selected_game, selected_spec, stop_event):
    try:
        spec_module = import_module(f'games.{selected_game}.specs.{selected_spec}')
        spec_module.run(stop_event)
    except ModuleNotFoundError:
        print(f"Failed to load spec '{selected_spec}' for game '{selected_game}'.")

# Function to select a game
def select_game():
    games = [f for f in next(os.walk('./games'))[1] if not f.startswith('__')]
    if not games:
        print("No games available.")
        return None

    print("Available games:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game}")

    try:
        selected_index = int(input("Select a game: ")) - 1
        if selected_index < 0 or selected_index >= len(games):
            print("Invalid game selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    return games[selected_index]

# Function to select a spec
def select_spec(selected_game):
    spec_path = os.path.join('./games', selected_game, 'specs')
    specs = [f[:-3] for f in os.listdir(spec_path) if f.endswith('.py') and not f.startswith('__')]

    if not specs:
        print(f"No specs found for {selected_game}.")
        return None

    print("Available specs:")
    for i, spec in enumerate(specs, 1):
        print(f"{i}. {spec}")

    try:
        selected_index = int(input("Select a spec: ")) - 1
        if selected_index < 0 or selected_index >= len(specs):
            print("Invalid spec selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    return specs[selected_index]

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C! Exiting gracefully.')
    stop_event.set()  # Ensure any running spec is stopped
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

stop_event = threading.Event()

# Main loop
while True:
    selected_game = select_game()
    if not selected_game:
        continue

    selected_spec = select_spec(selected_game)
    if not selected_spec:
        continue

    stop_event.clear()
    spec_thread = threading.Thread(target=run_spec, args=(selected_game, selected_spec, stop_event))
    spec_thread.start()

    # Wait for user to stop the running spec
    while spec_thread.is_alive():
        if keyboard.is_pressed('q'):
            print("Stopping the running spec. Please wait...")
            stop_event.set()
            spec_thread.join(timeout=5)
            if spec_thread.is_alive():
                print("The spec did not terminate as expected. You may experience some delay.")
            else:
                print("Spec stopped successfully.")
            break

    print(f"Returning to specs of {selected_game}.")
