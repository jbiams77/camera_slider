import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


BUTTON1 = 7
BUTTON2 = 16
BUTTON3 = 18
SPEAKER = 24

GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SPEAKER, GPIO.OUT)

def buzz(button):
    print("Button pushed: " + str(button))
    for count in range(1000):
        GPIO.output(SPEAKER, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SPEAKER, GPIO.LOW)
        time.sleep(0.0001)

while True:
    time.sleep(0.5)
    button1_pressed = GPIO.input(BUTTON1)
    button2_pressed = GPIO.input(BUTTON2)
    button3_pressed = GPIO.input(BUTTON3)

    print("--------------")
    print("Button 1: " + str(button1_pressed) + "\nButton 2: " + str(button2_pressed) + "\nButton 3: " + str(button3_pressed))


    # if button1_pressed == True:
    #     buzz("UP:4")
    # if button2_pressed == True:
    #     buzz("SELECT:23")
    # if button3_pressed == False:
    #     buzz("DOWN:24")

