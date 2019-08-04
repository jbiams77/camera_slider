import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
#image = Image.new('1', (width, height))
image = Image.open('START.png').convert('1')

top = 16
bottom = 64
delta = bottom - top
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,top,width,delta), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,top,width,delta), outline=0, fill=0)
    draw.text((x, top), "IP: hello world" ,  font=font, fill=255)
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
