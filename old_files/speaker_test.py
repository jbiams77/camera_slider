import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


SPEAKER = 23

FAN = 37

GPIO.setup(SPEAKER, GPIO.OUT)
GPIO.setup(FAN, GPIO.OUT)

GPIO.output(FAN, GPIO.HIGH)

while True:
    for count in range(1000):
        GPIO.output(SPEAKER, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SPEAKER, GPIO.LOW)
        time.sleep(0.0001)
    time.sleep(0.5)