# RaspberryPiEpq

## Simple Component Tests:

### Basic GPIO outputs

```python
pin = RPi.GPIO.setup(pin_number, GPIO.OUT)
GPIO.output(pin_number, GPIO.LOW)  # Send a 0 or Low Signal
GPIO.output(pin_number, GPIO.HIGH) # Send a 1 or High Signal
```

### Servos and Pulse Width Modulation Output

Need for Pulse Width Modulation for Servo
```python
pwm = RPi.GPIO.PWM(pin_number, frequency)
pwm.ChangeDutyCycle(duty)
```   
I also found a utility class ```gpiozero.Servo``` class.
https://gpiozero.readthedocs.io/en/stable/api_output.html
Note that my Servo needed a range of 500 to 2500 microseconds

```python
from gpiozero import Servo
servo = Servo(pin_number, initial_value = 0, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)
servo.value = v # Between -1 and 1 for a 180 degree movement range
```

### Potentiometers, Analog to Digital Converters and the I2C Protocol
I learned there was 3 different Bus Protocols - UART, SPI and I2C
The busio library controls these: https://pypi.org/project/ADS1x15-ADC/

I2C Bus Protocol https://en.wikipedia.org/wiki/I%C2%B2C:
https://www.robot-electronics.co.uk/i2c-tutorial
Half Duplex

```python
import board
import busio      
i2c = busio.I2C(board.SCL,board.SDA)
```
I bought some ADS1115 Analog to Digital Converters
Documentation here: https://pypi.org/project/ADS1x15-ADC/

```python
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c,address=0x48)
pot = AnalogIn(ads, ADS.P0)
print(pot.voltage, v)
```


## 3D Printing First Attempt:
I decided to test my servos on a robot arm. I found this model online:
https://www.thingiverse.com/thing:1684471

It came in two parts - an arm and a controller. I only wanted the arm. It is a very simple model so was excellent for starting to understand how the motors work together. It has 4 servos:
- a rotating on for the based
- two arm joints
- a gripper

I learned about 3D printing. I have a Creality Ender 3 v3 printer. I am using a 0.4mm nozzle and PLA filamnent. I knew a bit about this from before as I did my Design and Technology GCSE with 3D printed parts

In the beginning, the base of the model wouldn't print. The main issue was that the first layer was not sticking to the base. I tried:
* releveling and recalibrating the printer
* cleaning the nozzle. I replaced it and put it back
* changing the temperature of the nozzle and the bed for the PLA
In the end, the thing that seems to help the most was increasing the thickness of the first layer from 0.2mm to 0.4mm

## Assembling the model
### Learning about RCA plugs
In order to fit the servo motors into the frame, I had to remove the RCA plugs and put them back on again. The plugs have a small black clip for each wire. If you lift that, you can pull the wire out and then push them back to replace them.

I needed to buy some M3 bolts and screws to secure the servos, and some glue to keep things together.
I have set up one potentiometer per servo motor. Currently I have 3 working.
I need to think about the cable maintanance as there are a lot of wires coming out of the arm and into the servos

### Testing the model
I created a circuit that used:
- One potentiometer per servo
- The potentiometers were wired into 4 channels of my analog to digital converter (ADC)
- The ADC was wired into the Raspberry Pi IDC pins
- Each servo had a Pulse Width Modulation Output Pin going into it
The program simply had a loop that read the voltages of the ADC inputs (range of 0-3.3 V), and set the pulse widths to match (range of -1 to 1) using a map and clamp function I created

## Setting up mac with raspberry Pi

### Working directly on the raspeberry pi
In the beggining I was working directly on the raspberry pi plugging a monitor, mouse and keyboard into the raspberry pi's ports. Using this I can control the raspberry pi with my mouse and keyboard.
I was using the thonny editor on the raspberry pi. This was tedius because of all the setup every time. It was also very slow and difficult to type with with the lag.

I wanted to try to set it up so I can connect remotely to the rasperry pi.
In order to do this I needed to:
* allow SSH to the raspberry pi
* connect the raspeberry pi to the same network as the computer
* mount the raspberry pi drive on my mac using macFuse and SSHFS

### Enabling SSH
SSH stands for secure shell which needs to be running on the raspberry pi so other computers can connect to it, I turned this on on the raspberry pi settings

If we create a public/private key pair we can SSH without need the password every time
On your Mac, generate an SSH key (if you don’t already have one):
```ssh-keygen -t rsa -b 4096 -C "your_email@example.com"```

Copy the key to the Raspberry Pi:
```ssh-copy-id admin@192.168.86.250```

This saves your public key on the Pi so you don’t have to type a password.
Now, SSH without a password!
ssh admin@192.168.86.250

```ssh admin@192.168.86.250 "python3 /home/admin/src/RaspberryPiEpq/simpleLED.py"```

### Mounting the drive
```sshfs admin@192.168.86.250:/home/admin ~/mnt/pi -o reconnect,allow_other```

Unmounting
```umount ~/mnt/pi``` 

### Creating a Build System in Sublime Text

In Sublime Text, you can create a build system that runs your own commands when you press Cmd^B

In my setup this will run the current python file

```
    "shell_cmd": "ssh admin@192.168.86.250 \"python3 /home/admin/src/RaspberryPiEpq/${file_name}\"",
    "working_dir": "$file_path",
    "selector": "source.python"
}

```

