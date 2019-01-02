import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

TRIGGER = 22
BUTTON = 12
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)

while True:
    button_in = GPIO.input(BUTTON)
    if button_in == True:
        print('Button Pressed')
        GPIO.output(TRIGGER, GPIO.HIGH)
        time.sleep(0.2)
    GPIO.output(TRIGGER, GPIO.LOW)
