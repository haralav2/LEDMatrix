#!/usr/bin/python

################# BICOLOUR LED MATRIX LIBRABY ##########################

import smbus
import time
import sys
import font8x8


# Definitions for the MCP23017
ADDRR = 0x20   # I2C bus address of the 23017 Rows
ADDRC = 0x21   # I2C bus address of the 23017 Columns
DIRA  = 0x00   # PortA I/O direction
DIRB  = 0x01   # PortB I/O direction
PORTA = 0x12   # PortA data register
PORTB = 0x13   # PortB data register
bus = smbus.SMBus(1)

BRIGHTRED    = (255,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
BRIGHTYELLOW = (255, 255,   0)
ledColour = 1

''' Set all 16 pins to be output '''
def initialise():
    # All outputs on PortA address 0x20
    bus.write_byte_data(ADDRR,DIRA,0x00)
    
    # All outputs on PortB address 0x20
    bus.write_byte_data(ADDRR,DIRB,0x00)
    
    # All outputs on PortA address 0x21 - green
    bus.write_byte_data(ADDRC,DIRA,0x00)
    
    # All outputs on PortB address 0x21 - red
    bus.write_byte_data(ADDRC,DIRB,0x00)

    # Set all low
    bus.write_byte_data(ADDRR,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)

''' Turn on one column with specific colour -
    either green,red or yellow
'''
def turnOnColumn(colour,column):
    if colour == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif colour == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif colour == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,0xFF)

''' Turn on one row with specific colour -
    either green,red or yellow
'''
def turnOnRow(colour,row):   
    if colour == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,0x00) 
    elif colour == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif colour == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRR,PORTA,1<<row)
    

''' Turn on individual LED with a specific color -
    green,red ot yellow
'''
def turnOnLed(colour,row,column):
    if colour == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif colour == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif colour == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,1<<row)
    

''' Turn on all LEDs '''
def turnOnAll(colour):
    if colour == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,0x00)
    elif colour == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif colour == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)    
    bus.write_byte_data(ADDRR,PORTA,0xFF)

''' Turn off all LEDs '''
def turnOffAll():
    bus.write_byte_data(ADDRR,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)


''' Turn off individual LED with a specific color -
    green,red or yellow
'''     
def turnOffLed(colour,row,column):    
    if colour == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    elif colour == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    elif colour == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,1<<row)
    

''' Turn on LEDs with a specific color -
    green,red or yellow
'''   
def turnOnLeds(colour,row,column):   
    if colour == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,~column)
    elif colour == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,~column)
    elif colour == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,~column)
        bus.write_byte_data(ADDRC,PORTA,~column)
    bus.write_byte_data(ADDRR,PORTA,1<<row)


''' Going through all the rows quickly to create the
    illusion of a static image
'''
def multiplexingText(colour,pattern,count):
    if colour == "2\n" or colour == "green\n" \
       or colour == "2" or colour == "green":
        
        for count in range(0,count):
            for row in range(0,8):
                bus.write_byte_data(ADDRC,PORTB,0xFF)
                bus.write_byte_data(ADDRC,PORTA,~pattern[row])
                bus.write_byte_data(ADDRR,PORTA,1<<row)                
                turnOffAll()
    elif colour == "3\n" or colour == "yellow\n" \
         or colour == "3" or colour == "yellow":
        
        for count in range(0,count):
            for row in range(0,8):
                bus.write_byte_data(ADDRC,PORTA,~pattern[row])
                bus.write_byte_data(ADDRC,PORTB,~pattern[row])
                bus.write_byte_data(ADDRR,PORTA,1<<row)
                turnOffAll()
    else:
        for count in range(0,count):
            for row in range(0,8):
                bus.write_byte_data(ADDRC,PORTA,0xFF)
                bus.write_byte_data(ADDRC,PORTB,~pattern[row])
                bus.write_byte_data(ADDRR,PORTA,1<<row)                
                turnOffAll()                    
    time.sleep(0.0002)


''' Multiplexing images '''
def multiplexing(patternGreen,patternRed,patternYellow,count):
    for count in range(0,count):
        for row in range(0,8):
            bus.write_byte_data(ADDRR,PORTA,0x00)
            greenOrYellow = patternGreen[row]|patternYellow[row]
            bus.write_byte_data(ADDRC,PORTA,~greenOrYellow)
            redOrYellow = patternRed[row]|patternYellow[row]
            bus.write_byte_data(ADDRC,PORTB,~redOrYellow)
            bus.write_byte_data(ADDRR,PORTA,1<<row)
            time.sleep(0.0002)

''' Scrolling a pattern '''
def scroll(pattern,bufferText):
    for row in range(0,8):
        pattern[row] >>= 1
        if bufferText[row] & 0x01:
            pattern[row] |= 0x80
        bufferText[row] >>= 1


''' Using the font display the text on the matrix '''
def textScroll(ledColour,text,speed=8):
    pattern = [0,0,0,0,0,0,0,0]
    for character in text:
        bufferText = list(font8x8.font8x8[ord(character)])
        for count in range(0,8):
            multiplexingText(ledColour,pattern,speed)
            scroll(pattern,bufferText)

''' Function used to turn off all the Leds, but instead of
    setting everything to low, setting it to high achieves
    the same effect
'''
def turnOffAllAudio():
    bus.write_byte_data(ADDRC,PORTA,0xFF)
    bus.write_byte_data(ADDRC,PORTB,0xFF)
    bus.write_byte_data(ADDRR,PORTA,0xFF)

''' Turn on a specific column red with spesific number of rows'''
def setColumnRed(row,column):
    bus.write_byte_data(ADDRR,PORTA,(1<<row)-1)
    bus.write_byte_data(ADDRC,PORTA,0xFF)
    bus.write_byte_data(ADDRC,PORTB,~(1<<column))

''' Turn on a specific column green '''
def setColumnGreen(row,column):
    bus.write_byte_data(ADDRR,PORTA,(1<<row)-1)
    bus.write_byte_data(ADDRC,PORTB,0xFF)
    bus.write_byte_data(ADDRC,PORTA,~(1<<column))

''' Turn on a specific column yellow '''
def setColumnYellow(row,column):
    bus.write_byte_data(ADDRR,PORTA,(1<<row)-1)
    bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    bus.write_byte_data(ADDRC,PORTA,~(1<<column))
   
