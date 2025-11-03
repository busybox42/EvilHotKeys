"""
Power Amalgam (WvW) - WvW Build for Guild Wars 2
Based on: https://snowcrows.com/builds/wvw/engineer/power-amalgam

Build Overview:
- Weapon: Hammer (both sets)
- Utilities: Elixir Gun Kit, Flamethrower Kit
- Rotation: Evolve > Morphs (Obliterate + Thorns) > Evolve reset > Second Morph burst
- Focus: Strong spikes for generating downs, cleave, sustained damage
- Playstyle: Similar to Power Holosmith with rarer, stronger damage sources

Key Concepts:
- Evolve (F5) resets all morph skills and grants periodic stat boost
- Pair Evolve with squad spike timing (e.g., Well of Corruption)
- Offensive Protocol: Obliterate (F4) grants damage increase (Strain)
- Defensive Protocol: Thorns grants additional hits (Strain)

Your Keybinds:
Toolbelt (F1-F5): keys 1-5
  1 - Static Shock (or other F1 morph)
  2 - Offensive Protocol: Shred (or other F2 morph)
  3 - Defensive Protocol: Thorns
  4 - Offensive Protocol: Obliterate
  5 - Evolve

Weapon Skills (Hammer): numpad1-5
  NumPad1 - Positive Strike (auto)
  NumPad2 - Electro Whip
  NumPad3 - Rocket Charge
  NumPad4 - Shock Shield
  NumPad5 - Thunderclap

Utilities: numpad6-0
  NumPad6 - Heal skill
  NumPad7 - Elixir Gun Kit (skills 3, 4)
  NumPad8 - Flamethrower Kit (auto, 2, 4, 5)
  NumPad9 - Utility 3
  NumPad0 - Elite skill
"""

import time
import keyboard
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions_monitored import press_and_release, button_mash
from libs.key_mapping import key_mapping
from libs.logger import get_logger
import sys

logger = get_logger('power_amalgam_wvw')
# Ensure sub-logger propagates to root logger
logger.propagate = True
# Also add a direct stdout print for immediate feedback
def log_and_print(level, msg):
    """Log and also print to ensure visibility"""
    getattr(logger, level)(msg)
    print(f"[{level.upper()}] {msg}", flush=True)
    sys.stdout.flush()

# Coordinates for skill availability detection
# TODO: Update these coordinates using the coordinate_helper.py tool
DEFAULT_COORDS = {
    # Toolbelt skills (top bar, keys 1-5)
    'toolbelt_1': (2607, 950),  # 1 - Static Shock
    'toolbelt_2': (2645, 950),  # 2 - Offensive Protocol: Shred
    'toolbelt_3': (2693, 950),  # 3 - Defensive Protocol: Thorns
    'toolbelt_4': (2739, 950),  # 4 - Offensive Protocol: Obliterate
    'toolbelt_5': (2787, 950),  # 5 - Evolve
    
    # Weapon/Kit skills (bottom bar, numpad)
    'weapon_2': (2625, 1013),  # Electro Whip (Hammer 2)
    'weapon_3': (2686, 1013),  # Rocket Charge (Hammer 3)
    'weapon_4': (2743, 1013),  # Shock Shield (Hammer 4)
    'weapon_5': (2799, 1013),  # Thunderclap (Hammer 5)
    
    # Utility skills (numpad6-0)
    'utility_heal': (2652, 1013),    # NumPad6 - Heal
    'utility_elixir': (3007, 1013),  # NumPad7 - Elixir Gun Kit
    'utility_flamethrower': (3070, 1034),  # NumPad8 - Flamethrower Kit (check for white when equipped)
    'utility_3': (3116, 1013),       # NumPad9 - Utility 3
    'utility_elite': (3178, 1013),   # NumPad0 - Elite
}

# Debounce for kit toggles to avoid racing inputs
DEBOUNCE_WINDOW_SECONDS = 0.6
last_kit_toggle_time = 0.0
kit_switch_in_progress = False
current_mode = 'hammer'  # 'hammer', 'elixir', or 'flamethrower'

def just_toggled_recently() -> bool:
    """Return True if a kit toggle happened within the debounce window."""
    return (time.time() - last_kit_toggle_time) < DEBOUNCE_WINDOW_SECONDS

def check_stop_condition(stop_event):
    """Check if we should stop the rotation"""
    return not keyboard.is_pressed(key_mapping['numpad1']) or stop_event.is_set()

def check_skill_available(coords):
    """Check if a skill is available (not on cooldown)"""
    color = pixel_get_color(coords[0], coords[1])
    return color is not None and color != (0, 0, 0) and sum(color) > 300

def wait_until_on_cooldown(coords, timeout_seconds: float = 1.8, poll_seconds: float = 0.05) -> bool:
    """Wait until the given skill pixel turns dark (goes on cooldown).
    Returns True if it turned dark within timeout, False otherwise.
    """
    start = time.time()
    while (time.time() - start) < timeout_seconds:
        color = pixel_get_color(coords[0], coords[1])
        if color is None:
            return True
        if color == (0, 0, 0) or sum(color) <= 300:
            return True
        time.sleep(poll_seconds)
    return False

def is_kit_equipped(kit_coords):
    """Check if a kit is equipped by looking for white color"""
    color = pixel_get_color(kit_coords[0], kit_coords[1])
    if color is None:
        return False
    # Check if color is white or close to white (all RGB values high)
    return color[0] > 200 and color[1] > 200 and color[2] > 200

def execute_evolve_spike(stop_event):
    """
    Execute the PRIMARY BURST COMBO per AI instructions:
    1. Press F2 (Morph Skill 1) - initiate burst
    2. Press F3 (Morph Skill 2) - continue burst
    3. Press F4 (Morph Skill 3) - finish morph sequence
    4. Press F5 (EVOLVE) - gain stat boost + strain bonuses
    5. Switch to Flamethrower
    6. Use Flamethrower Skill 2
    7. Use Flamethrower Skill 4
    8. Auto attack with Flamethrower
    """
    logger.info("=" * 70)
    logger.info(">>> PRIMARY BURST COMBO (Coordinated Squad Moment)")
    logger.info("=" * 70)
    
    # Check if Evolve is ready
    evolve_ready = check_skill_available(DEFAULT_COORDS['toolbelt_5'])
    if not evolve_ready:
        logger.debug("Evolve not ready, skipping spike")
        return False
    
    # STEP 1: Morph Skills F2-F4 (build burst combo)
    logger.info(">>> STEP 1/7: Morph Skills Sequence (F2-F4)")
    
    shred_ready = check_skill_available(DEFAULT_COORDS['toolbelt_2'])
    thorns_ready = check_skill_available(DEFAULT_COORDS['toolbelt_3'])
    obliterate_ready = check_skill_available(DEFAULT_COORDS['toolbelt_4'])
    
    if shred_ready:
        logger.info("Using Morph F2 (Shred) - initiate burst")
        button_mash('2', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_2'])
        if check_stop_condition(stop_event): return False
    
    if thorns_ready:
        logger.info("Using Morph F3 (Thorns) - continue burst")
        button_mash('3', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_3'])
        if check_stop_condition(stop_event): return False
    
    if obliterate_ready:
        logger.info("Using Morph F4 (Obliterate) - finish morph sequence")
        button_mash('4', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_4'])
        if check_stop_condition(stop_event): return False
    
    # STEP 2: Evolve (F5) - triggers strain bonuses and stat boost
    logger.info(">>> STEP 2/7: Evolve (F5) - Stat boost + strain bonuses")
    button_mash('5', presses=3, delay=0.05)
    time.sleep(0.5)
    wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_5'])
    if check_stop_condition(stop_event): return False
    
    # STEP 3: Switch to Flamethrower
    logger.info(">>> STEP 3/7: Switching to Flamethrower")
    ensure_flamethrower_mode(stop_event)
    if check_stop_condition(stop_event): return False
    time.sleep(0.2)  # Brief pause after kit switch
    
    # STEP 4-5: Use Flamethrower Skills 2 and 4
    logger.info(">>> STEP 4/7: Flamethrower Skill 2")
    if check_skill_available(DEFAULT_COORDS['weapon_2']):
        logger.info("Using Flamethrower 2")
        button_mash(key_mapping['numpad2'], presses=2, delay=0.05)
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    logger.info(">>> STEP 5/7: Flamethrower Skill 4")
    if check_skill_available(DEFAULT_COORDS['weapon_4']):
        logger.info("Using Flamethrower 4")
        button_mash(key_mapping['numpad4'], presses=2, delay=0.05)
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    # STEP 6-7: Auto attack with Flamethrower (cone cleave)
    logger.info(">>> STEP 6-7/7: Flamethrower auto-attack (cone cleave)")
    for i in range(3):  # Use Flamethrower auto for a few cycles
        if check_stop_condition(stop_event): return False
        logger.debug(f"Flamethrower auto-attack cycle {i+1}/3")
        button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
        time.sleep(0.6)
    
    logger.info("=" * 70)
    logger.info("PRIMARY BURST COMBO COMPLETE")
    logger.info("=" * 70)
    return True

def ensure_flamethrower_mode(stop_event):
    """
    Ensure we're in Flamethrower mode - switch if not equipped
    Returns True if already in Flamethrower or successfully switched
    """
    global last_kit_toggle_time, kit_switch_in_progress, current_mode
    
    if kit_switch_in_progress or just_toggled_recently():
        return True  # Wait for current switch to complete
    
    if is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']):
        current_mode = 'flamethrower'
        return True
    
    # Not in Flamethrower - switch to it
    logger.info("Switching to Flamethrower Kit (NumPad8)")
    kit_switch_in_progress = True
    press_and_release(key_mapping['numpad8'])
    last_kit_toggle_time = time.time()
    time.sleep(0.8)
    kit_switch_in_progress = False
    
    if is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']):
        current_mode = 'flamethrower'
        return True
    
    return False

def is_elixir_gun_equipped():
    """Check if Elixir Gun is equipped"""
    return is_kit_equipped(DEFAULT_COORDS['utility_elixir'])

def ensure_hammer_mode(stop_event):
    """
    Ensure we're in Hammer mode - switch from kit if needed
    Returns True if already in Hammer or successfully switched
    """
    global last_kit_toggle_time, kit_switch_in_progress, current_mode
    
    if kit_switch_in_progress or just_toggled_recently():
        return True  # Wait for current switch to complete
    
    # Check if we're in any kit (Flamethrower or Elixir Gun)
    if is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']):
        # In Flamethrower - switch back to Hammer
        logger.info("Switching to Hammer (NumPad8)")
        kit_switch_in_progress = True
        press_and_release(key_mapping['numpad8'])
        last_kit_toggle_time = time.time()
        time.sleep(0.8)
        kit_switch_in_progress = False
        current_mode = 'hammer'
        return True
    elif is_elixir_gun_equipped():
        # In Elixir Gun - switch back to Hammer
        logger.info("Switching to Hammer (NumPad7)")
        kit_switch_in_progress = True
        press_and_release(key_mapping['numpad7'])
        last_kit_toggle_time = time.time()
        time.sleep(0.8)
        kit_switch_in_progress = False
        current_mode = 'hammer'
        return True
    else:
        # Already in Hammer
        current_mode = 'hammer'
        return True

def ensure_elixir_gun_mode(stop_event):
    """
    Ensure we're in Elixir Gun mode - switch if not equipped
    Returns True if already in Elixir Gun or successfully switched
    """
    global last_kit_toggle_time, kit_switch_in_progress, current_mode
    
    if kit_switch_in_progress or just_toggled_recently():
        return True
    
    if is_elixir_gun_equipped():
        current_mode = 'elixir'
        return True
    
    # Not in Elixir Gun - switch to it
    logger.info("Switching to Elixir Gun Kit (NumPad7)")
    kit_switch_in_progress = True
    press_and_release(key_mapping['numpad7'])
    last_kit_toggle_time = time.time()
    time.sleep(0.8)
    kit_switch_in_progress = False
    
    if is_elixir_gun_equipped():
        current_mode = 'elixir'
        return True
    
    return False

def cancel_out_of_kit(stop_event):
    """
    Cancel out of current kit using weapon swap (F1) - like healing_mechanist.py
    """
    global current_mode
    
    if is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']) or is_elixir_gun_equipped():
        logger.info("Canceling out of kit with weapon swap (F1)")
        press_and_release(key_mapping['f1'])
        time.sleep(0.5)
        current_mode = 'hammer'
        return True
    return False

def use_elixir_gun_skills(stop_event):
    """
    Use Elixir Gun skills (3, 4) for damage, then cancel out
    Assumes we're already in Elixir Gun mode
    """
    if not is_elixir_gun_equipped():
        logger.warning("Not in Elixir Gun mode - skipping")
        return False
    
    # Use Elixir Gun 4 (Acid Bomb) if available - cancel quickly
    if check_skill_available(DEFAULT_COORDS['weapon_4']):
        logger.info("Using Elixir Gun 4 (Acid Bomb)")
        button_mash(key_mapping['numpad4'], presses=2, delay=0.05)
        time.sleep(0.15)  # Very short delay - cancel almost immediately
        if check_stop_condition(stop_event): return False
        
        # Cancel Acid Bomb with weapon swap (F1) - faster cancellation
        logger.info("Canceling Acid Bomb with weapon swap (F1)")
        button_mash(key_mapping['f1'], presses=2, delay=0.05)
        time.sleep(0.25)
        if check_stop_condition(stop_event): return False
        return True
    
    # Use Elixir Gun 3 if available
    if check_skill_available(DEFAULT_COORDS['weapon_3']):
        logger.info("Using Elixir Gun 3")
        button_mash(key_mapping['numpad3'], presses=2, delay=0.05)
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    # After using Elixir Gun skills, cancel out of kit
    cancel_out_of_kit(stop_event)
    return True

def use_flamethrower_cleave(stop_event):
    """
    Use Flamethrower for sustained cleave damage
    Assumes we're already in Flamethrower mode
    """
    if not is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']):
        logger.warning("Not in Flamethrower mode - skipping cleave")
        return False
    
    # Use Flamethrower auto-attack (skill 1)
    logger.debug("Using Flamethrower auto-attack")
    button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
    time.sleep(0.6)
    
    # Use Flamethrower 2, 4, 5 if available (per Snow Crows guide)
    if check_skill_available(DEFAULT_COORDS['weapon_2']):
        logger.info("Using Flamethrower 2")
        button_mash(key_mapping['numpad2'], presses=2, delay=0.05)
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    if check_skill_available(DEFAULT_COORDS['weapon_4']):
        logger.info("Using Flamethrower 4")
        button_mash(key_mapping['numpad4'], presses=2, delay=0.05)
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    if check_skill_available(DEFAULT_COORDS['weapon_5']):
        logger.info("Using Flamethrower 5")
        button_mash(key_mapping['numpad5'], presses=2, delay=0.05)
        time.sleep(0.3)
        if check_stop_condition(stop_event): return False
    
    return True

def hammer_auto_attack_chain(stop_event):
    """Perform Hammer auto-attack chain"""
    for i in range(3):
        if check_stop_condition(stop_event):
            return False
        button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
        time.sleep(0.6)
    return True

def use_hammer_skills(stop_event):
    """
    Use all available Hammer skills
    Assumes we're already in Hammer mode
    """
    if is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']) or is_elixir_gun_equipped():
        logger.warning("Not in Hammer mode - skipping Hammer skills")
        return False
    
    skill_used = False
    
    # Use all Hammer skills based on availability
    thunderclap_ready = check_skill_available(DEFAULT_COORDS['weapon_5'])
    electrowhip_ready = check_skill_available(DEFAULT_COORDS['weapon_2'])
    rocket_ready = check_skill_available(DEFAULT_COORDS['weapon_3'])
    shock_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
    
    if thunderclap_ready:
        logger.info("Using Thunderclap (NumPad5)")
        button_mash(key_mapping['numpad5'], presses=3, delay=0.05)
        time.sleep(0.4)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_5'])
        skill_used = True
        if check_stop_condition(stop_event): return True
    
    if electrowhip_ready:
        logger.info("Using Electro Whip (NumPad2)")
        button_mash(key_mapping['numpad2'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_2'])
        skill_used = True
        if check_stop_condition(stop_event): return True
    
    if rocket_ready:
        logger.info("Using Rocket Charge (NumPad3)")
        button_mash(key_mapping['numpad3'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_3'])
        skill_used = True
        if check_stop_condition(stop_event): return True
    
    if shock_ready:
        logger.info("Using Shock Shield (NumPad4)")
        button_mash(key_mapping['numpad4'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_4'])
        skill_used = True
        if check_stop_condition(stop_event): return True
    
    # Use Hammer auto-attack if no skills available
    if not skill_used:
        logger.debug("Using Hammer auto-attack")
        button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
        time.sleep(0.6)
    
    return True

def power_amalgam_wvw_rotation(stop_event):
    """
    Dynamic WvW rotation:
    - Actively uses Hammer, Elixir Gun, and Flamethrower
    - Switches between weapons/kits based on available cooldowns
    - Uses Evolve spike when ready
    - Maintains pressure with all available skills
    """
    rotation_count = 0
    last_elixir_use = time.time()  # Track when we last used Elixir Gun (initialize to current time)
    flamethrower_usage_count = 0  # Track how many times we've used Flamethrower
    last_evolve_use = 0  # Track when we last used Evolve to prevent double-triggering
    
    while not stop_event.is_set():
        rotation_count += 1
        
        if check_stop_condition(stop_event): break
        
        # Check current mode
        in_flamethrower = is_kit_equipped(DEFAULT_COORDS['utility_flamethrower'])
        in_elixir = is_elixir_gun_equipped()
        current_mode_str = 'Flamethrower' if in_flamethrower else ('Elixir Gun' if in_elixir else 'Hammer')
        
        # Check all skill cooldowns
        evolve_ready = check_skill_available(DEFAULT_COORDS['toolbelt_5'])
        obliterate_ready = check_skill_available(DEFAULT_COORDS['toolbelt_4'])
        thorns_ready = check_skill_available(DEFAULT_COORDS['toolbelt_3'])
        shred_ready = check_skill_available(DEFAULT_COORDS['toolbelt_2'])
        
        # Check weapon/kit skill cooldowns
        hammer_5_ready = check_skill_available(DEFAULT_COORDS['weapon_5'])
        hammer_2_ready = check_skill_available(DEFAULT_COORDS['weapon_2'])
        hammer_3_ready = check_skill_available(DEFAULT_COORDS['weapon_3'])
        hammer_4_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
        
        elixir_ready = check_skill_available(DEFAULT_COORDS['utility_elixir'])
        flamethrower_ready = check_skill_available(DEFAULT_COORDS['utility_flamethrower'])
        
        # Log current state every loop
        current_time = time.time()
        time_since_elixir = current_time - last_elixir_use
        
        log_and_print('info', f"--- LOOP {rotation_count} | Mode: {current_mode_str} | Time since Elixir: {time_since_elixir:.1f}s ---")
        log_and_print('info', f"Evolve: {evolve_ready} | Morphs: F2={shred_ready} F3={thorns_ready} F4={obliterate_ready}")
        log_and_print('info', f"Hammer: 2={hammer_2_ready} 3={hammer_3_ready} 4={hammer_4_ready} 5={hammer_5_ready}")
        log_and_print('info', f"Kits: Elixir={elixir_ready} Flamethrower={flamethrower_ready}")
        
        # Priority 1: Evolve spike burst (highest priority)
        logger.debug("Checking Priority 1: Evolve spike")
        # Prevent double-triggering by ensuring at least 2 seconds has passed since last Evolve use
        time_since_evolve = current_time - last_evolve_use
        if evolve_ready and time_since_evolve > 2.0:  # At least 2 seconds since last Evolve (spike takes ~7s)
            log_and_print('info', ">>> PRIORITY 1 TRIGGERED: Evolve spike burst")
            log_and_print('info', "=" * 70)
            log_and_print('info', f"ROTATION CYCLE {rotation_count} - EVOLVE SPIKE PHASE")
            log_and_print('info', "=" * 70)
            
            # Set timestamp BEFORE executing to prevent immediate re-trigger
            last_evolve_use = time.time()
            execute_evolve_spike(stop_event)
            if check_stop_condition(stop_event): break
            continue
        else:
            if not evolve_ready:
                logger.debug(f"Priority 1 SKIP: Evolve not ready")
            else:
                logger.debug(f"Priority 1 SKIP: Evolve ready but only {time_since_evolve:.1f}s since last use (need >2.0s)")
        
        # Priority 2: Use Weapon Skills 2 and 5 (HIGH PRIORITY - use on cooldown)
        # These are the highest priority maintenance skills
        logger.debug("Checking Priority 2: Weapon Skills 2 and 5")
        if hammer_2_ready and not in_flamethrower and not in_elixir:
            log_and_print('info', ">>> PRIORITY 2 TRIGGERED: Weapon Skill 2 (HIGH PRIORITY)")
            button_mash(key_mapping['numpad2'], presses=3, delay=0.05)
            time.sleep(0.3)
            wait_until_on_cooldown(DEFAULT_COORDS['weapon_2'])
            if check_stop_condition(stop_event): break
            continue
        
        # Switch to weapon if Skill 2 is ready but we're in a kit
        if hammer_2_ready and (in_flamethrower or in_elixir):
            log_and_print('info', f">>> PRIORITY 2 TRIGGERED: Switching to weapon for Skill 2 (currently in {current_mode_str})")
            ensure_hammer_mode(stop_event)
            if check_stop_condition(stop_event): break
            if check_skill_available(DEFAULT_COORDS['weapon_2']):
                button_mash(key_mapping['numpad2'], presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['weapon_2'])
            if check_stop_condition(stop_event): break
            continue
        
        if hammer_5_ready and not in_flamethrower and not in_elixir:
            log_and_print('info', ">>> PRIORITY 2 TRIGGERED: Weapon Skill 5 (HIGH PRIORITY)")
            button_mash(key_mapping['numpad5'], presses=3, delay=0.05)
            time.sleep(0.4)
            wait_until_on_cooldown(DEFAULT_COORDS['weapon_5'])
            if check_stop_condition(stop_event): break
            continue
        
        # Switch to weapon if Skill 5 is ready but we're in a kit
        if hammer_5_ready and (in_flamethrower or in_elixir):
            log_and_print('info', f">>> PRIORITY 2 TRIGGERED: Switching to weapon for Skill 5 (currently in {current_mode_str})")
            ensure_hammer_mode(stop_event)
            if check_stop_condition(stop_event): break
            if check_skill_available(DEFAULT_COORDS['weapon_5']):
                button_mash(key_mapping['numpad5'], presses=3, delay=0.05)
                time.sleep(0.4)
                wait_until_on_cooldown(DEFAULT_COORDS['weapon_5'])
            if check_stop_condition(stop_event): break
            continue
        
        logger.debug(f"Priority 2 SKIP: Hammer 2={hammer_2_ready} 5={hammer_5_ready}, in_kit={in_flamethrower or in_elixir}")
        
        # Priority 3: Use other weapon skills (Hammer 3, 4) if available
        logger.debug("Checking Priority 3: Other weapon skills (3, 4)")
        if (hammer_3_ready or hammer_4_ready) and not in_flamethrower and not in_elixir:
            log_and_print('info', f">>> PRIORITY 3 TRIGGERED: Using weapon skills 3={hammer_3_ready} 4={hammer_4_ready}")
            use_hammer_skills(stop_event)
            if check_stop_condition(stop_event): break
            continue
        else:
            logger.debug(f"Priority 3 SKIP: Hammer 3={hammer_3_ready} 4={hammer_4_ready}, in_kit={in_flamethrower or in_elixir}")
        
        # Priority 4: Use morph skills (F2-F4) - build burst when available
        # Only use if Evolve isn't ready (don't waste morphs before burst combo)
        logger.debug(f"Checking Priority 4: Morph skills (Evolve ready: {evolve_ready})")
        if not evolve_ready:
            if obliterate_ready:
                log_and_print('info', ">>> PRIORITY 4 TRIGGERED: Using Offensive Protocol: Obliterate (4) - Strain effect")
                button_mash('4', presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_4'])
                if check_stop_condition(stop_event): break
                continue
            
            if thorns_ready:
                log_and_print('info', ">>> PRIORITY 4 TRIGGERED: Using Defensive Protocol: Thorns (3) - Strain effect")
                button_mash('3', presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_3'])
                if check_stop_condition(stop_event): break
                continue
            
            if shred_ready:
                log_and_print('info', ">>> PRIORITY 4 TRIGGERED: Using Offensive Protocol: Shred (2)")
                button_mash('2', presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_2'])
                if check_stop_condition(stop_event): break
                continue
        else:
            logger.debug("Priority 4 SKIP: Evolve is ready, saving morphs for burst combo")
        
        # Priority 5: Use Flamethrower Skills 2 and 4 (MEDIUM PRIORITY - rotation)
        logger.debug(f"Checking Priority 5: Flamethrower skills (in kit: {in_flamethrower})")
        if in_flamethrower:
            flamethrower_2_ready = check_skill_available(DEFAULT_COORDS['weapon_2'])
            flamethrower_4_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
            logger.debug(f"Flamethrower skills: 2={flamethrower_2_ready} 4={flamethrower_4_ready}")
            
            if flamethrower_2_ready:
                log_and_print('info', ">>> PRIORITY 5 TRIGGERED: Using Flamethrower Skill 2 (MEDIUM PRIORITY)")
                button_mash(key_mapping['numpad2'], presses=2, delay=0.05)
                time.sleep(0.3)
                if check_stop_condition(stop_event): break
                continue
            
            if flamethrower_4_ready:
                log_and_print('info', ">>> PRIORITY 5 TRIGGERED: Using Flamethrower Skill 4 (MEDIUM PRIORITY)")
                button_mash(key_mapping['numpad4'], presses=2, delay=0.05)
                time.sleep(0.3)
                if check_stop_condition(stop_event): break
                continue
            
            # If no Flamethrower skills ready, use auto-attack
            log_and_print('info', ">>> PRIORITY 5: Flamethrower auto-attack (no skills ready)")
            button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
            time.sleep(0.6)
            continue
        else:
            logger.debug("Priority 5 SKIP: Not in Flamethrower kit")
        
        # Priority 6: Switch to Elixir Gun if it's been a while since last use and Hammer skills are on cooldown
        # Alternate between Flamethrower and Elixir Gun to use both
        logger.debug("Checking Priority 6: Switch to Elixir Gun")
        hammer_all_on_cd = not hammer_5_ready and not hammer_2_ready and not hammer_3_ready and not hammer_4_ready
        elixir_kit_ready = check_skill_available(DEFAULT_COORDS['utility_elixir'])
        
        logger.debug(f"Priority 6 conditions: hammer_all_cd={hammer_all_on_cd}, elixir_kit={elixir_kit_ready}, "
                    f"time_since={time_since_elixir:.1f}s, in_kit={in_flamethrower or in_elixir}")
        
        if hammer_all_on_cd and not in_elixir and not in_flamethrower and elixir_kit_ready and time_since_elixir > 5.0:
            log_and_print('info', f">>> PRIORITY 6 TRIGGERED: Switching to Elixir Gun (time since last use: {time_since_elixir:.1f}s)")
            ensure_elixir_gun_mode(stop_event)
            if is_elixir_gun_equipped():
                # Check skills after switching
                elixir_3_ready = check_skill_available(DEFAULT_COORDS['weapon_3'])
                elixir_4_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
                log_and_print('info', f"After switching: Elixir skills 3={elixir_3_ready} 4={elixir_4_ready}")
                if elixir_3_ready or elixir_4_ready:
                    use_elixir_gun_skills(stop_event)
                    last_elixir_use = current_time
                    if check_stop_condition(stop_event): break
                else:
                    logger.warning("Elixir Gun has no skills ready - canceling immediately")
                    cancel_out_of_kit(stop_event)
                    if check_stop_condition(stop_event): break
            continue
        else:
            logger.debug("Priority 6 SKIP: Conditions not met")
        
        # Priority 7: Use Elixir Gun Skills 3 and 4 (MEDIUM PRIORITY - rotation filler)
        logger.debug(f"Checking Priority 7: Elixir Gun skills (in kit: {in_elixir})")
        if in_elixir:
            elixir_3_ready = check_skill_available(DEFAULT_COORDS['weapon_3'])
            elixir_4_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
            logger.debug(f"Elixir Gun skills: 3={elixir_3_ready} 4={elixir_4_ready}")
            
            if elixir_3_ready:
                log_and_print('info', ">>> PRIORITY 7 TRIGGERED: Using Elixir Gun Skill 3 (MEDIUM PRIORITY)")
                button_mash(key_mapping['numpad3'], presses=2, delay=0.05)
                time.sleep(0.3)
                last_elixir_use = time.time()
                if check_stop_condition(stop_event): break
                continue
            
            if elixir_4_ready:
                log_and_print('info', ">>> PRIORITY 7 TRIGGERED: Using Elixir Gun Skill 4 (Acid Bomb) - MEDIUM PRIORITY")
                button_mash(key_mapping['numpad4'], presses=2, delay=0.05)
                time.sleep(0.15)  # Very short delay - cancel almost immediately
                # Cancel Acid Bomb with weapon swap (F1) - like healing_mechanist.py
                log_and_print('info', "Canceling Acid Bomb with weapon swap (F1)")
                button_mash(key_mapping['f1'], presses=2, delay=0.05)
                time.sleep(0.25)
                last_elixir_use = time.time()
                if check_stop_condition(stop_event): break
                continue
            
            # No skills ready - cancel out of Elixir Gun
            log_and_print('info', ">>> PRIORITY 7: Elixir Gun has no skills ready - canceling out")
            cancel_out_of_kit(stop_event)
            if check_stop_condition(stop_event): break
            continue
        else:
            logger.debug("Priority 7 SKIP: Not in Elixir Gun kit")
        
        # Priority 8: Switch to Flamethrower if Hammer skills are on cooldown and not in any kit
        # Use Flamethrower if we haven't used Elixir Gun recently (alternate between them)
        logger.debug("Checking Priority 8: Switch to Flamethrower")
        logger.debug(f"Priority 8 conditions: hammer_all_cd={hammer_all_on_cd}, not_in_kit={not in_flamethrower and not in_elixir}, "
                    f"time_since_elixir={time_since_elixir:.1f}s (need >5.0)")
        
        if hammer_all_on_cd and not in_flamethrower and not in_elixir and time_since_elixir > 5.0:
            log_and_print('info', f">>> PRIORITY 8 TRIGGERED: Switching to Flamethrower (time since Elixir: {time_since_elixir:.1f}s)")
            ensure_flamethrower_mode(stop_event)
            if is_kit_equipped(DEFAULT_COORDS['utility_flamethrower']):
                use_flamethrower_cleave(stop_event)
                flamethrower_usage_count += 1
                if check_stop_condition(stop_event): break
            continue
        else:
            logger.debug("Priority 8 SKIP: Conditions not met")
        
        # Priority 9: If nothing else available, try to use what we have or switch
        # If we're in a kit but nothing is happening, check if we should switch
        logger.debug("Checking Priority 9: Filler/Auto-attack")
        if in_flamethrower:
            # Only switch out of Flamethrower if multiple Hammer skills are ready (not just one)
            # This prevents switching out too early
            hammer_skills_count = sum([hammer_5_ready, hammer_2_ready, hammer_3_ready, hammer_4_ready])
            logger.debug(f"Priority 9: In Flamethrower, hammer skills ready: {hammer_skills_count}")
            if hammer_skills_count >= 2:  # At least 2 Hammer skills ready
                log_and_print('info', f">>> PRIORITY 9 TRIGGERED: Multiple Hammer skills available ({hammer_skills_count}) - switching from Flamethrower")
                ensure_hammer_mode(stop_event)
                if check_stop_condition(stop_event): break
                continue
            
            # Otherwise use Flamethrower auto-attack
            log_and_print('info', f">>> PRIORITY 9: Flamethrower auto-attack filler (no skills, only {hammer_skills_count} hammer skills ready)")
            button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
            time.sleep(0.6)
        elif in_elixir:
            # Elixir Gun should have been handled above, but just in case
            logger.warning(">>> PRIORITY 9: Elixir Gun auto-attack filler (UNEXPECTED - should have been handled above)")
            cancel_out_of_kit(stop_event)
            time.sleep(0.5)
        else:
            # In Hammer - use auto-attack
            log_and_print('info', ">>> PRIORITY 9: Hammer auto-attack filler (nothing else available)")
            button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
            time.sleep(0.6)
        
        # Small delay before next check
        time.sleep(0.1)

def run(stop_event):
    """
    Main entry point for Power Amalgam (WvW) spec
    Hold numpad1 to activate the rotation
    """
    log_and_print('info', "Power Amalgam (WvW) spec started")
    log_and_print('info', "Hold NumPad1 to activate rotation")
    log_and_print('info', "Focus: Strong spikes with Evolve + morphs for generating downs")
    log_and_print('info', "Toolbelt skills on keys 1-5, weapon/kit skills on numpad")
    
    while not stop_event.is_set():
        # Check stop event first
        if stop_event.is_set():
            logger.info("Stop event detected")
            break
        
        # Activate rotation when numpad1 is pressed
        if keyboard.is_pressed(key_mapping['numpad1']):
            log_and_print('info', "NumPad1 pressed - starting rotation")
            power_amalgam_wvw_rotation(stop_event)
        
        # Always sleep to prevent busy-waiting
        time.sleep(0.05)
    
    logger.info("Power Amalgam (WvW) spec ended")

