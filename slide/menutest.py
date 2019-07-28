import sys
from time import sleep

from Menus.Menu import MainMenu
from Input.Button import Button

m = MainMenu()
b = Button(**{'menu': m})

while True:
    sleep(1)
