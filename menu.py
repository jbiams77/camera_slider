import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import threading
import enum

GPIO.setwarnings(False)
#UP = 18
#DOWN = 12
#SELECT = 16
UP = 24
DOWN = 18
SELECT = 23


class MenuType(enum.Enum):
    MENU_LIST = 0
    NUMERIC = 1
    OPTION = 2

class MenuNode(object):
    def __init__(self, name, menu_type, parameter_key=None, children=None):
        self.name = name
        self.parent = None
        self.children = []
        self.menu_type = menu_type
        self.parameter_key = parameter_key
        if parameter_key is not None:
            # Cannot have parameter keys for menu lists
            assert self.menu_type != MenuType.MENU_LIST
        if children is not None:
            for child in children:
                self.add_child(child)
                child.parent = self

    def add_child(self, node):
        # Can only add other MenuNode and only into MENU_LIST
        assert isinstance(node, MenuNode)
        assert self.menu_type == MenuType.MENU_LIST
        self.children.append(node)

class MenuSystem(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        # SPI Config
        DC = 23
        SPI_PORT = 0
        SPI_DEVICE = 0

        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

        GPIO.setup(UP, GPIO.IN)
        GPIO.setup(DOWN, GPIO.IN)
        GPIO.setup(SELECT, GPIO.IN)

        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Load default font.
        
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
        self.large_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 24)

        self.font_width = self.font.getsize("g")[0]
        self.font_height = self.font.getsize("g")[1]

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.display_udpated = False

        self.menu_tree = MenuNode("Main Menu", MenuType.MENU_LIST, None, [
            MenuNode("Config 1", MenuType.MENU_LIST, None, [
                MenuNode("Test 1", MenuType.NUMERIC, "test_1"),
                MenuNode("Test 2", MenuType.NUMERIC, "test_2"),
                MenuNode("Test 3", MenuType.NUMERIC, "test_1"),
            ]),
            MenuNode("Config 2", MenuType.NUMERIC)
        ])

        self.parameters = {
            "test_1": 0,
            "test_2": 50,
        }
        
    def run(self):
        print('Thread #%s started' % self.ident)
        carrot_index = 0
        current_node = self.menu_tree
        self.display_node(current_node)

        while not self.shutdown_flag.is_set():
            button_up = GPIO.input(UP)
            button_down = GPIO.input(DOWN)
            button_select = GPIO.input(SELECT)

            if current_node.menu_type == MenuType.MENU_LIST:
                if button_up == True:
                    if carrot_index > 0:
                        carrot_index -= 1
                        self.update_carrot(carrot_index)
                    elif current_node.parent is not None:
                        current_node = current_node.parent
                        self.display_node(current_node)
                        carrot_index = 0
                if button_down == True and carrot_index < len(current_node.children) - 1:
                    carrot_index += 1
                    self.update_carrot(carrot_index)
                if button_select == True and len(current_node.children) > 0:
                    current_node = current_node.children[carrot_index]
                    self.display_node(current_node)
                    carrot_index = 0

            elif current_node.menu_type == MenuType.NUMERIC:
                if button_up == True:
                    self.parameters[current_node.parameter_key] += 1
                    self.update_numeric(current_node.parameter_key)
                if button_down == True:
                    self.parameters[current_node.parameter_key] -= 1
                    self.update_numeric(current_node.parameter_key)
                if button_select == True:
                    current_node = current_node.parent
                    self.display_node(current_node)
                    carrot_index = 0


            if self.display_udpated:
                self.disp.image(self.image)
                self.disp.display()
                self.display_udpated = False

            time.sleep(0.1)


        print('Thread #%s stopped' % self.ident)

    def draw_header(self, text):
        text_width = self.font.getsize(text)[0]

        # Can only fit 127 pixels
        if text_width > self.width:
            text = "TEXT TOO LONG"
            text_width = self.font.getsize(text)[0]

        # Draw a black filled box to clear the header
        self.draw.rectangle((0,0,self.width, self.font_height), outline=0, fill=0)

        # Center text
        self.draw.text((self.width/2 - text_width/2, 0), text,  font=self.font, fill=255)
        
        #self.disp.image(self.image)
        #self.disp.display()
    
    def display_node(self, node):
        self.display_udpated = True
        self.draw_header(node.name)
        self.draw.rectangle((self.font_width + 2, 15, self.width, self.height), outline=0, fill=0)
        if node.menu_type == MenuType.MENU_LIST:
            self.update_carrot(0)
            count = 0
            y = 15
            # While there are children, or we've reached the end of the screen
            while count < len(node.children) and y < self.height - self.font_height:
                self.draw.text((self.font_width + 2, y), node.children[count].name,  font=self.font, fill=255)
                y += self.font_height
                count += 1
        elif node.menu_type == MenuType.NUMERIC:
            self.delete_carrot()
            self.update_numeric(node.parameter_key)


    def update_carrot(self, index):
        self.display_udpated = True
        self.delete_carrot()
        self.draw.text((0, 15 + index * self.font_height), '>',  font=self.font, fill=255)
    
    def delete_carrot(self):
        self.display_udpated = True
        self.draw.rectangle((0, 15, self.font_width, self.height), outline=0, fill=0)
    
    def update_numeric(self, parameter_key):
        self.display_udpated = True
        self.draw.rectangle((self.font_width + 2, 15, self.width, self.height), outline=0, fill=0)
        self.draw.text((self.font_width + 2, 17), str(self.parameters[parameter_key]),  font=self.large_font, fill=255)
    
