import pywapi
import string


import smbus
import time
import sys
import font8x8

ADDRR = 0x20   # I2C bus address of the 23017 Rows
ADDRC = 0x21   # I2C bus address of the 23017 Columns
DIRA  = 0x00   # PortA I/O direction
DIRB  = 0x01   # PortB I/O direction
PORTA = 0x12   # PortA data register
PORTB = 0x13   # PortB data register

RED = 1
GREEN = 2
YELLOW = 3
ledColor = 1
def initialise():
    # Set all 16 pins to be output
    bus.write_byte_data(ADDRR,DIRA,0x00)   # All outputs on PortA address 0x20
    bus.write_byte_data(ADDRR,DIRB,0x00)   # All outputs on PortB address 0x20
    bus.write_byte_data(ADDRC,DIRA,0x00)   # All outputs on PortA address 0x21 - green
    bus.write_byte_data(ADDRC,DIRB,0x00)   # All outputs on PortB address 0x21 - red
    bus.write_byte_data(ADDRR,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)

def turnOffAll():
    # Turn off all LEDs
    bus.write_byte_data(ADDRR,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)


def multiplexingText(color,pattern,count):
    if color == GREEN:
        for count in range(0,count):
            for row in range(0,8):
                turnOnLeds(GREEN,row,pattern[row])
                time.sleep(0.0003)
    elif color == YELLOW:
        for count in range(0,count):
            for row in range(0,8):
                turnOnLeds(YELLOW,row,pattern[row])
                time.sleep(0.0003)
    else:
        for count in range(0,count):
            for row in range(0,8):
                turnOnLeds(RED,row,pattern[row])
                time.sleep(0.0003)

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

def turnOnLeds(color,row,column):
    # Turn on individual LED with a specific color - green,red or yellow
    if color == RED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,~column)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,~column)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~column)
        bus.write_byte_data(ADDRC,PORTA,~column)
    bus.write_byte_data(ADDRR,PORTA,1<<row)


bus = smbus.SMBus(1)
initialise()
ledColor = GREEN

location = pywapi.get_location_ids('London')
#print location
weather_com_result = pywapi.get_weather_from_weather_com('44418')
string1 = "Weather.com says: It is " + string.lower(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + "C now in New York."
textScroll(int(ledColor),string1)

ledColor = RED
yahoo_result = pywapi.get_weather_from_yahoo('10001')
string2 = "Yahoo says: It is " + string.lower(yahoo_result['condition']['text']) + " and " + yahoo_result['condition']['temp'] + "C now in New York."
textScroll(int(ledColor),string2)

print "Weather.com says: It is " + string.lower(weather_com_result['current_conditions']['text']) + " and " + weather_com_result['current_conditions']['temperature'] + "C now in New York.\n\n"

print "Yahoo says: It is " + string.lower(yahoo_result['condition']['text']) + " and " + yahoo_result['condition']['temp'] + "C now in New York.\n\n"


