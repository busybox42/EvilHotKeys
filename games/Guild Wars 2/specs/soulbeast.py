import time
import keyboard
from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions import press, release, press_and_release, button_mash
from libs.key_mapping import key_mapping

def check_stop_condition(stop_event):
    """Check if we should stop the rotation"""
    return not keyboard.is_pressed(key_mapping['numpad1']) or stop_event.is_set()

def execute_opener(stop_event):
    """Execute the optimal opener sequence"""
    # One Wolf Pack
    button_mash(key_mapping['numpad0'], stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Frost Trap
    button_mash(key_mapping['numpad9'], stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Brutal Charge
    button_mash('2', stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # "Sic 'Em!" during the cast
    button_mash(key_mapping['numpad8'], stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Maul
    button_mash('1', stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Unleashed Savage Shock Wave
    button_mash(key_mapping['numpad4'], stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Unleashed Wild Swing
    button_mash(key_mapping['numpad2'], stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Weapon swap
    button_mash(key_mapping['f1'], stop_check=lambda: check_stop_condition(stop_event))
    time.sleep(0.1)
    
    return True

def simple_rotation(stop_event):
    """Execute a simple ability loop based on what's available"""
    while not stop_event.is_set():
        if check_stop_condition(stop_event):
            break
        
        # Check if we're in Hammer or Axe mode
        is_hammer = pixel_get_color(2585, 1021) != (0, 0, 0)
        
        # Get merge state
        merged = pixel_get_color(2595, 970) != (112, 112, 112)
        
        # Check available abilities
        if merged:
            # If not merged, merge with pet
            button_mash('5', stop_check=lambda: check_stop_condition(stop_event))
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
        
        # Utility skills (same in both weapon sets)
        wolf_pack = pixel_get_color(3174, 1015) != (0, 0, 0)
        frost_trap = pixel_get_color(3121, 1015) != (0, 0, 0)
        sic_em = pixel_get_color(3064, 1015) != (0, 0, 0)
        
        # Use utility skills if available
        if wolf_pack:
            if not button_mash(key_mapping['numpad0'], stop_check=lambda: check_stop_condition(stop_event)): break
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
            
        if frost_trap:
            if not button_mash(key_mapping['numpad9'], stop_check=lambda: check_stop_condition(stop_event)): break
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
            
        if sic_em:
            if not button_mash(key_mapping['numpad8'], stop_check=lambda: check_stop_condition(stop_event)): break
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
            
        # Class mechanic (Worldly Impact)
        worldly = pixel_get_color(2695, 944) != (0, 0, 0)
        if worldly:
            if not button_mash('2', stop_check=lambda: check_stop_condition(stop_event)): break
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
            
        # Profession skill (Maul)
        maul = pixel_get_color(2645, 944) != (0, 0, 0)
        if maul:
            if not button_mash('1', stop_check=lambda: check_stop_condition(stop_event)): break
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
        
        # Weapon skills based on current weapon set
        if is_hammer:
            # Hammer skills
            overbearing_smash = pixel_get_color(2690, 1015) != (0, 0, 0)
            savage_shock_wave = pixel_get_color(2745, 1015) != (0, 0, 0)
            wild_swing = pixel_get_color(2634, 1015) != (0, 0, 0)
            unleashed_thump = pixel_get_color(2800, 1015) != (0, 0, 0)
            
            # Use available hammer skills
            if overbearing_smash:
                if not button_mash(key_mapping['numpad3'], stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
                
            if savage_shock_wave:
                if not button_mash(key_mapping['numpad4'], stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
                
            if wild_swing:
                if not button_mash(key_mapping['numpad2'], stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
                
            if unleashed_thump:
                if not button_mash(key_mapping['numpad5'], stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
        else:
            # Axe skills
            path_scars = pixel_get_color(2745, 1015) != (0, 0, 0)
            winter_bite = pixel_get_color(2690, 1015) != (0, 0, 0)
            splitblade = pixel_get_color(2634, 1015) != (0, 0, 0)
            whirling = pixel_get_color(2800, 1015) != (0, 0, 0)
            
            # Use available axe skills (use 3 presses for better reliability)
            if path_scars:
                if not button_mash(key_mapping['numpad4'], 3, stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
                
            if winter_bite:
                if not button_mash(key_mapping['numpad3'], 3, stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
                
            if splitblade:
                if not button_mash(key_mapping['numpad2'], 3, stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
                
            if whirling:
                if not button_mash(key_mapping['numpad5'], 3, stop_check=lambda: check_stop_condition(stop_event)): break
                time.sleep(0.1)
                if check_stop_condition(stop_event): break
        
        # If no skills were available or after using skills, use auto-attack
        if not button_mash(key_mapping['numpad1'], stop_check=lambda: check_stop_condition(stop_event)): break
        
        # Check for weapon swap after a full cycle
        weapon_swap = pixel_get_color(2530, 1010) != (0, 0, 0)
        
        # Try to swap weapons if cooldown is ready and we've used most abilities
        if weapon_swap:
            if not button_mash(key_mapping['f1'], stop_check=lambda: check_stop_condition(stop_event)): break
            time.sleep(0.1)
            if check_stop_condition(stop_event): break
        
        # Small pause before next iteration
        time.sleep(0.1)

def run(stop_event):
    opener_executed = False
    
    while not stop_event.is_set():
        # Check for Ctrl+Numpad1 for opener
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed(key_mapping['numpad1']) and not opener_executed:
            # Execute opener sequence
            if execute_opener(stop_event):
                opener_executed = True  # Mark opener as executed
                time.sleep(0.5)  # Small delay before starting rotation
        # Normal rotation with just Numpad1
        elif keyboard.is_pressed(key_mapping['numpad1']) and not keyboard.is_pressed('ctrl'):  
            opener_executed = False  # Reset opener flag when only numpad1 is pressed
            simple_rotation(stop_event)  # Use the simplified rotation
        # Reset opener flag when nothing is pressed
        elif not keyboard.is_pressed(key_mapping['numpad1']):
            opener_executed = False
        
        time.sleep(0.1)
