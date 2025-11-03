"""
Power Amalgam (Hammer) - PvE/Raid Build for Guild Wars 2
Based on: https://web.archive.org/web/20250923030431/https://snowcrows.com/builds/raids/engineer/power-amalgam

Build Overview:
- Weapon: Hammer
- Utilities: Plasmatic Strike, Bomb Kit, Throw Mine, Flux Strike (elite)
- Rotation: Hammer burst > Toolbelt morphs > Bomb Kit > repeat
- Focus: High burst damage, cleave, CC

Your Keybinds:
Toolbelt (F1-F5): keys 1-5
  1 - Static Shock
  2 - Offensive Protocol: Shred
  3 - Offensive Protocol: Pierce
  4 - Offensive Protocol: Obliterate
  5 - Evolve

Weapon Skills (Hammer): numpad1-5
  NumPad1 - Positive Strike (auto)
  NumPad2 - Electro Whip
  NumPad3 - Rocket Charge
  NumPad4 - Shock Shield
  NumPad5 - Thunderclap

Utilities: numpad6-0
  NumPad6 - A.E.D (heal)
  NumPad7 - Plasmatic Strike
  NumPad8 - Bomb Kit
  NumPad9 - Throw Mine
  NumPad0 - Flux Strike (elite)
"""

import time
import keyboard
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions_monitored import press_and_release, button_mash
from libs.key_mapping import key_mapping
from libs.logger import get_logger

logger = get_logger('power_amalgam_hammer')

# Coordinates for skill availability detection (from power_amalgam.py)
DEFAULT_COORDS = {
    # Toolbelt skills (top bar, keys 1-5)
    'toolbelt_1': (2607, 950),  # 1 - Static Shock
    'toolbelt_2': (2645, 950),  # 2 - Offensive Protocol: Shred
    'toolbelt_3': (2693, 950),  # 3 - Offensive Protocol: Pierce
    'toolbelt_4': (2739, 950),  # 4 - Offensive Protocol: Obliterate
    'toolbelt_5': (2787, 950),  # 5 - Evolve
    
    # Weapon/Kit skills (bottom bar, numpad)
    'weapon_2': (2625, 1013),  # Electro Whip (Hammer 2)
    'weapon_3': (2686, 1013),  # Rocket Charge (Hammer 3)
    'weapon_4': (2743, 1013),  # Shock Shield (Hammer 4)
    'weapon_5': (2799, 1013),  # Thunderclap (Hammer 5)
    
    # Utility skills (numpad6-0)
    'utility_heal': (2652, 1013),      # NumPad6 - A.E.D
    'utility_plasmatic': (3007, 1013), # NumPad7 - Plasmatic Strike
    'utility_bomb': (3070, 1034),      # NumPad8 - Bomb Kit (check for white when equipped)
    'utility_mine': (3116, 1013),      # NumPad9 - Throw Mine
    'utility_elite': (3178, 1013),     # NumPad0 - Flux Strike
}

# Debounce for kit toggles to avoid racing inputs
DEBOUNCE_WINDOW_SECONDS = 0.6
last_kit_toggle_time = 0.0
kit_switch_in_progress = False
current_mode = 'hammer'  # 'hammer' or 'bomb'

def just_toggled_recently() -> bool:
    """Return True if a kit toggle happened within the debounce window."""
    return (time.time() - last_kit_toggle_time) < DEBOUNCE_WINDOW_SECONDS

def switch_to_bomb() -> None:
    global last_kit_toggle_time, kit_switch_in_progress, current_mode
    if kit_switch_in_progress:
        return
    kit_switch_in_progress = True
    press_and_release(key_mapping['numpad8'])
    last_kit_toggle_time = time.time()
    current_mode = 'bomb'
    time.sleep(0.8)
    kit_switch_in_progress = False

def switch_to_hammer() -> None:
    global last_kit_toggle_time, kit_switch_in_progress, current_mode
    if kit_switch_in_progress:
        return
    kit_switch_in_progress = True
    press_and_release(key_mapping['numpad8'])
    last_kit_toggle_time = time.time()
    current_mode = 'hammer'
    time.sleep(1.0)
    kit_switch_in_progress = False

def ensure_hammer_mode() -> None:
    """If Bomb Kit is detected outside a toggle, switch back to Hammer."""
    if not kit_switch_in_progress and not just_toggled_recently() and is_bomb_kit_equipped():
        logger.warning("Recovery: Bomb Kit detected during rotation - switching to Hammer")
        switch_to_hammer()

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

def is_bomb_kit_equipped():
    """Check if Bomb Kit is equipped by looking for white color"""
    coords = DEFAULT_COORDS['utility_bomb']
    color = pixel_get_color(coords[0], coords[1])
    if color is None:
        return False
    
    # Check if color is white or close to white (all RGB values high)
    is_white = color[0] > 200 and color[1] > 200 and color[2] > 200
    
    # ALWAYS log this to help debug the issue
    logger.info(f"Bomb Kit check at ({coords[0]}, {coords[1]}): RGB={color}, is_white={is_white}")
    
    return is_white

def opener_bomb_combo(stop_event):
    """
    Opener bomb combo in correct order:
    Big Ol' Bomb (NumPad5) > Magnetic Bomb (NumPad4) > Fire Bomb (NumPad2) > Galvanic Bomb (NumPad3)
    
    When Bomb Kit is equipped, weapon skills become:
    NumPad1 - Bomb
    NumPad2 - Fire Bomb  
    NumPad3 - Galvanic Bomb
    NumPad4 - Magnetic Bomb
    NumPad5 - Big Ol' Bomb
    """
    logger.info("Switching to Bomb Kit for opener")
    
    # Activate Bomb Kit (NumPad8)
    switch_to_bomb()
    # Give time to equip
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    # Verify Bomb Kit is equipped (check for white color)
    if not is_bomb_kit_equipped():
        # Skip silently and try again
        time.sleep(0.2)
        return False
    
    # Big Ol' Bomb (NumPad5) - mash to ensure it fires
    logger.info("Using Big Ol' Bomb (NumPad5)")
    button_mash(key_mapping['numpad5'], presses=3, delay=0.05)
    time.sleep(0.4)
    wait_until_on_cooldown(DEFAULT_COORDS['weapon_5'])
    if check_stop_condition(stop_event): return False
    
    # Magnetic Bomb (NumPad4) - mash to ensure it fires
    logger.info("Using Magnetic Bomb (NumPad4)")
    button_mash(key_mapping['numpad4'], presses=3, delay=0.05)
    time.sleep(0.4)
    wait_until_on_cooldown(DEFAULT_COORDS['weapon_4'])
    if check_stop_condition(stop_event): return False
    
    # Fire Bomb (NumPad2) - mash to ensure it fires
    logger.info("Using Fire Bomb (NumPad2)")
    button_mash(key_mapping['numpad2'], presses=3, delay=0.05)
    time.sleep(0.4)
    wait_until_on_cooldown(DEFAULT_COORDS['weapon_2'])
    if check_stop_condition(stop_event): return False
    
    # Galvanic Bomb (NumPad3) - mash to ensure it fires
    logger.info("Using Galvanic Bomb (NumPad3)")
    button_mash(key_mapping['numpad3'], presses=3, delay=0.05)
    time.sleep(0.4)
    wait_until_on_cooldown(DEFAULT_COORDS['weapon_3'])
    if check_stop_condition(stop_event): return False
    
    # Return to Hammer (NumPad8 toggles)
    logger.info("Returning to Hammer - pressing NumPad8")
    
    # Use switch helper to toggle back to Hammer
    switch_to_hammer()
    
    # Check what we see after first press
    logger.info("After first NumPad8 press:")
    if is_bomb_kit_equipped():
        logger.warning("Still in Bomb Kit - pressing NumPad8 again via helper")
        switch_to_hammer()
        
        # Check what we see after second press
        logger.info("After second NumPad8 press:")
        if is_bomb_kit_equipped():
            logger.error("Still showing Bomb Kit after 2 toggles - NumPad8 might not be the right key!")
        else:
            logger.info("Successfully returned to Hammer after 2nd press")
    else:
        logger.info("Successfully returned to Hammer after 1st press")
    
    return True

def use_bomb_regular(stop_event):
    """
    Use regular Bomb (NumPad1 while in Bomb Kit)
    NumPad1 - Bomb (same position as Positive Strike)
    """
    logger.info("Switching to Bomb Kit for regular bomb")
    
    # Activate Bomb Kit (NumPad8)
    switch_to_bomb()
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    if is_bomb_kit_equipped():
        # Regular Bomb (NumPad1) - mash to ensure it fires
        logger.info("Using Bomb (NumPad1)")
        button_mash(key_mapping['numpad1'], presses=3, delay=0.05)
        time.sleep(0.4)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_1'] if 'weapon_1' in DEFAULT_COORDS else DEFAULT_COORDS['weapon_2'])
        if check_stop_condition(stop_event): return False
    
    # Return to Hammer
    switch_to_hammer()
    
    if is_bomb_kit_equipped():
        logger.warning("Still in Bomb Kit - pressing NumPad8 again via helper")
        switch_to_hammer()
    
    if is_bomb_kit_equipped():
        logger.error("Still showing Bomb Kit after 2 toggles!")
    else:
        logger.info("Successfully returned to Hammer")
    
    return True

def use_fire_bomb(stop_event):
    """
    Use just Fire Bomb
    NumPad2 - Fire Bomb (same position as Electro Whip)
    """
    logger.info("Switching to Bomb Kit for Fire Bomb")
    
    # Activate Bomb Kit (NumPad8)
    switch_to_bomb()
    time.sleep(0.1)
    if check_stop_condition(stop_event): return False
    
    if is_bomb_kit_equipped():
        # Fire Bomb (NumPad2) - mash to ensure it fires
        logger.info("Using Fire Bomb (NumPad2)")
        button_mash(key_mapping['numpad2'], presses=3, delay=0.05)
        time.sleep(0.4)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_2'])
        if check_stop_condition(stop_event): return False
    
    # Return to Hammer
    switch_to_hammer()
    
    if is_bomb_kit_equipped():
        logger.warning("Still in Bomb Kit - pressing NumPad8 again via helper")
        switch_to_hammer()
    
    if is_bomb_kit_equipped():
        logger.error("Still showing Bomb Kit after 2 toggles!")
    else:
        logger.info("Successfully returned to Hammer")
    
    return True

def use_plasmatic_strike(stop_event):
    """Use Plasmatic Strike utility (NumPad7) - has cast time"""
    coords = DEFAULT_COORDS['utility_plasmatic']
    color = pixel_get_color(coords[0], coords[1])
    
    # Debug: Log the color we're seeing
    if color:
        color_sum = sum(color)
        logger.debug(f"Plasmatic Strike coord ({coords[0]}, {coords[1]}): color={color}, sum={color_sum}")
    
    if check_skill_available(coords):
        logger.info("Using Plasmatic Strike (NumPad7)")
        button_mash(key_mapping['numpad7'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(coords)
        if check_stop_condition(stop_event): return False
    return True

def use_throw_mine(stop_event):
    """Use Throw Mine utility (NumPad9) - instant cast"""
    if check_skill_available(DEFAULT_COORDS['utility_mine']):
        logger.info("Using Throw Mine (NumPad9)")
        button_mash(key_mapping['numpad9'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['utility_mine'])
        if check_stop_condition(stop_event): return False
    return True

def use_flux_strike(stop_event):
    """Use Flux Strike elite (NumPad0) - has cast time"""
    if check_skill_available(DEFAULT_COORDS['utility_elite']):
        logger.info("Using Flux Strike (NumPad0)")
        button_mash(key_mapping['numpad0'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['utility_elite'])
        if check_stop_condition(stop_event): return False
    return True

def use_static_shock(stop_event):
    """Use Static Shock toolbelt (key 1) - instant"""
    if check_skill_available(DEFAULT_COORDS['toolbelt_1']):
        logger.info("Using Static Shock (1)")
        button_mash('1', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_1'])
        if check_stop_condition(stop_event): return False
    return True

def use_electro_whip(stop_event):
    """Use Electro Whip (Hammer 2) - has cast time"""
    coords = DEFAULT_COORDS['weapon_2']
    color = pixel_get_color(coords[0], coords[1])
    
    # Debug: Log what we're seeing
    if color:
        color_sum = sum(color)
        if color_sum > 300:
            logger.info(f"Electro-Whip READY: color={color}, sum={color_sum}")
        else:
            logger.debug(f"Electro-Whip on cooldown: color={color}, sum={color_sum}")
    
    if check_skill_available(coords):
        logger.info("Using Electro-Whip (NumPad2)")
        button_mash(key_mapping['numpad2'], presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(coords)
        if check_stop_condition(stop_event): return False
    return True

def use_thunderclap(stop_event):
    """Use Thunderclap (Hammer 5) - has cast time"""
    if check_skill_available(DEFAULT_COORDS['weapon_5']):
        logger.info("Using Thunderclap (NumPad5)")
        button_mash(key_mapping['numpad5'], presses=3, delay=0.05)
        time.sleep(0.4)
        wait_until_on_cooldown(DEFAULT_COORDS['weapon_5'])
        if check_stop_condition(stop_event): return False
    return True

def hammer_auto_attack_chain(stop_event):
    """
    Perform 3x Hammer auto-attack chain
    IMPORTANT: Makes sure we're not in Bomb Kit first!
    """
    # Debounce: if a kit switch is in progress or just happened, skip this tick
    if kit_switch_in_progress or just_toggled_recently():
        logger.debug("Auto-attack: debounce active, skipping this chain tick")
        return False
    # If we're in Bomb Kit, attempt a single safe recovery toggle then exit
    if is_bomb_kit_equipped():
        logger.warning("Auto-attack: Detected Bomb Kit still equipped - attempting recovery to Hammer")
        ensure_hammer_mode()
        return False
    
    # Perform auto-attacks (Positive Strike on Hammer) - mash for reliability
    for i in range(3):
        if check_stop_condition(stop_event):
            return False
        button_mash(key_mapping['numpad1'], presses=2, delay=0.05)
        time.sleep(0.6)  # Wait for full chain
    
    return True

def execute_full_burst(stop_event):
    """
    Execute the full burst rotation when major skills are ready
    """
    logger.info(">>> BURST STEP 1/6: Opening (Mine + Bombs)")
    
    # 1. Throw Mine (precast/detonate)
    use_throw_mine(stop_event)
    if check_stop_condition(stop_event): return False
    
    # 2. Bomb combo: Big Ol' Bomb > Magnetic > Fire > Galvanic
    opener_bomb_combo(stop_event)
    if check_stop_condition(stop_event): return False
    
    # 3. Detonate (Throw Mine again)
    use_throw_mine(stop_event)
    if check_stop_condition(stop_event): return False
    
    logger.info(">>> BURST STEP 2/6: Thunderclap + Utilities")
    
    # 4. Thunderclap
    use_thunderclap(stop_event)
    if check_stop_condition(stop_event): return False
    
    # 5. Flux Strike
    use_flux_strike(stop_event)
    if check_stop_condition(stop_event): return False
    
    # 6. Plasmatic Strike (big damage buff) - ALWAYS use in burst
    logger.info("Forcing Plasmatic Strike (NumPad7) - big damage buff")
    press_and_release(key_mapping['numpad7'])
    time.sleep(0.6)
    if check_stop_condition(stop_event): return False
    
    logger.info(">>> BURST STEP 3/6: First Morph Sequence (Shred > EW > Pierce > Obliterate)")
    
    # 7-10. First morph sequence: Shred > Electro-Whip > Pierce > Obliterate
    if check_skill_available(DEFAULT_COORDS['toolbelt_2']):
        logger.info("Using Offensive Protocol: Shred (2)")
        button_mash('2', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_2'])
    if check_stop_condition(stop_event): return False
    
    use_electro_whip(stop_event)
    if check_stop_condition(stop_event): return False
    
    if check_skill_available(DEFAULT_COORDS['toolbelt_3']):
        logger.info("Using Offensive Protocol: Pierce (3)")
        button_mash('3', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_3'])
    if check_stop_condition(stop_event): return False
    
    if check_skill_available(DEFAULT_COORDS['toolbelt_4']):
        logger.info("Using Offensive Protocol: Obliterate (4)")
        button_mash('4', presses=3, delay=0.05)
        time.sleep(0.3)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_4'])
    if check_stop_condition(stop_event): return False
    
    logger.info(">>> BURST STEP 4/6: Evolve (Reset Morphs)")
    
    # 11. Evolve (resets morphs) - mash to ensure it fires
    if check_skill_available(DEFAULT_COORDS['toolbelt_5']):
        logger.info("Using Evolve (5) - morphs reset!")
        button_mash('5', presses=3, delay=0.05)
        time.sleep(0.5)
        wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_5'])
    if check_stop_condition(stop_event): return False
    
    logger.info(">>> BURST STEP 5/6: Second Morph Sequence (Shred > Pierce > Obliterate)")
    
    # 12-14. Second morph sequence: Shred > Pierce > Obliterate - mash aggressively after Evolve
    logger.info("Using Offensive Protocol: Shred (2)")
    button_mash('2', presses=3, delay=0.05)
    time.sleep(0.3)
    wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_2'])
    if check_stop_condition(stop_event): return False
    
    logger.info("Using Offensive Protocol: Pierce (3)")
    button_mash('3', presses=3, delay=0.05)
    time.sleep(0.3)
    wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_3'])
    if check_stop_condition(stop_event): return False
    
    logger.info("Using Offensive Protocol: Obliterate (4)")
    button_mash('4', presses=3, delay=0.05)
    time.sleep(0.3)
    wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_4'])
    if check_stop_condition(stop_event): return False
    
    logger.info(">>> BURST STEP 6/6: Finisher (Mine + Electro-Whip + Bombs)")
    
    # 15-18. Throw Mine > Electro-Whip > Fire Bomb > Bomb
    use_throw_mine(stop_event)
    if check_stop_condition(stop_event): return False
    
    use_electro_whip(stop_event)
    if check_stop_condition(stop_event): return False
    
    use_fire_bomb(stop_event)
    if check_stop_condition(stop_event): return False
    
    use_bomb_regular(stop_event)
    if check_stop_condition(stop_event): return False
    
    logger.info("=" * 70)
    logger.info("BURST COMPLETE - All 6 steps executed successfully")
    logger.info("=" * 70)
    return True

def power_amalgam_rotation(stop_event):
    """
    Dynamic rotation that checks for cooldowns:
    - Execute full burst when Thunderclap is ready
    - Fill with auto-attacks and Electro-Whip while waiting
    - Use Static Shock before starting next burst
    """
    rotation_count = 0
    
    while not stop_event.is_set():
        rotation_count += 1
        
        if check_stop_condition(stop_event): break
        
        # Recovery: if Bomb Kit is lingering, switch to Hammer before deciding phase
        ensure_hammer_mode()
        
        # Check if major skills are ready for burst
        thunderclap_ready = check_skill_available(DEFAULT_COORDS['weapon_5'])
        
        if thunderclap_ready:
            logger.info("=" * 70)
            logger.info(f"ROTATION CYCLE {rotation_count} - BURST PHASE START")
            logger.info("Thunderclap (NumPad5) is READY - executing full burst rotation")
            logger.info("=" * 70)
            
            # Execute full burst rotation
            execute_full_burst(stop_event)
            if check_stop_condition(stop_event): break
            
            # After burst: filler phase (3x auto + skills + auto + Static Shock)
            logger.info("-" * 70)
            logger.info("POST-BURST FILLER: 3x Auto + skills + auto + Static Shock")
            logger.info("-" * 70)
            
            for i in range(3):
                hammer_auto_attack_chain(stop_event)
                if check_stop_condition(stop_event): break
            
            # Use Electro-Whip if available
            if check_skill_available(DEFAULT_COORDS['weapon_2']):
                use_electro_whip(stop_event)
            else:
                logger.debug("Electro-Whip on cooldown (post-burst)")
            
            # Use Rocket Charge if available - mash to ensure firing
            if check_skill_available(DEFAULT_COORDS['weapon_3']):
                logger.info("Using Rocket Charge (NumPad3)")
                button_mash(key_mapping['numpad3'], presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['weapon_3'])
            else:
                logger.debug("Rocket Charge on cooldown (post-burst)")
            
            # Use Shock Shield if available - mash to ensure firing
            if check_skill_available(DEFAULT_COORDS['weapon_4']):
                logger.info("Using Shock Shield (NumPad4)")
                button_mash(key_mapping['numpad4'], presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['weapon_4'])
            else:
                logger.debug("Shock Shield on cooldown (post-burst)")
            
            hammer_auto_attack_chain(stop_event)
            use_static_shock(stop_event)
            
            logger.info("Burst cycle complete - checking for next Thunderclap\n")
            
        else:
            # Thunderclap on cooldown - fill with all available skills
            logger.info("-" * 70)
            logger.info(f"ROTATION CYCLE {rotation_count} - FILLER PHASE")
            logger.info("Thunderclap on cooldown - checking available skills...")
            
            # Check what's available
            flux_ready = check_skill_available(DEFAULT_COORDS['utility_elite'])
            plasmatic_ready = check_skill_available(DEFAULT_COORDS['utility_plasmatic'])
            shred_ready = check_skill_available(DEFAULT_COORDS['toolbelt_2'])
            pierce_ready = check_skill_available(DEFAULT_COORDS['toolbelt_3'])
            obliterate_ready = check_skill_available(DEFAULT_COORDS['toolbelt_4'])
            electrowhip_ready = check_skill_available(DEFAULT_COORDS['weapon_2'])
            rocket_ready = check_skill_available(DEFAULT_COORDS['weapon_3'])
            shock_ready = check_skill_available(DEFAULT_COORDS['weapon_4'])
            mine_ready = check_skill_available(DEFAULT_COORDS['utility_mine'])
            
            logger.info(f"Skills ready: Flux={flux_ready}, Plasmatic={plasmatic_ready}, "
                       f"Shred={shred_ready}, Pierce={pierce_ready}, Obliterate={obliterate_ready}, "
                       f"Electro-Whip={electrowhip_ready}, Rocket={rocket_ready}, "
                       f"Shock={shock_ready}, Mine={mine_ready}")
            
            skill_used = False
            
            # Priority 1: Flux Strike (elite) - use whenever available
            if flux_ready:
                use_flux_strike(stop_event)
                skill_used = True
                if check_stop_condition(stop_event): break
            else:
                logger.debug("Flux Strike on cooldown")
            
            # Priority 2: Plasmatic Strike (big damage buff) - use whenever available
            if plasmatic_ready:
                use_plasmatic_strike(stop_event)
                skill_used = True
                if check_stop_condition(stop_event): break
            else:
                logger.debug("Plasmatic Strike on cooldown")
            
            # Priority 3: Electro-Whip (NumPad2) - use whenever available
            if electrowhip_ready:
                use_electro_whip(stop_event)
                skill_used = True
                if check_stop_condition(stop_event): break
            else:
                logger.debug("Electro-Whip on cooldown")
            
            # Priority 4: Offensive Protocols if available (maintain pressure even outside strict morph windows)
            if shred_ready:
                logger.info("Using Offensive Protocol: Shred (2)")
                button_mash('2', presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_2'])
                skill_used = True
                if check_stop_condition(stop_event): break
            if pierce_ready and not check_stop_condition(stop_event):
                logger.info("Using Offensive Protocol: Pierce (3)")
                button_mash('3', presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_3'])
                skill_used = True
                if check_stop_condition(stop_event): break
            if obliterate_ready and not check_stop_condition(stop_event):
                logger.info("Using Offensive Protocol: Obliterate (4)")
                button_mash('4', presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['toolbelt_4'])
                skill_used = True
                if check_stop_condition(stop_event): break

            # Priority 5: Rocket Charge (NumPad3) if available - mash to ensure firing
            if rocket_ready:
                logger.info("Using Rocket Charge (NumPad3)")
                button_mash(key_mapping['numpad3'], presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['weapon_3'])
                skill_used = True
                if check_stop_condition(stop_event): break
            else:
                logger.debug("Rocket Charge on cooldown")
            
            # Priority 6: Shock Shield (NumPad4) if available - mash to ensure firing
            if shock_ready:
                logger.info("Using Shock Shield (NumPad4)")
                button_mash(key_mapping['numpad4'], presses=3, delay=0.05)
                time.sleep(0.3)
                wait_until_on_cooldown(DEFAULT_COORDS['weapon_4'])
                skill_used = True
                if check_stop_condition(stop_event): break
            else:
                logger.debug("Shock Shield on cooldown")
            
            # Priority 7: Throw Mine if available
            if mine_ready:
                use_throw_mine(stop_event)
                skill_used = True
                if check_stop_condition(stop_event): break
            else:
                logger.debug("Throw Mine on cooldown")
            
            # Priority 8: Auto attack chain (if nothing else available)
            if not skill_used:
                logger.info("All priority skills on cooldown - using auto-attack chain")
            hammer_auto_attack_chain(stop_event)
            if check_stop_condition(stop_event): break
            
            # Small delay before checking cooldowns again
            time.sleep(0.2)

def run(stop_event):
    """
    Main entry point for Power Amalgam (Hammer) spec
    Hold numpad1 to activate the rotation
    """
    logger.info("Power Amalgam (Hammer) raid spec started")
    logger.info("Hold NumPad1 to activate rotation")
    logger.info("Toolbelt skills on keys 1-5, weapon/kit skills on numpad")
    
    # Debug: Check initial Bomb Kit status
    logger.info("Initial Bomb Kit status check:")
    is_bomb_kit_equipped()
    
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
    
    logger.info("Power Amalgam (Hammer) raid spec ended")

