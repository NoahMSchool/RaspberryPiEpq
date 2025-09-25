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

def set_servo_degrees(servo, degrees):
    mapped = map(degrees, -90, 90, -1, 1)
    servo.value = mapped


def SERVOtest(servo):
    for i in range(0,181,30):
        v = map(i,0,180,-1,1)
        servo.value = v
        print(v)
        sleep(0.25)
    
    servo.value=None

# GPIOtest(servopin)

servopin = 12

sg90_min = 700/1000000
sg90_max = 2500/1000000

ser = Servo(servopin, initial_value = 0, min_pulse_width = sg90_min, max_pulse_width = sg90_max)

print(ser.min_pulse_width)
print(ser.max_pulse_width)


#SERVOtest(ser)

set_servo_degrees(ser, 0)
sleep(2)
set_servo_degrees(ser, -90)
sleep(2)
set_servo_degrees(ser, 0)
sleep(2)
set_servo_degrees(ser, 90)
sleep(2)
set_servo_degrees(ser, 00)
sleep(2)
ser.value = None