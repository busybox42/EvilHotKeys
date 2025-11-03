"""
Power Amalgam PvP Build for Guild Wars 2
Based on: https://guildjen.com/power-amalgam-pvp-build/

Build Overview:
- Weapon: Mace/Shield
- Rotation: Solid State > Mace 2 > Shield 4 > Shield 3 > Demolish
- Key Skills: Offensive Protocol, Defense Protocol, Flamethrower Kit
- Focus: Survivability, crowd control, burst damage
"""

import time
import keyboard
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions_monitored import press_and_release
from libs.key_mapping import key_mapping
from libs.logger import get_logger

logger = get_logger('power_amalgam')

# Default coordinates for a 1920x1080 display
# TODO: Update these coordinates using the coordinate_helper.py tool
DEFAULT_COORDS = {
    # Utility skills (row of 5 skills at bottom of screen)
    'utility_1': (2652, 1013),  # Heal skill
    'utility_2': (3007, 1013),  # Utility 1
    'utility_3': (3070, 1034),  # Utility 2 (Flamethrower Kit)
    'utility_4': (3116, 1013),  # Utility 3
    'utility_5': (3178, 1013),  # Elite
    # Protocol skills (F-keys)
    'protocol_1': (2607, 950),  # Offensive Protocol
    'protocol_2': (2650, 950),  # Defense Protocol
    'protocol_3': (2693, 950),  # Support Protocol
    'protocol_4': (2739, 950),  # Protocol 4
    'protocol_5': (2787, 950),  # Elevate (Protocol 5)
    
    # Weapon skills
    'weapon_2': (2635, 1013),  # Mace 2
    'weapon_3': (2686, 1013),  # Mace 3
    
    # Shield skills
    'weapon_4': (2743, 1013),  # Shield 4
    'weapon_5': (2799, 1013),  # Shield 5
}

def check_stop_condition(stop_event):
    """Check if we should stop the rotation"""
    return not keyboard.is_pressed(key_mapping['numpad1']) or stop_event.is_set()

def check_skill_available(coords):
    """Check if a skill is available (not on cooldown)"""
    color = pixel_get_color(coords[0], coords[1])
    # Skills ready have a brighter color, on cooldown are dark/gray
    return color is not None and color != (0, 0, 0) and sum(color) > 300

def execute_opener_burst(stop_event):
    """
    Execute the opener burst combo:
    Solid State > Mace 2 > Shield 4 > Shield 3 > Demolish
    """
    logger.info("Executing opener burst combo")
    
    # Use Offensive Protocol: Solid State (numpad7 on bottom bar)
    if check_skill_available(DEFAULT_COORDS['protocol_1']):
        logger.info("Using Offensive Protocol: Solid State")
        press_and_release(key_mapping['numpad7'])  # Bottom bar numpad
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    # Mace 2 - Brutal Leap (numpad2 = bottom bar slot 2)
    if check_skill_available(DEFAULT_COORDS['weapon_2']):
        logger.info("Using Mace 2: Brutal Leap")
        press_and_release(key_mapping['numpad2'])
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    # Shield 4 - Shield Smack (numpad4 = bottom bar slot 4)
    if check_skill_available(DEFAULT_COORDS['weapon_4']):
        logger.info("Using Shield 4: Shield Smack")
        press_and_release(key_mapping['numpad4'])
        time.sleep(0.2)
        if check_stop_condition(stop_event): return False
    
    # Shield 5 (numpad5 = bottom bar slot 5)
    if check_skill_available(DEFAULT_COORDS['weapon_5']):
        logger.info("Using Shield 5")
        press_and_release(key_mapping['numpad5'])
        time.sleep(0.2)
        if check_stop_condition(stop_event): return False
    
    # Finish with Demolish (Mace 3) (numpad3 = bottom bar slot 3)
    if check_skill_available(DEFAULT_COORDS['weapon_3']):
        logger.info("Using Demolish (Mace 3)")
        press_and_release(key_mapping['numpad3'])
        time.sleep(0.2)
    
    return True

def power_amalgam_rotation(stop_event):
    """
    Main rotation loop for Power Amalgam PvP
    """
    loop_count = 0
    last_protocol_use = {'2': 0, '3': 0, '4': 0, '5': 0}  # Track last protocol use
    
    while not stop_event.is_set():
        loop_count += 1
        current_time = time.time()
        
        # Log every 50 loops to show it's running
        if loop_count % 50 == 0:
            logger.info(f"Rotation running, loop {loop_count}")
        
        # Check stop condition frequently
        if check_stop_condition(stop_event):
            logger.info("Stop condition detected")
            break
        
        # Priority 1: Check if burst combo skills are ready
        protocol_1_ready = check_skill_available(DEFAULT_COORDS['protocol_1'])
        protocol_2_ready = check_skill_available(DEFAULT_COORDS['protocol_2'])
        protocol_3_ready = check_skill_available(DEFAULT_COORDS['protocol_3'])
        protocol_4_ready = check_skill_available(DEFAULT_COORDS['protocol_4'])
        protocol_5_ready = check_skill_available(DEFAULT_COORDS['protocol_5'])
        mace_2_ready = check_skill_available(DEFAULT_COORDS['weapon_2'])
        shield_4_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
        mace_3_ready = check_skill_available(DEFAULT_COORDS['weapon_3'])
        
        # Execute burst combo when key skills are off cooldown (HIGHEST PRIORITY)
        if protocol_1_ready and mace_2_ready and shield_4_ready:
            logger.info("Executing burst opener - skills ready")
            execute_opener_burst(stop_event)
            if check_stop_condition(stop_event): break
            continue
        
        # Use protocol 2/3 ONLY if haven't used in last 5 seconds AND ready
        if protocol_2_ready and (current_time - last_protocol_use['2'] > 5.0):
            logger.info("Using Protocol 2 (key 2)")
            press_and_release('2')
            last_protocol_use['2'] = current_time
            time.sleep(0.3)
            if check_stop_condition(stop_event): break
            continue
        
        if protocol_3_ready and (current_time - last_protocol_use['3'] > 5.0):
            logger.info("Using Protocol 3 (key 3)")
            press_and_release('3')
            last_protocol_use['3'] = current_time
            time.sleep(0.3)
            if check_stop_condition(stop_event): break
            continue
        
        # Priority 2: Check for Mace 2 or Shield 4 individually if off cooldown
        if mace_2_ready:
            logger.info("Using Mace 2: Brutal Leap")
            press_and_release(key_mapping['numpad2'])
            time.sleep(0.3)
            if check_stop_condition(stop_event): break
            continue
        
        if shield_4_ready:
            logger.info("Using Shield 4: Shield Smack")
            press_and_release(key_mapping['numpad4'])
            time.sleep(0.2)
            if check_stop_condition(stop_event): break
            continue
        
        # Priority 3: Use Mace 3 (Demolish) if ready
        if mace_3_ready:
            logger.info("Using Demolish (Mace 3)")
            press_and_release(key_mapping['numpad3'])
            time.sleep(0.2)
            if check_stop_condition(stop_event): break
            continue
        
        # Priority 4: Small sleep, then retry (no auto-attack spam)
        # Mace 1 is removed from rotation to avoid triggering F1-F5
        time.sleep(0.1)

def run(stop_event):
    """
    Main entry point for Power Amalgam spec
    Hold numpad1 to activate the rotation
    """
    logger.info("Power Amalgam PvP spec started")
    logger.info("Hold numpad1 to activate rotation")
    
    while not stop_event.is_set():
        # Check stop event first
        if stop_event.is_set():
            logger.info("Stop event detected")
            break
        
        # Activate rotation when numpad1 is pressed
        if keyboard.is_pressed(key_mapping['numpad1']):
            power_amalgam_rotation(stop_event)
        
        # Always sleep to prevent busy-waiting
        time.sleep(0.05)
    
    logger.info("Power Amalgam PvP spec ended")

