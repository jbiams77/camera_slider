from RPi import GPIO
from Stepper.Stepper import Stepper
'''
This class is used to drive the menus with three buttons, up, select, down. 
The pins are hardwired into these three buttons and cannot be changed. This class
contains the menu display.
'''

class Button:
    #default constructor that initializes 
    def __init__(self, menu=None):
        self.up = 7
        self.select = 16
        self.down = 18
        self.menu = None
        self.upLastState = None
        self.selectLastState = None
        self.downLastState = None
        self.menuOption = 0
        self.s1 = Stepper()
        self.s1.eigthStep()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.select, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if menu is not None:
            self.set_menu(menu)

    def set_menu(self, menu):
        self.menu = menu
        GPIO.add_event_detect(self.up, GPIO.RISING, callback=self.__up, bouncetime=400)
        GPIO.add_event_detect(self.select, GPIO.RISING, callback=self.__button, bouncetime=400)
        GPIO.add_event_detect(self.down, GPIO.RISING, callback=self.__down, bouncetime=400)
        self.upLastState = GPIO.input(self.up)
        self.selectLastState = GPIO.input(self.select)
        self.downLastState = GPIO.input(self.down)


    def __up(self, channel):
        # print('up')
        self.menu.change(-1)

    def __down(self, channel):
        # print('down')
        self.menu.change(1)

    def __button(self, channel):
        # print('select')
        self.menu.select()
