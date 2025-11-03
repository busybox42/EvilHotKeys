from libs.pixel_search import pixel_search
from libs.pixel_get_color import get_color as pixel_get_color
from libs.keyboard_actions_monitored import press_and_release, press, release, record_interrupt
from libs.key_mapping import key_mapping
from libs.logger import get_logger
from libs.wow_helpers import get_coord
import time
import keyboard

logger = get_logger('wow_responsive')

# Constants
DEFAULT_COLOR = (0, 0, 0)

def run(stop_event):
    """Responsive WoW spec that checks stop_event frequently"""
    keys_to_watch = ['numpad4', 'numpad5', 'numpad7']
    
    try:
        # Get interrupt coordinates from config
        interrupt_x, interrupt_y = get_coord('interrupt')
        logger.info(f"WoW responsive spec started. Checking interrupt at ({interrupt_x}, {interrupt_y})")
        logger.info("Press numpad4, numpad5, or numpad7 to activate rotation.")
        
        loop_count = 0
        
        while not stop_event.is_set():
            loop_count += 1
            
            # Log every 100 loops (every ~5 seconds) to show it's responsive
            if loop_count % 100 == 0:
                logger.info(f"Spec running, loop {loop_count}")
            
            key_pressed = False
            
            # Check each key quickly
            for key in keys_to_watch:
                if stop_event.is_set():
                    logger.info("Stop event detected, exiting key loop")
                    return
                
                try:
                    # Quick keyboard check with timeout
                    if keyboard.is_pressed(key_mapping[key]):
                        key_pressed = True
                        logger.info(f"Key {key} pressed, executing rotation")
                        
                        # Check for interrupt condition
                        interrupt_target = pixel_get_color(interrupt_x, interrupt_y)
                        
                        # Fire interrupt if we got a valid color that's not black
                        if interrupt_target is not None and interrupt_target != DEFAULT_COLOR:
                            logger.info(f"Interrupt fired! Color detected: {interrupt_target}")
                            record_interrupt("enemy")
                            press_and_release('=')

                        # Press and release the current key
                        press(key_mapping[key])
                        release(key_mapping[key])
                        time.sleep(0.2)
                        break  # Exit key loop after handling one key
                        
                except Exception as e:
                    logger.error(f"Error checking key {key}: {e}")
                    continue
            
            # Always sleep to prevent busy-waiting and allow stop_event checks
            if key_pressed:
                time.sleep(0.1)  # Shorter sleep after action
            else:
                time.sleep(0.05)  # Very short sleep when no keys pressed
            
            # Check stop_event one more time before next loop
            if stop_event.is_set():
                logger.info("Stop event detected, exiting main loop")
                break
                
    except Exception as e:
        logger.exception(f"Error in WoW responsive spec: {e}")
    finally:
        logger.info("WoW responsive spec ended")
