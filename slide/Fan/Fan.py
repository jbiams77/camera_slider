from time import sleep
from RPi import GPIO


class Fan:
    def __init__(self):
        self.FAN =  37        #GPIO Pin connected to BJT that turns fan on/off
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.FAN, GPIO.OUT)
        GPIO.output(self.FAN, 0)

    def turnFanOn(self):
        GPIO.output(self.FAN, 1)

    def turnFanOff(self):
        GPIO.output(self.FAN, 0)

