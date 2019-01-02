import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

UP = 18
DOWN = 12
SELECT = 16

GPIO.setup(UP, GPIO.IN)
GPIO.setup(DOWN, GPIO.IN)
GPIO.setup(SELECT, GPIO.IN)


while True:
    button_up = GPIO.input(UP)
    button_down = GPIO.input(DOWN)
    button_select = GPIO.input(SELECT)
    
    if button_up == True:
        print('Up Pressed')
    if button_down == True:
        print('Down Pressed')
    if button_select == True:
        print('Select Pressed')
    time.sleep(0.1)
         
