# sg90_calibrate.py
import time
from gpiozero import Servo
try:
    from gpiozero.pins.pigpio import PiGPIOFactory
    FACT = PiGPIOFactory()
except Exception:
    FACT = None  # falls back to default timing

PIN = 12
min_us, max_us = 1500, 1800  # start safe

def make_servo():
    return Servo(PIN,
                 min_pulse_width=min_us/1_000_000,
                 max_pulse_width=max_us/1_000_000,
                 pin_factory=FACT,
                 initial_value=0.0)

ser = make_servo()
print(f"Start range: {min_us}-{max_us} µs. Centering…"); time.sleep(1)

def try_edge(val_desc, v):
    print(f"Testing {val_desc} (value={v:+.2f})")
    ser.value = v
    time.sleep(1.0)

try:
    try_edge("min", -1.0)
    try_edge("center", 0.0)
    try_edge("max", +1.0)

    # If it *doesn't* hit hard stops (no buzzing/straining), widen slightly:
    # Increase cautiously, e.g. min_us -= 50; max_us += 50; then recreate the Servo()
    # Repeat until you *almost* hit the stops, then back off 50 µs.
finally:
    ser.value = None
    ser.close()