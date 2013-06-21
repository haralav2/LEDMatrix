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
        bus.write_byte_data(ADDRC,PORTB,0<<row)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,0<<row)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0<<row)
        bus.write_byte_data(ADDRC,PORTA,0<<row)
    bus.write_byte_data(ADDRR,PORTB,0xFF)


def turnOnLed(color,row,column):
    # Turn on individual LED with a specific color - green,red ot yellow
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        #bus.write_byte_data(ADDRC,PORTA,0x00)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
        #bus.write_byte_data(ADDRC,PORTB,0x00)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTB,0<<row)

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
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    bus.write_byte_data(ADDRR,PORTB,0xFF)
    
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
    

bus = smbus.SMBus(1)
initialise()

turnOnAll(RED)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)
turnOnAll(GREEN)
time.sleep(0.5)
turnOffAll(GREEN)
time.sleep(0.5)

turnOnRow(RED,1)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)
turnOnRow(GREEN,0)
time.sleep(0.5)
turnOffAll(GREEN)
time.sleep(0.5)

turnOnColumn(RED,0)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)
turnOnColumn(GREEN,0)
time.sleep(0.5)
turnOffAll(GREEN)
time.sleep(0.5)

turnOnColumn(RED,1)
time.sleep(0.5)
turnOffAll(RED)
time.sleep(0.5)
turnOnColumn(GREEN,1)
time.sleep(0.5)
turnOffAll(GREEN)
time.sleep(0.5)

turnOnLed(GREEN,0,0)
time.sleep(0.5)
turnOnLed(RED,1,0)
time.sleep(0.5)
turnOnLed(GREEN,0,1)
time.sleep(0.5)
turnOnLed(RED,1,1)
time.sleep(0.5)

turnOffAll(GREEN)
turnOffAll(RED)
