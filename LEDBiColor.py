#!/usr/bin/python

##########################   LED MATRIX INTERFACE  ##########################


import smbus
import time

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
    # Turn off individual LED with a specific color - green,red ot yellow
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTB,1<<row)
    
    
def turnOnLeds(color,row,column):
    # Turn on individual LED with a specific color - green,red ot yellow
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
            turnOnLeds(GREEN,row,~patternGreen[row])
            turnOnLeds(RED,row,~patternRed[row])

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

patternGreen = [0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00]
patternRed = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

multiplexing(patternGreen,patternRed,1000)
