import RPi.GPIO as GPIO
import time

leds = [27, 17, 22]
button = 2
ledchoice = 1
led = leds[ledchoice]

GPIO.setmode(GPIO.BCM)

# Set LED as an output
GPIO.setup(leds[0], GPIO.OUT)
GPIO.setup(leds[1], GPIO.OUT)
GPIO.setup(leds[2], GPIO.OUT)

# Use a pull-up resistor (default HIGH, press = LOW)
GPIO.setup(button, GPIO.IN)


while True:
    for l in leds:
        GPIO.output(l, GPIO.LOW)
        print(l)
    if GPIO.input(button) == GPIO.HIGH:  # Button pressed
        ledchoice+=1
        ledchoice%=len(leds)
        led = leds[ledchoice]

       # GPIO.output(led, GPIO.HIGH)
    
    time.sleep(0.1)  # Small delay to debounce

GPIO.cleanup