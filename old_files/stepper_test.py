import RPi.GPIO as GPIO   
from time import sleep

GPIO.setmode(GPIO.BOARD)

DIR = 11   # Direction GPIO Pin
STEP = 13  # Step GPIO Pin
M0_1 = 19   # Direction GPIO Pin
M1_1 = 15  # Step GPIO Pin


GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(M0_1, GPIO.OUT)
GPIO.setup(M1_1, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, 1)

GPIO.output(M0_1, 1)
GPIO.output(M1_1, 1)

delay = .0001

try:
    while True:
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
finally:
    GPIO.cleanup()