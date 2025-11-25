#!/usr/bin/env python3
"""
Laptop Controller for Neo Trinkey Keep-Awake Device

Usage:
    python controller.py on          # Turn on keep-awake
    python controller.py off         # Turn off keep-awake
    python controller.py toggle      # Toggle on/off
    python controller.py status      # Check current status
    python controller.py interval 45 # Set interval to 45 seconds
    python controller.py quiet on    # Disable LED actions
    python controller.py quiet off   # Enable LED actions
    python controller.py monitor     # Interactive monitor mode

Requirements:
    pip install pyserial
"""

import argparse
import sys
import time

import serial
import serial.tools.list_ports


def find_neo_trinkey():
    """Find the Neo Trinkey serial port"""
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Neo Trinkey typically shows up as USB Serial Device
        if "USB" in port.description or "ACM" in port.device or "COM" in port.device:
            try:
                # Try to open and verify
                ser = serial.Serial(port.device, 115200, timeout=1)
                ser.write(b"status\n")
                time.sleep(0.1)
                if ser.in_waiting > 0:
                    response = ser.readline().decode("utf-8").strip()
                    if response.startswith("STATUS:"):
                        print(f"Found Neo Trinkey on {port.device}")
                        return ser
                ser.close()
            except (serial.SerialException, OSError):
                pass

    return None


def send_command(ser, command):
    """Send command and get response"""
    ser.write(f"{command}\n".encode())
    time.sleep(0.2)

    if ser.in_waiting > 0:
        response = ser.readline().decode("utf-8").strip()
        return response
    return None


def monitor_mode(ser):
    """Interactive monitor mode with status display"""
    print("\n" + "=" * 50)
    print("Neo Trinkey Keep-Awake Monitor")
    print("=" * 50)
    print("\nCommands:")
    print("  1 or 'on'     - Turn ON keep-awake")
    print("  0 or 'off'    - Turn OFF keep-awake")
    print("  t or 'toggle' - Toggle on/off")
    print("  s or 'status' - Check status")
    print("  i or 'interval' - Set interval (e.g., 'i 45')")
    print("  qon          - Enable quiet mode (disable LEDs)")
    print("  qoff         - Disable quiet mode (enable LEDs)")
    print("  q or 'quit'   - Exit monitor")
    print("=" * 50 + "\n")

    # Get initial status
    response = send_command(ser, "status")
    if response:
        status = response.split(":")[1]
        print(f"Current Status: {status}\n")

    while True:
        try:
            user_input = input("Command> ").strip().lower()

            if user_input in ["q", "quit", "exit"]:
                print("Exiting monitor mode...")
                break
            elif user_input in ["1", "on"]:
                response = send_command(ser, "on")
                print("✓ Keep-Awake ACTIVATED")
            elif user_input in ["0", "off"]:
                response = send_command(ser, "off")
                print("✓ Keep-Awake DEACTIVATED")
            elif user_input in ["t", "toggle"]:
                response = send_command(ser, "toggle")
                if response:
                    status = response.split(":")[1]
                    print(f"✓ Toggled to: {status}")
            elif user_input in ["s", "status"]:
                response = send_command(ser, "status")
                if response:
                    status = response.split(":")[1]
                    print(f"Current Status: {status}")
            elif user_input.startswith("i"):
                parts = user_input.split()
                if len(parts) == 2:
                    try:
                        interval = int(parts[1])
                        response = send_command(ser, f"interval:{interval}")
                        if response and response.startswith("INTERVAL:"):
                            print(f"✓ Interval set to {interval} seconds")
                        else:
                            print("✗ Invalid interval (must be 5-300 seconds)")
                    except ValueError:
                        print("✗ Invalid interval value")
                else:
                    print("Usage: i <seconds>  (e.g., 'i 45')")
            elif user_input == "qon":
                response = send_command(ser, "quiet on")
                if response and response.startswith("QUIET:"):
                    print("✓ Quiet mode ENABLED (LEDs off)")
            elif user_input == "qoff":
                response = send_command(ser, "quiet off")
                if response and response.startswith("QUIET:"):
                    print("✓ Quiet mode DISABLED (LEDs on)")
            elif user_input:
                print("Unknown command. Type 'q' to quit.")

        except KeyboardInterrupt:
            print("\n\nExiting monitor mode...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Control Neo Trinkey Keep-Awake Device"
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["on", "off", "toggle", "status", "interval", "quiet", "monitor"],
        help="Command to send to device",
    )
    parser.add_argument(
        "value",
        nargs="?",
        help="Value for interval command or on/off for quiet command",
    )
    parser.add_argument("--port", help="Specify serial port manually")

    args = parser.parse_args()

    # Find or open serial port
    if args.port:
        try:
            ser = serial.Serial(args.port, 115200, timeout=1)
            print(f"Connected to {args.port}")
        except Exception as e:
            print(f"Error opening port {args.port}: {e}")
            sys.exit(1)
    else:
        ser = find_neo_trinkey()
        if not ser:
            print("Error: Could not find Neo Trinkey device")
            print("\nAvailable ports:")
            for port in serial.tools.list_ports.comports():
                print(f"  {port.device}: {port.description}")
            sys.exit(1)

    try:
        if not args.command or args.command == "monitor":
            monitor_mode(ser)
        elif args.command == "interval":
            if args.value:
                try:
                    interval_val = int(args.value)
                    response = send_command(ser, f"interval:{interval_val}")
                    print(response if response else "Command sent")
                except ValueError:
                    print("Error: interval value must be a number")
            else:
                print("Error: interval command requires a value")
                print("Usage: python controller.py interval 45")
        elif args.command == "quiet":
            if args.value in ["on", "off"]:
                response = send_command(ser, f"quiet {args.value}")
                print(response if response else "Command sent")
            else:
                print("Error: quiet command requires 'on' or 'off'")
                print("Usage: python controller.py quiet on")
                print("       python controller.py quiet off")
        else:
            response = send_command(ser, args.command)
            print(response if response else "Command sent")

    finally:
        ser.close()


if __name__ == "__main__":
    main()
