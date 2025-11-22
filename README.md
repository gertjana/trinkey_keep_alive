# Neo Trinkey Keep-Awake Device

A USB device that prevents your laptop from going to sleep or showing a screensaver by simulating minimal user activity. Features NeoPixel status indicators and laptop control interface.

![Status: Active](https://img.shields.io/badge/status-active-brightgreen)
![Platform: CircuitPython](https://img.shields.io/badge/platform-CircuitPython-blueviolet)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- 🎮 **Random keep-awake actions** (F15 key press or tiny mouse movements)
- 💡 **Visual status indicators** using 4 NeoPixels
- 🖥️ **Laptop control** via serial commands
- ⚙️ **Configurable interval** (5-300 seconds)
- 🔄 **Toggle on/off** remotely from your laptop
- 📊 **Interactive monitor mode**

## 🎨 Status Colors

| Color | Status |
|-------|--------|
| 🔵 Blue | Idle/Ready (device off) |
| 🟢 Green | Active (keeping laptop awake) |
| 🟡 Yellow | Action flash (key press/mouse move) |

## 📋 Hardware Requirements

- [Adafruit Neo Trinkey (SAMD21)](https://www.adafruit.com/product/4870) with 4 NeoPixels
- USB-A port on your laptop
- That's it!

## 🛠️ Software Requirements

### Neo Trinkey
- CircuitPython 8.0 or newer
- Adafruit HID library

### Laptop
- Python 3.7+
- pyserial library

## 📦 Installation

### 1. Set Up the Neo Trinkey

1. **Install CircuitPython** on your Neo Trinkey:
   - Download CircuitPython for Neo Trinkey from [circuitpython.org](https://circuitpython.org/board/neo_trinkey_m0/)
   - Enter bootloader mode (double-press reset button)
   - Drag the .UF2 file to the TRINKETBOOT drive
   - Device will reboot and appear as CIRCUITPY drive

2. **Install required libraries**:
   - Download the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries)
   - Copy the `adafruit_hid` folder to `CIRCUITPY/lib/`

3. **Upload the device code**:
   - Copy `trinkey/code.py` to the root of the CIRCUITPY drive
   - The device will automatically restart

4. **Verify installation**:
   - NeoPixels should light up blue (idle state)
   - Device is ready!

### 2. Set Up Laptop Controller

1. **Install Python dependencies**:
```bash
pip install pyserial
```

2. **Run the controller**:
```bash
cd laptop
python controller.py monitor
```

## 🚀 Usage

### Quick Commands

```bash
# Turn on keep-awake
python controller.py on

# Turn off keep-awake
python controller.py off

# Toggle on/off
python controller.py toggle

# Check current status
python controller.py status

# Set interval to 60 seconds
python controller.py interval 60

# Interactive monitor mode
python controller.py monitor
```

### Monitor Mode (Recommended)

Run the interactive monitor for easy control:

```bash
python controller.py monitor
```

**Monitor Commands:**
- `on` or `1` - Activate keep-awake
- `off` or `0` - Deactivate keep-awake
- `toggle` or `t` - Toggle state
- `status` or `s` - Check current status
- `i <seconds>` - Set interval (e.g., `i 45`)
- `quit` or `q` - Exit monitor

### Manual Port Selection

If auto-detection doesn't work:

```bash
# Windows
python controller.py --port COM3 monitor

# macOS/Linux
python controller.py --port /dev/ttyACM0 monitor
```

## 🔧 Configuration

### Changing Default Settings

Edit `trinkey/code.py`:

```python
ACTION_INTERVAL = 30  # Seconds between actions (default: 30)

# Change status colors
COLOR_IDLE = (0, 0, 255)    # Blue
COLOR_ACTIVE = (0, 255, 0)  # Green
COLOR_ACTION = (255, 255, 0) # Yellow
```

### Keep-Awake Actions

The device randomly performs one of these actions:
1. Press F15 key (rarely used, non-intrusive)
2. Move mouse 1 pixel right and back
3. Move mouse 1 pixel down and back

You can modify the `keep_awake_action()` function to customize behavior.

## 📁 Project Structure

```
neo-trinkey-keepawake/
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore             # Git ignore patterns
├── trinkey/              # Neo Trinkey CircuitPython code
│   └── code.py           # Main device code
├── laptop/               # Laptop controller
│   └── controller.py     # Python control script
└── docs/                 # Additional documentation
    └── TROUBLESHOOTING.md
```

## 🐛 Troubleshooting

### Device not found
- Check USB cable connection
- Try a different USB port
- Verify CIRCUITPY drive is visible
- Check that CircuitPython is installed correctly

### Serial port not detected
- **Windows**: Check Device Manager for COM port
- **macOS/Linux**: Run `ls /dev/tty*` to list ports
- Try unplugging and replugging the device
- Use `--port` argument to specify manually

### NeoPixels not lighting up
- Check that `neopixel` library is installed (built into CircuitPython)
- Verify brightness setting in code
- Try adjusting `brightness=0.3` value (0.0-1.0)

### Commands not working
- Verify serial connection is established
- Check that you're using the correct port
- Try restarting the device (unplug/replug)
- Check for typos in commands

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

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

---

**Made with ❤️ and CircuitPython**