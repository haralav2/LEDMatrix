#!/usr/bin/python

import smbus
import time

# Definitions for the MCP23017 chip
ADDR  = 0x20
DIRA  = 0x00
DIRB  = 0x01
PORTA = 0x12
PORTB = 0x13

def Init():
    # Set up the chip for 16 output pins
    bus.write_byte_data(ADDR,DIRA,0x00);
    bus.write_byte_data(ADDR,DIRB,0x00);

def TurnOnLED(row,column):
    # Turn on one LED at (row,col). All other LEDS are off.
    bus.write_byte_data(ADDR,PORTA,0x80>>col);
    bus.write_byte_data(ADDR,PORTB,~(1<<row));

def TurnOffLED(row,column):
    # Turn off one LED at (row,col). All other LEDS are off.
    bus.write_byte_data(ADDR,PORTA,0x00>>col);
    bus.write_byte_data(ADDR,PORTB,~(1<<row));

def TurnOnColumn(col):
    # Turn on one column from the matrix
    bus.write_byte_data(ADDR,PORTB,0x00);
    bus.write_byte_data(ADDR,PORTA,0x80>>col);

def TurnOnRow(row):
    # Turn on one row from the matrix
    bus.write_byte_data(ADDR,PORTA,0xFF);
    bus.write_byte_data(ADDR,PORTB,~(1<<row));

def TurnOnAll():
    # Turn on all LEDs
    bus.write_byte_data(ADDR,PORTA,0xFF);
    bus.write_byte_data(ADDR,PORTB,0x00);

def TurnOfAll():
    # Turn off all LEDs
    bus.write_byte_data(ADDR,PORTA,0x00);
    bus.write_byte_data(ADDR,PORTB,0x00);

def FlashLED(row,column):
    # Flash one LED at (row,column).
    TurnOnLED(row,column)
    time.sleep(1)
    TurnOffLED(row,column)
    time.sleep(1)

def FlashAll(delay):
    # Flash all Leds in the matrix
    TurnOnAll()
    time.sleep(delay)
    TurnOffAll()
    time.sleep(delay)

def FlashAllCons(delay):
    # Flash all Leds one after the other
    for row in range(0,8):
        for column in range(0,8):
            TurnOnLED(row,column)
            time.sleep(delay)
            TurnOffLED(row,column)
            time.sleep(delay)
            
    
    
    
