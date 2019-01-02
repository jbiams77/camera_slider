import RPi.GPIO as GPIO   
from time import sleep
import PiStepper
GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

m1 = PiStepper.Stepper("STEPPER2")

while True:
    m1.forward(0.01, 1000)