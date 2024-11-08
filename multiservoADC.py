'''
Simple test of the Analog To Digital Converter using 2 potentiometers
'''
import board
import busio
import keyboard

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

def testmax(servos):
    print("max")
    for s in servos:
        s.max()
def testmid(servos):
   print("mid")
   for s in servos:
       s.mid()
       
def testmin(servos):
    print("min")
    for s in servos:
        s.min()
def testdelta(servos, delta):
    print("delta", delta)
    for s in servos:
        s.value = clamp(s.value + delta, -1,1)
        
def testdetach(servos):
    print("Detatching")
    for s in servos:
        s.detach()

max_pot_volt = 3.3
min_pot_volt = 0.0

i2c = busio.I2C(board.SCL,board.SDA)

ads = ADS.ADS1115(i2c,address=0x48)
# ads.gain = 1
pot0 = AnalogIn(ads, ADS.P0)
pot1 = AnalogIn(ads, ADS.P1)
pot2 = AnalogIn(ads, ADS.P2)

servo0 = Servo(17, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)
servo1 = Servo(27, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)
servo2 = Servo(22, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)
servo3 = Servo(23, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

servos = [servo0, servo1, servo2, servo3]

while True:
        if keyboard.read_key() == "o":
            servo3.min()
        if keyboard.read_key() == "c":
            servo3.max()
        
        if keyboard.read_key() == "1":
            testmin(servos)
        if keyboard.read_key() =="2":
            testmid(servos)
        if keyboard.read_key() == "3":
            testmax(servos)
        if keyboard.read_key() == "z":
            testdelta(servos, 0.1)
        if keyboard.read_key() == "x":
            print("sdf")
            testdelta(servos, -0.1)
        if keyboard.read_key() == "0":
            testdetach(servos)
        
        '''
        servo0.value = map(pot0.voltage, max_pot_volt, min_pot_volt, -1, 1)
        servo1.value = map(pot1.voltage, max_pot_volt, min_pot_volt, -1, 1)
        servo2.value = map(pot2.voltage, max_pot_volt, min_pot_volt, -1, 1)
        time.sleep(0.1)
---------============================---------        '''
