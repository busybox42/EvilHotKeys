import signal
import sys
import threading
import time
import os
from importlib import import_module
from libs.menu_customization import customize_menu, customize_specs
import tkinter as tk
from tkinter import ttk, messagebox
import pystray
from PIL import Image
import ctypes

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

# GUI Application Class
class SpecRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EvilHotKeys GUI")
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.stop_event = threading.Event()

        # Game Selection
        self.game_label = ttk.Label(root, text="Select a Game:")
        self.game_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.game_combo = ttk.Combobox(root, state="readonly")
        self.game_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.game_combo.bind("<<ComboboxSelected>>", self.load_specs)

        # Spec Selection
        self.spec_label = ttk.Label(root, text="Select a Spec:")
        self.spec_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.spec_combo = ttk.Combobox(root, state="readonly")
        self.spec_combo.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Run Button
        self.run_button = ttk.Button(root, text="Run Spec", command=self.run_selected_spec)
        self.run_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Stop Button
        self.stop_button = ttk.Button(root, text="Stop Spec", command=self.stop_spec, state='disabled')
        self.stop_button.grid(row=3, column=0, columnspan=2, pady=10)

        # System Tray Icon
        self.icon_image = Image.new('RGB', (64, 64), color=(255, 0, 0))
        self.tray_icon = pystray.Icon("SpecRunner", self.icon_image, menu=pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.on_close)
        ))

        # Load games initially
        self.load_games()

    def load_games(self):
        games = customize_menu('./games')
        if games:
            self.game_combo['values'] = games
        else:
            messagebox.showerror("Error", "No games available.")

    def load_specs(self, event):
        selected_game = self.game_combo.get()
        if not selected_game:
            return

        spec_path = os.path.join('./games', selected_game, 'specs')
        specs = [f[:-3] for f in os.listdir(spec_path) if f.endswith('.py') and not f.startswith('__')]

        if selected_game == 'World of Warcraft':
            specs = customize_specs(specs)

        if specs:
            self.spec_combo['values'] = specs
        else:
            self.spec_combo['values'] = []
            messagebox.showerror("Error", f"No specs found for {selected_game}.")

    def run_selected_spec(self):
        selected_game = self.game_combo.get()
        selected_spec = self.spec_combo.get()

        if not selected_game or not selected_spec:
            messagebox.showwarning("Warning", "Please select both a game and a spec.")
            return

        self.stop_event.clear()
        self.run_button.config(state='disabled')
        self.stop_button.config(state='normal')

        self.spec_thread = threading.Thread(target=run_spec, args=(selected_game, selected_spec, self.stop_event))
        self.spec_thread.start()

    def stop_spec(self):
        self.stop_event.set()
        self.run_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
        if self.spec_thread.is_alive():
            self.spec_thread.join(timeout=5)
            if self.spec_thread.is_alive():
                print("The spec did not terminate as expected. You may experience some delay.")
            else:
                print("Spec stopped successfully.")

    def on_close(self):
        self.stop_event.set()
        if hasattr(self, 'spec_thread') and self.spec_thread.is_alive():
            self.spec_thread.join(timeout=5)
        self.tray_icon.stop()
        self.root.destroy()

    def on_minimize(self, event):
        if self.root.state() == 'iconic':
            self.root.withdraw()
            self.tray_icon.run_detached()

    def show_window(self):
        self.root.deiconify()
        self.root.state('normal')
        self.tray_icon.stop()

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C! Exiting gracefully.')
    stop_event.set()  # Ensure any running spec is stopped
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Main function to start the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SpecRunnerApp(root)
    root.mainloop()

