import os
import threading
import time
from Adafruit import SSD1306
from RPi import GPIO
from PIL import Image, ImageDraw, ImageFont
from Stepper.Stepper import Stepper

stepper = Stepper()

'''
The following class serves to represent a node of menu objects. 
Each selectable item represents a different menu option with access to these fields.
This still needs to be finished and is currently unused.
'''
class Menu(object):

    def __init__(self, image, subMenu = []):
        self.subMenu = subMenu
        self.menuOptions = len(self.subMenu)
        self.RST = 24
        # 128x64 display with hardware I2C:
        self.disp = SSD1306.SSD1306_128_64(rst=None, gpio=GPIO)
        # Initialize library
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        # blue dimenension set text within the blue portion of the OLED
        self.blueWidth = 128
        self.blueHeight = 64-16
        self.blueX = 0
        self.secondColumn = 70
        self.blueY = 16
        #premade settings images for yellow menu bar
        self.image = image
        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)
        # Draw a black filled box to clear the image.
        self.draw.rectangle((self.blueX, self.blueY, self.blueWidth, self.blueHeight), outline=0, fill=0)
        # Load default font
        self.font = ImageFont.load_default()
        self.currentSelection = -1
        self.subMenuSelected = False

    def drawObject(self):
        self.draw.rectangle((self.blueX, self.blueY, self.blueWidth, self.blueHeight), outline=0, fill=0)
        y=self.blueY
        indent = 10
        count = 0
        leftBracket = " "
        rightBracket = " "
        for x in self.subMenu:
            if(count==self.currentSelection):
                indent = 20
                if(self.subMenuSelected==True):
                    leftBracket = "["
                    rightBracket = "]"
            else :
                indent = 10
                leftBracket = " "
                rightBracket = " "
            self.draw.text((self.blueX + indent, y), x,  font=self.font, fill=255)
            self.draw.text((self.secondColumn, y), leftBracket + stepper.getSetting(x) + rightBracket,  font=self.font, fill=255)
            y += 10
            count += 1
        # Display image.
        self.disp.image(self.image)
        self.disp.display()

    def getCurrentSelection(self):
        return self.currentSelection

    def changeCurrentSelection(self, changeBy):
        num = self.currentSelection
        if(num+changeBy<self.menuOptions and num+changeBy>=-1):
            self.currentSelection += changeBy
        self.drawObject()

    def adjustSelection(self, changeBy):
        stepper.changeSetting(self.subMenu[self.currentSelection], changeBy)
        self.drawObject()
    
        
'''
This class currently drives the menus. It creates 5 top level menus
based on .png files and works with Button class to move through the 
menu with setMenuOption Function.
'''
class MainMenu:

    def __init__(self):
        ''' Selection layer determines where the menu is:
           1. TOP MENU:  HOME, START, CAMERA, ADJUST, SETTINGS
           2. SUB-MENU:  The sub-menus of the TOP MENU
           3. SETTINGS:  The adjustable settings of the sub-menus .
        '''
        self.selectionLayer = 0
        self.topMenuSelection = 0
        # array of Menu Class objecs for each menu page
        self.menuArray = []
        self.makeMenu()

    def makeMenu(self):
        self.menuArray.append( Menu(Image.open('HOME.png').convert('1'), ["N/A"]) )
        self.menuArray.append( Menu(Image.open('START.png').convert('1'), ["Begin"]) )
        self.menuArray.append( Menu(Image.open('CAMERA.png').convert('1'), ["N/A"]) )
        self.menuArray.append( Menu(Image.open('ADJUST.png').convert('1'), ["<<", "<", ">", ">>"]) )
        self.menuArray.append( Menu(Image.open('SETTINGS.png').convert('1'), ["Time", "Step Mode"]) )
        self.displayMenu()

    def displayMenu(self):
        self.menuArray[self.topMenuSelection].drawObject()

    def change(self, changeBy):
        if(self.selectionLayer==0):
            self.changeTopMenu(changeBy)
        elif(self.selectionLayer==1):
            if(self.menuArray[self.topMenuSelection].getCurrentSelection()==0 and changeBy==-1):
                print("Up and Out")
                self.selectionLayer=0
            self.menuArray[self.topMenuSelection].changeCurrentSelection(changeBy)
            self.displayMenu()
        else:
            self.menuArray[self.topMenuSelection].adjustSelection(changeBy)


    def changeTopMenu(self, changeBy):
        num = self.topMenuSelection
        if(num+changeBy>=0 and num+changeBy<5):
            self.topMenuSelection+=changeBy
        self.displayMenu()

    def select(self):
        if(self.selectionLayer==0):
            self.menuArray[self.topMenuSelection].changeCurrentSelection(1)
            self.selectionLayer = 1
            self.displayMenu()
        elif(self.selectionLayer==1):
            self.selectionLayer = 2
            self.menuArray[self.topMenuSelection].subMenuSelected = True
            self.displayMenu()
        else:
            self.selectionLayer = 1
            self.menuArray[self.topMenuSelection].subMenuSelected = False
            self.displayMenu()
        