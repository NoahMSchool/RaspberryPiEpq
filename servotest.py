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

def calculate_duty_cycle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    servo_min_micro = 500
    servo_max_micro = 2500
    
    pulse_width = map(angle, 0, 180, servo_min_micro, servo_max_micro) 
    servo_period_micro = 20000
    pwm = map(pulse_width, 0,servo_period_micro, 0,100)
    return pwm

def SetAngle(angle, pin, pwm):
    duty = calculate_duty_cycle(angle)
    GPIO.output(pin, True)
    print(angle, duty)
    pwm.ChangeDutyCycle(duty)
    sleep(0.25)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)

    
def GPIOtest(servopin):
    frequency = 50
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servopin,GPIO.OUT)
    GPIO.output(servopin, GPIO.LOW)
    #servo expects a pusle every 20 milliseconds
    pwm = GPIO.PWM(servopin, frequency)
    pwm.start(0)
    
    for i in range(0,181, 30):
        SetAngle(i, servopin, pwm)
    pwm.stop()
    GPIO.cleanup()

def SERVOtest(servopin):

    servo = Servo(servopin)
    for i in range(0,181,30):
        v = map(i,0,180,-1,1)
        servo.value = v
        sleep(0.25)
    servo.value=None

servopin = 17

# GPIOtest(servopin)


ser = Servo(17, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

print(ser.min_pulse_width)
print(ser.max_pulse_width)


while True:
    i = int(input())
    v = map(i,0,180,-1,1)
    print(v)
    ser.value = v
    sleep(1)
    ser.value=None
    
    