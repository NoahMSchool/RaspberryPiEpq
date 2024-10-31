import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

blueled = 27
redled = 17

GPIO.setup(blueled, GPIO.OUT)
GPIO.setup(redled, GPIO.OUT)

def blink(p, interval, repeats):
    for r in range(repeats):
        time.sleep(interval)
        GPIO.output(p, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(p, GPIO.LOW)

#blink(blueled, 0.5, 5)
#blink(redled, 0.25, 5)


ledstrip = {0 : 22,
           1 : 13,
           2 : 19,
           3 : 26}
for i in range(4):
    GPIO.setup(ledstrip[i], GPIO.OUT)

def to_binary(num):
    binary = []
    bases = [8,4,2,1]
    for b in bases:
        if num >=b :
            num = num-b
            binary.append(1)
        else:
            binary.append(0)
    
    return binary


def show_num(l, num):
    bin = to_binary(num)
    for i in range(4):
        if bin[i] == 1:
            GPIO.output(l[i], GPIO.HIGH)
        else:
            GPIO.output(l[i], GPIO.LOW)
while True:
    num = input()
    if num == "b":
        blink(blueled, 0.25,4)
    elif num == "r":
        blink(redled, 0.25, 4)
    else:
        show_num(ledstrip, int(num))