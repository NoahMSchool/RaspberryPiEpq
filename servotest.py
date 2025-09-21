'''
Testing a servo motor, which uses Pulse Width Modulation (PWM) in two ways
- directly using a GPIO PWM output pin and setting the duty cycle
- using the gpiozero library which has a Servo object
'''
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import Servo

def map(value, in_min, in_max, out_min, out_max):
    return ((out_max-out_min) * (value-in_min))/(in_max-in_min) + out_min

def SERVOtest(servo):
    for i in range(0,181,30):
        v = map(i,0,180,-1,1)
        servo.value = v
        print(v)
        sleep(0.25)
    
    servo.value=None

# GPIOtest(servopin)

servopin = 12

ser = Servo(servopin, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

print(ser.min_pulse_width)
print(ser.max_pulse_width)


SERVOtest(ser)