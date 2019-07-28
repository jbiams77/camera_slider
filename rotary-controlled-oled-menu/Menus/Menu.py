import os
import threading
import time

from Adafruit import SSD1306
from RPi import GPIO
from PIL import Image, ImageDraw, ImageFont

class Menu:

    def __init__(self, options=[]):
        self.options = options
        self.highlightOption = None
        self.rowCount = 3

        self.oled = SSD1306.SSD1306_128_32(rst=None, gpio=GPIO)
        self.oled.begin()
        self.oled.clear()
        self.oled.display()

        # Load image based on OLED display height.  Note that image is converted to 1 bit color.
        self.HOME = Image.open('HOME.png').convert('1')
        self.ADJUST = Image.open('ADJUST.png').convert('1')
        self.CAMERA = Image.open('CAMERA.png').convert('1')
        self.SETTINGS = Image.open('SETTINGS.png').convert('1')
        self.START = Image.open('START.png').convert('1')

    def set_options(self, options):
        self.options = options
        self.highlightOption = None

    def set_highlight(self, highlight):
        if highlight is None:
            self.highlightOption = None
        elif highlight < 0:
            self.highlightOption = 0
        elif highlight >= len(self.options):
            self.highlightOption = len(self.options) - 1
        else:
            self.highlightOption = highlight

    # def change_highlight(self, by):
    #     self.set_highlight(0 if self.highlightOption is None else self.highlightOption + by)

    # def blank(self, draw=False):
    #     self.draw.rectangle((-1, -1, self.oled.width+1, self.oled.height+1), outline=0, fill=0)
    #     if draw:
    #         self.oled.image(self.image)
    #         self.oled.display()

    # def render(self):
    #     if self.renderThread is None or not self.renderThread.isAlive():
    #         self.renderThread = threading.Thread(target=self.__render)
    #         self.renderThread.start()

    # def __render(self):
    #     self.blank()
    #     self.__build()
    #     self.oled.image(self.image)
    #     self.oled.display()

    # def __build(self):
    #     # adjust the start/end positions of the range
    #     if (self.highlightOption is None) or (self.highlightOption < self.rowCount):
    #         start = 0
    #         end = self.rowCount
    #     elif self.highlightOption >= (len(self.options) - self.rowCount):
    #         end = len(self.options)
    #         start = end - self.rowCount
    #     else:
    #         start = self.highlightOption
    #         end = start + self.rowCount

    #     # draw the menu options
    #     top = 0
    #     for x in range(start, end):
    #         fill = 1
    #         if self.highlightOption is not None and self.highlightOption == x:
    #             self.draw.rectangle([0, top, self.oled.width, top + 11], outline=0, fill=1)
    #             fill = 0
    #         self.draw.text((3, top + 1), self.options[x], font=self.font, fill=fill)
    #         top += 10

