import time
import board
import neopixel
import touchio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import random

pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, brightness=0.3, auto_write=False)
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)

active = False
quiet_mode = False

last_action_time = time.monotonic()
last_status_change = time.monotonic()

ACTION_INTERVAL = 30
ACTION_OFFSET = 5
STATUS_LED_TIMEOUT = 2

touch1_pressed = False
touch2_pressed = False

COLOR_OFF = (0, 0, 0)
COLOR_ACTIVE = (0, 255, 0)
COLOR_IDLE = (0, 0, 255)
COLOR_ACTION = (255, 255, 0)

def set_status(color):
    global last_status_change
    if not quiet_mode:
        pixels.fill(color)
        pixels.show()
        last_status_change = time.monotonic()

def flash_status(color, duration=0.1):
    if not quiet_mode:
        pixels.fill(color)
        pixels.show()
        time.sleep(duration)
        set_status(COLOR_ACTIVE if active else COLOR_IDLE)

def running_light_animation():
    if not quiet_mode:
        for i in range(8):
            pixels.fill(COLOR_OFF)
            pixels[i % 4] = COLOR_ACTION
            pixels.show()
            time.sleep(0.1)
        pixels.fill(COLOR_OFF)
        pixels.show()

def keep_awake_action():
    action = random.randint(0, 2)
    
    if action == 0:
        kbd.press(Keycode.F15)
        kbd.release_all()
    elif action == 1:
        mouse.move(x=1, y=0)
        time.sleep(0.05)
        mouse.move(x=-1, y=0)
    else:
        mouse.move(x=0, y=1)
        time.sleep(0.05)
        mouse.move(x=0, y=-1)
    
    running_light_animation()

def handle_touch_buttons():
    global active, quiet_mode, touch1_pressed, touch2_pressed, last_action_time
    
    if touch1.value:
        if not touch1_pressed:
            touch1_pressed = True
            active = not active
            if active:
                last_action_time = time.monotonic() - ACTION_INTERVAL + ACTION_OFFSET 
            set_status(COLOR_ACTIVE if active else COLOR_IDLE)
    else:
        touch1_pressed = False
    
    if touch2.value:
        if not touch2_pressed:
            touch2_pressed = True
            quiet_mode = not quiet_mode
            if quiet_mode:
                # Brief flash before going quiet
                pixels.fill((255, 128, 0))  # Orange flash for touch 2
                pixels.show()
                time.sleep(0.1)
                pixels.fill(COLOR_OFF)
                pixels.show()
            else:
                # Brief flash when enabling LEDs
                pixels.fill((255, 128, 0))  # Orange flash for touch 2
                pixels.show()
                time.sleep(0.1)
                set_status(COLOR_ACTIVE if active else COLOR_IDLE)
    else:
        touch2_pressed = False

set_status(COLOR_IDLE)

print("Neo Trinkey Keep-Awake Device Ready")
print("Touch 1: Toggle On/Off | Touch 2: Toggle Quiet Mode")

# Main loop
while True:
    handle_touch_buttons()
    
    # Turn off status LEDs after timeout
    if not quiet_mode:
        current_time = time.monotonic()
        if current_time - last_status_change >= STATUS_LED_TIMEOUT:
            if pixels[0] != COLOR_OFF:  # Only update if not already off
                pixels.fill(COLOR_OFF)
                pixels.show()
    
    # Perform keep-awake action if active
    if active:
        current_time = time.monotonic()
        if current_time - last_action_time >= ACTION_INTERVAL:
            keep_awake_action()
            last_action_time = current_time
    
    time.sleep(0.1)