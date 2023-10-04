import time
import os
import sys
import threading
from importlib import import_module

# Function to run the spec
def run_spec(selected_game, selected_spec, stop_event):
    spec_module = import_module(f'games.{selected_game}.specs.{selected_spec}')
    spec_module.run(stop_event)


last_selected_game = None  # Initialize last_selected_game to None

while True:
    try:
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

        # Create a stop event to signal the spec to stop running
        stop_event = threading.Event()

        # Create a thread to run the selected spec
        spec_thread = threading.Thread(target=run_spec, args=(selected_game, selected_spec, stop_event))
        spec_thread.start()

        # Listen for a key press to return to the spec selection menu
        while spec_thread.is_alive():
            try:
                key = input("Press 'q' to return to the spec selection menu: ")
                if key == 'q':
                    last_selected_game = selected_game  # Store the last selected game
                    stop_event.set()  # Set the stop event to stop the spec
                    break
            except KeyboardInterrupt:
                print("\nExiting.")
                stop_event.set()  # Set the stop event to stop the spec
                sys.exit()

        # When 'q' is pressed, it takes you back to the specs of the last selected game
        if last_selected_game:
            print(f"Returning to specs of {last_selected_game}.\n")
        else:
            print("No previous game selection. Exiting.\n")
            break
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit()