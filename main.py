import signal
import sys
import threading
import time
import os
from importlib import import_module
from libs.menu_customization import customize_menu, customize_specs

# Function to run the spec
def run_spec(selected_game, selected_spec, stop_event):
    try:
        print(f"Running spec '{selected_spec}' for game '{selected_game}'.")

        # Import and run the spec
        spec_module = import_module(f'games.{selected_game}.specs.{selected_spec}')
        if hasattr(spec_module, 'run'):
            spec_module.run(stop_event)
        else:
            print(f"Spec '{selected_spec}' for game '{selected_game}' does not have a 'run' function or is incorrectly defined.")

    except ModuleNotFoundError as e:
        print(f"Failed to load spec '{selected_spec}' for game '{selected_game}'. Error: {e}")
    except AttributeError as e:
        print(f"Spec '{selected_spec}' for game '{selected_game}' encountered an AttributeError. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while running spec '{selected_spec}' for game '{selected_game}': {e}")

# Function to select a game
def select_game():
    games = customize_menu('./games')
    if not games:
        print("No games available.")
        return None

    print("Available games:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game}")

    while True:
        try:
            selected_index = int(input("Select a game: ")) - 1
            if 0 <= selected_index < len(games):
                return games[selected_index]
            else:
                print("Invalid game selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to select a spec
def select_spec(selected_game):
    spec_path = os.path.join('./games', selected_game, 'specs')
    specs = [f[:-3] for f in os.listdir(spec_path) if f.endswith('.py') and not f.startswith('__')]

    if selected_game == 'World of Warcraft':
        specs = customize_specs(specs)

    if not specs:
        print(f"No specs found for {selected_game}.")
        return None

    print("Available specs:")
    for i, spec in enumerate(specs, 1):
        print(f"{i}. {spec}")

    while True:
        try:
            selected_index = int(input("Select a spec: ")) - 1
            if 0 <= selected_index < len(specs):
                return specs[selected_index]
            else:
                print("Invalid spec selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

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

    while True:
        selected_spec = select_spec(selected_game)
        if selected_spec is None:
            print("Returning to game selection.")
            break

        stop_event.clear()
        spec_thread = threading.Thread(target=run_spec, args=(selected_game, selected_spec, stop_event))
        spec_thread.start()

        # Wait for user to stop the running spec manually using Ctrl+C
        while spec_thread.is_alive():
            time.sleep(0.05)  # Add a slight delay to avoid busy-waiting

            if stop_event.is_set():
                spec_thread.join(timeout=5)
                if spec_thread.is_alive():
                    print("The spec did not terminate as expected. You may experience some delay.")
                else:
                    print("Spec stopped successfully.")
                break

        print("Returning to spec selection.")
