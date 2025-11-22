# Neo Trinkey Keep-Awake Device
# Copy this to code.py on your Neo Trinkey (CircuitPython)

import time
import board
import neopixel
import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import random

# Initialize hardware
pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=0.3, auto_write=False)
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# Status
active = False
quiet_mode = False  # When True, disable all LED actions
last_action_time = time.monotonic()
ACTION_INTERVAL = 30  # seconds between actions

# Colors
COLOR_OFF = (0, 0, 0)
COLOR_ACTIVE = (0, 255, 0)  # Green when active
COLOR_IDLE = (0, 0, 255)    # Blue when idle/ready
COLOR_ACTION = (255, 255, 0)  # Yellow flash during action

def set_status(color):
    """Set all NeoPixels to a color"""
    if not quiet_mode:
        pixels.fill(color)
        pixels.show()

def flash_status(color, duration=0.1):
    """Flash NeoPixels briefly"""
    if not quiet_mode:
        pixels.fill(color)
        pixels.show()
        time.sleep(duration)
        set_status(COLOR_ACTIVE if active else COLOR_IDLE)

def keep_awake_action():
    """Perform a random keep-awake action"""
    action = random.randint(0, 2)
    
    if action == 0:
        # Press F15 key (rarely used, won't interfere)
        kbd.press(Keycode.F15)
        kbd.release_all()
    elif action == 1:
        # Small mouse jiggle
        mouse.move(x=1, y=0)
        time.sleep(0.05)
        mouse.move(x=-1, y=0)
    else:
        # Tiny mouse movement
        mouse.move(x=0, y=1)
        time.sleep(0.05)
        mouse.move(x=0, y=-1)
    
    flash_status(COLOR_ACTION)

def process_command(command):
    """Process commands from laptop"""
    global active, ACTION_INTERVAL, quiet_mode
    
    command = command.strip().lower()
    
    if command == 'on':
        active = True
        set_status(COLOR_ACTIVE)
        usb_cdc.data.write(b'STATUS:ACTIVE\n')
    elif command == 'off':
        active = False
        set_status(COLOR_IDLE)
        usb_cdc.data.write(b'STATUS:IDLE\n')
    elif command == 'toggle':
        active = not active
        set_status(COLOR_ACTIVE if active else COLOR_IDLE)
        status = 'ACTIVE' if active else 'IDLE'
        usb_cdc.data.write(f'STATUS:{status}\n'.encode())
    elif command == 'status':
        status = 'ACTIVE' if active else 'IDLE'
        usb_cdc.data.write(f'STATUS:{status}\n'.encode())
    elif command == 'quiet on':
        quiet_mode = True
        pixels.fill(COLOR_OFF)
        pixels.show()
        usb_cdc.data.write(b'QUIET:ON\n')
    elif command == 'quiet off':
        quiet_mode = False
        set_status(COLOR_ACTIVE if active else COLOR_IDLE)
        usb_cdc.data.write(b'QUIET:OFF\n')
    elif command.startswith('interval:'):
        try:
            new_interval = int(command.split(':')[1])
            if 5 <= new_interval <= 300:  # Between 5 seconds and 5 minutes
                ACTION_INTERVAL = new_interval
                usb_cdc.data.write(f'INTERVAL:{ACTION_INTERVAL}\n'.encode())
        except:
            usb_cdc.data.write(b'ERROR:INVALID_INTERVAL\n')

# Initial status
set_status(COLOR_IDLE)

print("Neo Trinkey Keep-Awake Device Ready")
print("Commands: on, off, toggle, status, interval:30, quiet on, quiet off")

# Main loop
while True:
    # Check for commands from laptop
    if usb_cdc.data.in_waiting > 0:
        try:
            command = usb_cdc.data.readline().decode('utf-8')
            process_command(command)
        except Exception as e:
            print(f"Error processing command: {e}")
    
    # Perform keep-awake action if active
    if active:
        current_time = time.monotonic()
        if current_time - last_action_time >= ACTION_INTERVAL:
            keep_awake_action()
            last_action_time = current_time
    
    time.sleep(0.1)  # Small delay to prevent CPU spinning