#!/usr/bin/python

import smbus
import time
import sys
import font8x8
import Adafruit_8x8Veni

grid = Adafruit_8x8Veni.ColorEightByEight(address=0x70)

colour = 1
# Initialise matrix
grid.clear()

# Greet the user 
greeting = "Hello!What's your name?\n"
print greeting
grid.textScroll(colour,greeting)

name = sys.stdin.read()
nameAndGreeting = "\nHello " + name + "I am PiLight!"
print nameAndGreeting
grid.textScroll(colour,nameAndGreeting)
grid.clear()
continuing = True

if len(sys.argv) > 2:
   ledColor = sys.argv[1]
   text = sys.argv[2]
else:
    while (continuing == True):
        print "\nChoose text color: 1 for red, 2 for green, 3 for yellow."
        colour = sys.stdin.read() 
        print "\nEnter text to display and then press (Ctrl-D)."
        text = sys.stdin.read()
        grid.textScroll(colour,text)
        print "\nDo you wish to enter more text?"
        text = sys.stdin.read()
        if (text == "yes\n" or text == "y\n"):           
            continuing = True
        else:
            continuing = False
text = 'Bye!'
grid.textScroll(colour,text)
grid.clear()
print "\nFinished"

