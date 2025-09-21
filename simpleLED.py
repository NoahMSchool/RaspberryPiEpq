import RPi.GPIO as GPIO
import time

green = 27
red = 17
blue = 22
cycles = 50
delay = 1

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO17 as an output pin
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)


for i in range(cycles):
    print("on")
    # Turn on the LED
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.HIGH)
    
    GPIO.output(red, GPIO.LOW)
    # Wait for 5 seconds
    time.sleep(delay)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(blue, GPIO.LOW)
    GPIO.output(red, GPIO.HIGH)
    print("offfffff")
    time.sleep(delay)
# Clean up the GPIO settings
GPIO.cleanup()
c = 27


