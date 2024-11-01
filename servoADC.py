'''
Simple test of the Analog To Digital Converter using 2 potentiometers
'''
import board
import busio
import time

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from gpiozero import Servo
def clamp(val, out_min, out_max):
    return max(min(val, out_max), out_min)
    
def map(value, in_min, in_max, out_min, out_max):
    val = ((out_max-out_min) * (value-in_min))/(in_max-in_min) + out_min
    val = clamp(val, out_min, out_max)
    
    return val
i2c = busio.I2C(board.SCL,board.SDA)

ads = ADS.ADS1115(i2c,address=0x48)
# ads.gain = 1

pot = AnalogIn(ads, ADS.P0)
max_pot_volt = 3.3
min_pot_volt = 0.0
servo = Servo(17, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

while True:
        v = map(pot.voltage, max_pot_volt, min_pot_volt, -1, 1)
        print(pot.voltage, v)
        servo.value = v
        time.sleep(0.1)
