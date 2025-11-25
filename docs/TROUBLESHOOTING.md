# Troubleshooting Guide

## Common Issues and Solutions

### Device Not Detected

**Symptom:** Laptop controller can't find the Neo Trinkey

**Solutions:**

1. Check USB cable is properly connected
2. Try a different USB port (some ports may not provide enough power)
3. Verify CircuitPython is installed
4. Check serial port manually

### NeoPixels Not Working

**Symptom:** LEDs don't light up or show wrong colors

**Solutions:**

1. Check brightness setting in code.py
2. Verify code has no errors
3. Test with simple code

### Serial Communication Issues

**Symptom:** Commands sent but no response

**Solutions:**

1. Verify baud rate matches (115200)
2. Check line endings
3. Add longer timeout
4. Try manual serial connection

For more details, see the full documentation.
