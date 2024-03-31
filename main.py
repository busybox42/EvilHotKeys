import signal
import sys
import threading
import time
import os
from importlib import import_module

# Function to run the spec
def run_spec(selected_game, selected_spec, stop_event):
    spec_module = import_module(f'games.{selected_game}.specs.{selected_spec}')
    spec_module.run(stop_event)

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C! Exiting gracefully.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

last_selected_game = None

while True:
    games = [f for f in next(os.walk('./games'))[1] if not f.startswith('__')]
    print("Welcome to EvilHotKeys!")
    print("Available games:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game}")

    selected_game_index = int(input("Select a game: ")) - 1

    if selected_game_index < 0 or selected_game_index >= len(games):
        print("Invalid game selection. Please try again.")
        continue

    selected_game = games[selected_game_index]

    spec_path = f'./games/{selected_game}/specs'
    specs = [f[:-3] for f in os.listdir(spec_path) if f.endswith('.py') and not f.startswith('__')]

    if not specs:
        print(f"No specs found for {selected_game}.")
        continue

    print("Available specs for " + selected_game + ":")
    for i, spec in enumerate(specs, 1):
        print(f"{i}. {spec}")

    selected_spec_index = int(input("Select a spec: ")) - 1

    if selected_spec_index < 0 or selected_spec_index >= len(specs):
        print("Invalid spec selection. Please try again.")
        continue

    selected_spec = specs[selected_spec_index]

    stop_event = threading.Event()
    spec_thread = threading.Thread(target=run_spec, args=(selected_game, selected_spec, stop_event))
    spec_thread.start()

    while spec_thread.is_alive():
        key = input("Press 'q' to return to the spec selection menu: ")
        if key.lower() == 'q':  
            print("Stopping the running spec. Please wait...")
            last_selected_game = selected_game
            stop_event.set()
            spec_thread.join(timeout=5)  
            if spec_thread.is_alive():
                print("The spec did not terminate as expected. You may experience some delay.")
            else:
                print("Spec stopped successfully.")
            break

    if last_selected_game:
        print(f"Returning to specs of {last_selected_game}.\n")
    else:
        print("No previous game selection. Exiting.\n")
        break
