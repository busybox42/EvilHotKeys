from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def healing_mechanist_rotation():
    while True:  # You'll control this loop from your main program
        if not keyboard.is_pressed(key_mapping['numpad1']):
            break
        press(key_mapping['numpad1'])
        release(key_mapping['numpad1'])
        press_and_release('1')
        press_and_release('2')
        press_and_release('3')
        time.sleep(0.5)
        
        if pixel_search((255, 255, 255), 2170, 2045, 2205, 2080):
            if pixel_get_color(1644, 2022) != (0, 0, 0):
                press(key_mapping['numpad4']) # Acid Bomb
                release(key_mapping['numpad4'])
                time.sleep(0.5)
                press(key_mapping['f1']) # Weapon Swap
                release(key_mapping['f1'])
                continue
            
            if pixel_get_color(1755, 2026) != (0, 0, 0):
                press(key_mapping['numpad5']) # Super Elixir
                release(key_mapping['numpad5'])
                time.sleep(0.5)
                continue
            
            press(key_mapping['numpad0']) # Switch to Mortar
            release(key_mapping['numpad0'])
            time.sleep(1)
        
        elif pixel_search((255, 255, 255), 2500, 2055, 2530, 2080):
            if pixel_get_color(1755, 2026) != (0, 0, 0):
                press(key_mapping['numpad5']) # Elixir Shell
                release(key_mapping['numpad5'])
            else:
                press(key_mapping['numpad6']) # Switch to MedKit
                release(key_mapping['numpad6'])
            time.sleep(1)
        
        elif pixel_search((255, 255, 255), 2055, 2045, 2095, 2080):
            if pixel_get_color(1755, 2026) != (0, 0, 0):
                press(key_mapping['numpad5']) # Infusion Bomb
                release(key_mapping['numpad5'])
            else:
                press(key_mapping['f1']) # Weapon Swap
                release(key_mapping['f1'])
            time.sleep(1)
        
        else:
            if pixel_get_color(1644, 2022) != (0, 0, 0):
                press(key_mapping['numpad4']) # Magnetic Shield
                release(key_mapping['numpad4'])
            elif pixel_get_color(1755, 2026) != (0, 0, 0):
                press(key_mapping['numpad5']) # Static Shield
                release(key_mapping['numpad5'])
                press(key_mapping['numpad2']) # Energizing Slam
                release(key_mapping['numpad2'])
            else:
                press(key_mapping['numpad7']) # Switch to Elixir Gun
                release(key_mapping['numpad7'])
            time.sleep(1)
        
        press(key_mapping['numpad8'])
        release(key_mapping['numpad8'])
        time.sleep(0.5)

def run(stop_event):
    while not stop_event.is_set():
        while True:  # Main loop
            if keyboard.is_pressed(key_mapping['numpad1']):  
                healing_mechanist_rotation()  
            time.sleep(0.1) 
