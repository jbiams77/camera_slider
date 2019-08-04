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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.MODE0, GPIO.OUT)
        GPIO.setup(self.MODE1, GPIO.OUT)
        self.start = False
        # By default, it takes 1 hour to complete a time lapse
        self.timeInHour = 1.0
        self.totalTime = self.timeInHour * (60*60)
        self.stepCount = 6000
        self.speed = self.setSpeed()
        self.stepMode = None
        self.stepTracker = 0 #used to maintain position
        #by default, full step
        self.fullStep()

    def getSetting(self, setting):
        if(setting=="Time"):
            return "" + str(self.timeInHour) + "hr"
        elif(setting=="Step Mode"):
            return "" + self.stepMode
        elif(setting=="Begin"):
            return "" + str(self.start)
        elif(setting=="<<" or setting==">>"):
            return "10cm"
        elif(setting=="<" or setting==">"):
            return "1cm"
        else:
            return "N/A"

    def changeSetting(self, setting, changeBy):
        if(setting=="Step Mode"):
            if(self.stepMode=="Full"):
                if(changeBy==1):
                    self.halfStep()
                else:
                    self.eigthStep()
            elif(self.stepMode=="1/2"):
                if(changeBy==1):
                    self.quarterStep()
                else:
                    self.fullStep()
            elif(self.stepMode=="1/4"):
                if(changeBy==1):
                    self.eigthStep()
                else:
                    self.halfStep()
            else:
                if(changeBy==1):
                    self.fullStep()
                else:
                    self.quarterStep()
        elif(setting=="Time"):
            num = self.timeInHour
            num += changeBy*.25*-1
            if(changeBy==-1 and num<=4):
                self.timeInHour+=.25
            elif(changeBy==1 and num>0):
                self.timeInHour-=.25
        elif(setting=="Begin"):
            self.start = True
            self.move(1)
        elif(setting=="<<"):
            self.speed = .001
            self.fullStep()
            self.stepCount = 10000
            self.move(1)
        elif(setting=="<"):
            self.speed = .001
            self.fullStep()
            self.stepCount = 1000
            self.move(1)
        elif(setting==">>"):
            self.speed = .001
            self.fullStep()
            self.stepCount = 10000
            self.move(0)
        elif(setting==">"):
            self.speed = .001
            self.fullStep()
            self.stepCount = 1000
            self.move(0)


    def setSpeed(self):
        #return self.totalTime/self.stepCount
        return .0001

    def getTime(self):
        return " " + str(self.totalTime) + " min"

    def fullStep(self):
        GPIO.output(self.MODE0, 0)
        GPIO.output(self.MODE1, 0)
        self.stepMode = "Full"
    
    def halfStep(self):
        GPIO.output(self.MODE0, 1)
        GPIO.output(self.MODE1, 0)
        self.stepMode = "1/2"

    def quarterStep(self):
        GPIO.output(self.MODE0, 0)
        GPIO.output(self.MODE1, 1)
        self.stepMode = "1/4"

    def eigthStep(self):
        GPIO.output(self.MODE0, 1)
        GPIO.output(self.MODE1, 1)
        self.stepMode = "1/8"

    def move(self, direction):
        GPIO.output(self.DIR, direction)
        if(direction==0):
            mult = -1
        else:
            mult = 1
        for x in range(self.stepCount):
            self.step_tracker = self.stepTracker + (1 * mult)
            print(self.stepTracker)    
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(self.speed)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(self.speed)
            print(x)

    def returnToCenter(self):
        self.fullStep() 
        if(self.stepTracker<0):
            GPIO.output(self.DIR, 1)
        else:
            GPIO.output(self.DIR, 0)
        for x in range(self.stepTracker):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(0.01)

    def zero(self):
        self.stepTracker = 0
        



    
