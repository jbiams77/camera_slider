import os
import threading
import time
from Adafruit import SSD1306
from RPi import GPIO
from PIL import Image, ImageDraw, ImageFont

'''
The following class serves to represent a node of menu objects. 
Each selectable item represents a different menu option with access to these fields.
This still needs to be finished and is currently unused.
'''
class Menu(object):

    def __init__(self, topMenu=None, subMenu=[]):
        self.topMenu = topMenu
        #these submenus allow the user to access menu specific items
        self.subMenu = []
        
'''
This class currently drives the menus. It creates 5 top level menus
based on .png files and works with Button class to move through the 
menu with setMenuOption Function.
'''
class MainMenu:

    def __init__(self, options=[]):
        self.menuOption = 0
        self.RST = 24
        self.oled = SSD1306.SSD1306_128_64(rst=None, gpio=GPIO)

        # self.oled.begin()
        self.oled.clear()
        self.oled.display()
        self.home = Image.open('HOME.png').convert('1')
        self.start = Image.open('START.png').convert('1')
        self.camera = Image.open('CAMERA.png').convert('1')
        self.adjust = Image.open('ADJUST.png').convert('1')
        self.settings = Image.open('SETTINGS.png').convert('1')
        self.refreshDisplay(self.home)

    def refreshDisplay(self, screen):
        # Display image.
        self.oled.image(screen)
        # self.render()
        self.oled.display()

    def setMenuOption(self, menu_num):
        if menu_num%5 == 0:
            print("home ", menu_num)
            self.refreshDisplay(self.home)
        elif menu_num%5 == 1:
            print("start", menu_num)
            self.refreshDisplay(self.start)
        elif menu_num%5 == 2:
            print("camera", menu_num)
            self.refreshDisplay(self.camera)
        elif menu_num%5 == 3:
            print("adjust", menu_num)
            self.refreshDisplay(self.adjust)
        else:
            print("settings", menu_num)
            self.refreshDisplay(self.settings)

    def changeMenu(self, by):
        self.menuOption = self.menuOption + by
        self.setMenuOption(self.menuOption)


