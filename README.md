![Status: Active](https://img.shields.io/badge/status-active-brightgreen)
![Platform: CircuitPython](https://img.shields.io/badge/platform-CircuitPython-blueviolet)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)

# Neo Trinkey Keep-Awake Device

A standalone USB device that prevents your laptop from going to sleep or showing a screensaver by simulating minimal user activity. Control it with capacitive touch buttons and visual NeoPixel feedback.

![Neo Trinkey](/images/neo_trinky.jpg)

## 🎨 Status Colors

| Color     | Status                            |
| --------- | --------------------------------- |
| 🔵 Blue   | Idle/Ready (device off)           |
| 🟢 Green  | Active (keeping laptop awake)     |
| 🟡 Yellow | Action flash (circular animation) |
| 🟠 Orange | Quiet mode enabled indicator      |

**Note:** Status LEDs automatically turn off after 2 seconds to reduce brightness/distraction.

## Hardware Requirements

- [Adafruit Neo Trinkey (SAMD21)](https://www.adafruit.com/product/4870) with 4 NeoPixels
- USB-A port on your laptop

## Software Requirements

- CircuitPython 8.0 or newer
- Adafruit HID library

## Installation

1. **Install CircuitPython** on your Neo Trinkey:

   - Download CircuitPython for Neo Trinkey from [circuitpython.org](https://circuitpython.org/board/neo_trinkey_m0/)
   - Enter bootloader mode (double-press reset button)
   - Drag the .UF2 file to the TRINKETBOOT drive
   - Device will reboot and appear as CIRCUITPY drive

2. **Install required libraries**:

   - Download the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries)
   - Copy the `adafruit_hid` folder to `CIRCUITPY/lib/`

3. **Upload the device code**:

   - Copy both `trinky/boot.py` and `trinky/code.py` to the root of the CIRCUITPY drive
   - The device will automatically restart
   - if not, un and re-plug the device

4. **Verify installation**:
   - NeoPixels should light up blue for 2 seconds (idle state)
   - No red flashing (red = error)
   - Device is ready!

## 🚀 Usage

### Touch Button Controls

- **Touch 1** (Left pad): Toggle keep-awake on/off

  - Magenta flash when pressed
  - Green = Active, Blue = Idle (shows for 2 seconds)
  - First action happens 5 seconds after activation

- **Touch 2** (Right pad): Toggle quiet mode
  - Orange flash when pressed
  - In quiet mode, all LEDs stay off (except action animations if not in quiet mode)

### How It Works

1. Plug the Trinkey into your laptop's USB port
2. Touch the left pad (Touch 1) to activate - you'll see the LEDs go green for 2 seconds
3. After 5 seconds, the first keep-awake action occurs (circular yellow animation)
4. Actions repeat every 30 seconds while active
5. Touch left pad again to deactivate
6. Touch right pad (Touch 2) anytime to toggle quiet mode (disable LED animations)

## 🔧 Configuration

### Changing Default Settings

Edit `trinkey/code.py`:

```python
ACTION_INTERVAL = 30  # Seconds between actions
ACTION_OFFSET = 5     # Seconds to wait before first action after activation
STATUS_LED_TIMEOUT = 2  # Seconds to show status LEDs

# Change status colors
COLOR_IDLE = (0, 0, 255)    # Blue
COLOR_ACTIVE = (0, 255, 0)  # Green
COLOR_ACTION = (255, 255, 0) # Yellow

# Change touch button feedback colors
(255, 128, 0)   # Orange for Touch 2
```

### Keep-Awake Actions

The device randomly performs one of these actions:

1. Press F15 key (rarely used, non-intrusive)
2. Move mouse 1 pixel right and back
3. Move mouse 1 pixel down and back

Each action triggers a circular yellow LED animation around the 4 NeoPixels.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Adafruit](https://www.adafruit.com/) for the Neo Trinkey hardware
- CircuitPython community for excellent documentation
- Coffee ☕ for keeping me awake while coding this

## 📧 Contact

Questions or suggestions? Open an issue on GitHub!

## ⚠️ Disclaimer

This device is intended for legitimate use cases like preventing screen timeout during presentations or long-running tasks. Please use responsibly and in accordance with your organization's policies.
