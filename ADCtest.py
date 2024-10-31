import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
'''
import smbus
ADDR = 0x48
bus = smbus.SMBus(1)
try:
    config = bus.read_word_data(ADDR, 0x01)
    print("good")
except OSError as e:
    print(f"bad: {e}")
'''
i2c = busio.I2C(board.SCL,board.SDA)

ads = ADS.ADS1115(i2c,address=0x4a)
ads.gain = 1

ch0 = AnalogIn(ads, ADS.P0)
ch1 = AnalogIn(ads, ADS.P1)

while True:
        print(f"Voltage: {ch0.voltage}V {ch1.voltage}V ")
        time.sleep(0.5)
print("hello")

'''
Notes:
Discovered a Pico can read Analog signals but a RPi 4 and 5 cannot
You need an analog to digital converter to read analog
I bought a pack of ADS115 modules
I instannled the Adafruit ADS1115 software
My software did not recognise the input - got an error saying I2C not enabled
I enabled I2C - this is a 2 wire one way communication protocol that used GPIO2 and GPIO3 as
SCL (clock) and SDA (data)
Even after that it still didn't work
I learned about the terminal program i2cdetect which helps troubleshoot this
Running this shows the i2c buses: sudo i2cdetect -l
It found this: i2c-1	i2c       	bcm2835 (i2c@7e804000)  

Running this finds devices:
sudo i2cdetect -y 1 0x45 0x4F

I spent hours making sure the wiring was correct. I learned that with soldering my header pins onto
the module it didn't work.

Once it was properly soldered. it works

The module has 4 channels
It can also be configure to have 4 addresses so you can have 4 of them talking on the SPI

'''


