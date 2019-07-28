from time import sleep
from RPi import GPIO

'''
microstep resolution   MODE0   MODE1
      full step          0       0
      half step          1       0
       1/4 step          0       1
       1/8 step          1       1
'''

class Stepper:
    #default constructor that initializes 
    def __init__(self):
        self.DIR =  11        #Direction GPIO pin
        self.STEP = 13        #Step GPIO pin
        self.MODE0 = 19       # MODE 0 and MODE1 are used to set step resolution
        self.MODE1 = 15
        self.step_tracker = 0 #used to maintain position
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.MODE0, GPIO.OUT)
        GPIO.setup(self.MODE1, GPIO.OUT)
        #by default, full step
        GPIO.output(self.MODE0, 0)
        GPIO.output(self.MODE1, 0)

    def fullStep(self):
        GPIO.output(self.MODE0, 0)
        GPIO.output(self.MODE1, 0)
    
    def halfStep(self):
        GPIO.output(self.MODE0, 1)
        GPIO.output(self.MODE1, 0)

    def quarterStep(self):
        GPIO.output(self.MODE0, 0)
        GPIO.output(self.MODE1, 1)

    def eigthStep(self):
        GPIO.output(self.MODE0, 1)
        GPIO.output(self.MODE1, 1)

    def move(self, step_count, speed, direction):
        print("trying to move")
        self.eigthStep()
        GPIO.output(self.DIR, direction)
        if(direction==0):
            mult = -1
        else:
            mult = 1
        for x in range(step_count):
            self.step_tracker = self.step_tracker + (1 * mult)
            print(self.step_tracker)    
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(speed)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(speed)

    def returnToCenter(self):
        self.fullStep() 
        if(self.step_tracker<0):
            GPIO.output(self.DIR, 1)
        else:
            GPIO.output(self.DIR, 0)
        for x in range(self.step_tracker):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(0.01)

    def zero(self):
        self.step_tracker = 0
        



    
