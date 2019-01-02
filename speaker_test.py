import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


SPEAKER = 24

GPIO.setup(SPEAKER, GPIO.OUT)

while True:
    GPIO.output(SPEAKER, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(SPEAKER, GPIO.LOW)
    time.sleep(.5)


