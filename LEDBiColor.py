#!/usr/bin/python

##########################   LED MATRIX INTERFACE  ##########################


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

RED = PORTB
GREEN = PORTA
YELLOW = PORTA
ledColor = GREEN
def initialise():
    # Set all 16 pins to be output
    bus.write_byte_data(ADDRR,DIRA,0x00)   # All outputs on PortA address 0x20
    bus.write_byte_data(ADDRR,DIRB,0x00)   # All outputs on PortB address 0x20
    bus.write_byte_data(ADDRC,DIRA,0x00)   # All outputs on PortA address 0x21 - green
    bus.write_byte_data(ADDRC,DIRB,0x00)   # All outputs on PortB address 0x21 - red
    bus.write_byte_data(ADDRR,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)



def turnOnColumn(color,column):
    # Turn on one column with specific color - either green,red or yellow
    bus.write_byte_data(ADDRR,PORTB,0xFF)
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))

def turnOnRow(color,row):
    # Turn on one row with specific color - either green,red or yellow    
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,0x00) 
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRR,PORTB,1<<row)
    


def turnOnLed(color,row,column):
    # Turn on individual LED with a specific color - green,red ot yellow
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTB,1<<row)
    

def turnOnAll(color):
    # Turn on all LEDs
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,0x00)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)    
    bus.write_byte_data(ADDRR,PORTB,0xFF)

def turnOffAll(color):
    # Turn off all LEDs
    bus.write_byte_data(ADDRR,PORTB,0xFF)
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    
    
def turnOffLed(color,row,column):
    # Turn off individual LED with a specific color - green,red or yellow
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTB,1<<row)
    
    
def turnOnLeds(color,row,column):
    # Turn on individual LED with a specific color - green,red or yellow
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,column)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,column)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,column)
        bus.write_byte_data(ADDRC,PORTA,column)
    bus.write_byte_data(ADDRR,PORTB,1<<row)

def multiplexing(patternGreen,patternRed, count):
    for count in range(0,count):
        for row in range(0,8):
            turnOnLeds(GREEN,row,patternGreen[row])
            turnOnLeds(RED,row,patternRed[row])

def multiplexingText(color,pattern,count):
    if color == RED:
        for count in range(0,count):
            for row in range(0,8):
                turnOnLeds(RED,row,pattern[row])
    if color == GREEN:
        for count in range(0,count):
            for row in range(0,8):
                turnOnLeds(GREEN,row,pattern[row])
    if color == YELLOW:
        for count in range(0,count):
            for row in range(0,8):
                turnOnLeds(YELLOW,row,pattern[row])


def displayText():
    color = raw_input("Choose the color of your text - green,red or yellow")
    text = raw_input("Enter some text to display:")
    for char in text:
        pattern = font8x8.font8x8[ord(char)]
        multiplexingText(color,pattern,100)

def charImage(character):
    index = ord(character)
    image = list(font8x8.font8x8[index])
    return image

def scroll(pattern,bufferText):
    for row in range(0,8):
        pattern[row] >>= 1
        if bufferText[row] & 0x01:
            pattern[row] |= 0x80
        bufferText[row] >>= 1

def textScroll(ledColor,text):
    speed = 10
    pattern = [0,0,0,0,0,0,0,0]
    for char in text:
        bufferText = charImage(char)
        for shiftCount in range(0,8):
            multiplexingText(ledColor,pattern,speed)
            scroll(pattern,bufferText)



bus = smbus.SMBus(1)
initialise()

bus.write_byte_data(ADDRR,PORTB,0xFF)
bus.write_byte_data(ADDRR,PORTA,0xFF)  
bus.write_byte_data(ADDRR,PORTB,0xFF)
#turnOnAll(RED)
#time.sleep(0.5)
#turnOffAll(RED)
#time.sleep(0.5)
turnOnAll(RED)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)

#turnOnRow(RED,1)
#time.sleep(0.5)
#turnOffAll(RED)
#time.sleep(0.5)
#for row in range(0,8):
turnOnRow(RED,2)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)
turnOnRow(RED,1)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)
    

#turnOnColumn(RED,0)
#time.sleep(0.5)
#turnOffAll(RED)
#time.sleep(0.5)
turnOnColumn(RED,0)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)

#turnOnColumn(RED,1)
#time.sleep(0.5)
#turnOffAll(RED)
#time.sleep(0.5)
turnOnColumn(RED,1)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)


turnOnLed(RED,1,0)
time.sleep(0.5)
#turnOnLed(RED,1,0)
time.sleep(0.5)
turnOnLed(RED,2,0)
time.sleep(0.5)
#turnOnLed(RED,1,1)
time.sleep(0.5)
turnOnLed(RED,1,1)
time.sleep(0.5)
turnOnLed(RED,2,1)
time.sleep(0.5)

turnOffAll(RED)

patternGreen = [0xFD,0xEF,0x00,0x00,0x00,0x00,0x00,0x00]
patternRed = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]


multiplexing(patternGreen,patternRed,100)

#char = raw_input("Enter a character to display:")
#patternGreen = font8x8.font8x8[ord(char)]
#print char,patternGreen
#multiplexing(patternGreen,patternRed,100)

if len(sys.argv) > 2:
    ledColor = sys.argv[1]
    text = sys.argv[2]
else:
    print "Enter text to display and then press (Ctrl-D)."
    text = sys.stdin.read()

textScroll(ledColor,text)
print "Finished"
