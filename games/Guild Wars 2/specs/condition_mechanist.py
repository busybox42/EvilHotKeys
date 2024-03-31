from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press_and_release, press, release
from libs.key_mapping import key_mapping
import time
import keyboard

def condition_mechanist_rotation(stop_event):
    while not stop_event.is_set():  
        if not keyboard.is_pressed(key_mapping['numpad1']) or stop_event.is_set():
            break
        
        press_and_release('2')
        press_and_release('1')
        press_and_release('3')
        
        if pixel_search((255, 255, 255), 2170, 2045, 2205, 2080):  # Grenade Kit
            sg = pixel_get_color(1425, 2025)
            pg = pixel_get_color(1755, 2026)
            signet = pixel_get_color(2285, 2026)
            fg = pixel_get_color(1644, 2022)
            
            if sg != (0, 0, 0):
                press(key_mapping['numpad2'])
                release(key_mapping['numpad2'])
                time.sleep(0.5)
                
            if pg != (0, 0, 0):
                press(key_mapping['numpad5'])
                release(key_mapping['numpad5'])
                time.sleep(0.5)
            
            if signet != (0, 0, 0):
                press(key_mapping['numpad8'])
                release(key_mapping['numpad8'])
                time.sleep(0.5)
            
            if fg != (0, 0, 0):
                press(key_mapping['numpad4'])
                release(key_mapping['numpad4'])
                time.sleep(0.5)
            
            if sg == (0, 0, 0) and pg == (0, 0, 0) and fg == (0, 0, 0):
                press(key_mapping['f1'])
                release(key_mapping['f1'])

            press(key_mapping['numpad1'])
            release(key_mapping['numpad1'])
        
        else:
            pdv = pixel_get_color(1425, 2025)
            bt = pixel_get_color(1644, 2022)
            ss = pixel_get_color(1530, 2025)
            
            if pdv != (0, 0, 0):
                press(key_mapping['numpad2'])
                release(key_mapping['numpad2'])
                time.sleep(0.5)
            
            if bt != (0, 0, 0):
                press(key_mapping['numpad4'])
                release(key_mapping['numpad4'])
                time.sleep(0.5)
            
            if ss != (0, 0, 0):
                press(key_mapping['numpad3'])
                release(key_mapping['numpad3'])
                time.sleep(0.5)
            
            if pdv == (0, 0, 0) and bt == (0, 0, 0) and ss == (0, 0, 0):
                press(key_mapping['numpad7'])
                release(key_mapping['numpad7'])
            
            press(key_mapping['numpad1'])
            release(key_mapping['numpad1'])

def run(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed(key_mapping['numpad1']):
            condition_mechanist_rotation(stop_event)  
        time.sleep(0.1)  
