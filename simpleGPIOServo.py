import RPi.GPIO as GPIO
import time

def map(value, in_min, in_max, out_min, out_max):
    return ((out_max-out_min) * (value-in_min))/(in_max-in_min) + out_min

def calculate_duty_cycle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    servo_min_micro = 500
    servo_max_micro = 2500
    #the pulse width is lerped between the min (500) and max (2500) for a range of 180 degrees
    pulse_width_micro = map(angle, 0, 180, servo_min_micro, servo_max_micro)

    #with a frequency of 50Hz the period is 20ms which is 20000 microseconds 
    servo_period_micro = 20000
    duty_value = map(pulse_width_micro, 0,servo_period_micro, 0,100)
    print(angle, pulse_width_micro, duty_value)
    return duty_value

def SetAngle(angle, pin, pwm):
    duty = calculate_duty_cycle(angle)
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.25)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)

def GPIOtest(servopin):
    frequency = 50
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servopin,GPIO.OUT)
    GPIO.output(servopin, GPIO.LOW)
    #servo expects a pusle every 20 milliseconds
    pwm_pin = GPIO.PWM(servopin, frequency)
    pwm_pin.start(0)
    for angle in range(0, 180, 10):
        SetAngle(angle, servopin, pwm_pin)
    SetAngle(0, servopin, pwm_pin)
    pwm_pin.stop()
    GPIO.cleanup()


testPin = 12
GPIOtest(12)