#!/usr/bin/python

import smbus
import time
import sys
import font8x8
import Bicolour_Interface

# Definitions for the MCP23017
ADDRR = 0x20   # I2C bus address of the 23017 Rows
ADDRC = 0x21   # I2C bus address of the 23017 Columns
DIRA  = 0x00   # PortA I/O direction
DIRB  = 0x01   # PortB I/O direction
PORTA = 0x12   # PortA data register
PORTB = 0x13   # PortB data register

colour = 1

bus = smbus.SMBus(1)
Bicolour_Interface.initialise()

# Greet the user 
greeting = "Hello!What's your name?\n"
print greeting
Bicolour_Interface.textScroll(colour,greeting)

name = sys.stdin.read()
nameAndGreeting = "\nHello " + name + "I am PiLight!"
print nameAndGreeting
Bicolour_Interface.textScroll(colour,nameAndGreeting)

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
        Bicolour_Interface.textScroll(colour,text)
        print "\nDo you wish to enter more text?"
        text = sys.stdin.read()
        if (text == "yes\n" or text == "y\n"):
            
            continuing = True
        else:
            continuing = False

print "\nFinished"

