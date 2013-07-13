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

RED = 1
GREEN = 2
YELLOW = 3
ledColor = 1

# Set all 16 pins to be output
def initialise():
    bus.write_byte_data(ADDRR,DIRA,0x00)   # All outputs on PortA address 0x20
    bus.write_byte_data(ADDRR,DIRB,0x00)   # All outputs on PortB address 0x20
    bus.write_byte_data(ADDRC,DIRA,0x00)   # All outputs on PortA address 0x21 - green
    bus.write_byte_data(ADDRC,DIRB,0x00)   # All outputs on PortB address 0x21 - red
    bus.write_byte_data(ADDRR,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)



# Turn on one column with specific color - either green,red or yellow
def turnOnColumn(color,column):
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,0xFF)

# Turn on one row with specific color - either green,red or yellow 
def turnOnRow(color,row):   
    if color == RED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,0x00) 
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRR,PORTA,1<<row)
    

# Turn on individual LED with a specific color - green,red ot yellow
def turnOnLed(color,row,column):
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,1<<row)
    

# Turn on all LEDs
def turnOnAll(color):
    if color == RED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,0x00)
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)    
    bus.write_byte_data(ADDRR,PORTA,0xFF)

# Turn off all LEDs
def turnOffAll():
    bus.write_byte_data(ADDRR,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)


# Turn off individual LED with a specific color - green,red or yellow    
def turnOffLed(color,row,column):    
    if color == RED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
    elif color == GREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    elif color == YELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,1<<row)
    

# Turn on LEDs with a specific color - green,red or yellow    
def turnOnLeds(color,row,column):   
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


# Going through all the rows quickly to create the illusion of a static image
def multiplexingText(color,pattern,count):
    if color == "2\n" or color == "green\n" or color == "2" or color == "green":
        for count in range(0,count):
            for row in range(0,8):
                bus.write_byte_data(ADDRC,PORTB,0xFF)
                bus.write_byte_data(ADDRC,PORTA,~pattern[row])
                bus.write_byte_data(ADDRR,PORTA,1<<row)                
                turnOffAll()
    elif color == "3\n" or color == "yellow\n" or color == "3" or color == "yellow":
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


# Multiplexing images
def fastMultiplexing(patternGreen,patternRed,patternYellow,count):
    for count in range(0,count):
        for row in range(0,8):
            bus.write_byte_data(ADDRR,PORTA,0x00)
            greenOrYellow = patternGreen[row]|patternYellow[row]
            bus.write_byte_data(ADDRC,PORTA,~greenOrYellow)
            redOrYellow = patternRed[row]|patternYellow[row]
            bus.write_byte_data(ADDRC,PORTB,~redOrYellow)
            bus.write_byte_data(ADDRR,PORTA,1<<row)
            time.sleep(0.0002)

# Scrolling a pattern
def scroll(pattern,bufferText):
    for row in range(0,8):
        pattern[row] >>= 1
        if bufferText[row] & 0x01:
            pattern[row] |= 0x80
        bufferText[row] >>= 1


# Using the font display the text on the matrix
def textScroll(ledColor,text):
    speed = 8
    pattern = [0,0,0,0,0,0,0,0]
    for character in text:
        bufferText = list(font8x8.font8x8[ord(character)])
        for count in range(0,8):
            multiplexingText(ledColor,pattern,speed)
            scroll(pattern,bufferText)


################################# Start test ################################

bus = smbus.SMBus(1)
initialise()

patternRed = [ 0x18, 0x3C, 0x3C, 0x18, 0x18, 0x00, 0x18, 0x00]
patternYellow = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternGreen = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
fastMultiplexing(patternGreen,patternRed,patternYellow,50)

# Greet the user 
greeting = "Hello!What's your name?\n"
print greeting
textScroll(ledColor,greeting)

name = sys.stdin.read()
nameAndGreeting = "Hello " + name + "I am PiLight!"
print nameAndGreeting
textScroll(ledColor,nameAndGreeting)

number = 0
while (number < 10):
    for index in range(0,8):
        turnOnLed(RED,0,index)
        time.sleep(0.05)
    for index in range(8,-1,-1):
        turnOnLed(RED,0,index)
        time.sleep(0.05)
    number = number + 1

patternGreen = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternRed = [0x00,0x00,0xEF,0x00,0x00,0x00,0x00,0x00]
patternYellow = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
fastMultiplexing(patternGreen,patternRed,patternYellow,500)

patternGreen = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternRed = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternYellow = [0x00,0x00,0x18,0x3C,0x3C,0x18,0x00,0x00]
fastMultiplexing(patternGreen,patternRed,patternYellow,500)

turnOffAll()
time.sleep(2)

turnOnAll(RED)
time.sleep(0.3)
turnOffAll()
time.sleep(0.3)
turnOnAll(GREEN)
time.sleep(0.3)
turnOffAll()
time.sleep(0.3)
turnOnAll(YELLOW)
time.sleep(1)
turnOffAll()
time.sleep(0.5)

for row in range(0,8):
    turnOnRow(RED,row)
    time.sleep(0.1)
turnOffAll()
for row in range(0,8):
    turnOnRow(GREEN,row)
    time.sleep(0.1)
turnOffAll()
for row in range(0,8):
    turnOnRow(YELLOW,row)
    time.sleep(0.1)
turnOffAll()

for column in range(0,8):
    turnOnColumn(RED,column)
    time.sleep(0.1)
turnOffAll()
for column in range(0,8):
    turnOnColumn(GREEN,column)
    time.sleep(0.1)
turnOffAll()
for column in range(0,8):
    turnOnColumn(YELLOW,column)
    time.sleep(0.1)
turnOffAll()

for row in range(0,8):
    for column in range(0,8):
        turnOnLed(RED,row,column)
        time.sleep(0.1)
turnOffAll()
for row in range(0,8):
    for column in range(0,8):
        turnOnLed(GREEN,row,column)
        time.sleep(0.1)
turnOffAll()
for row in range(0,8):
    for column in range(0,8):
        turnOnLed(YELLOW,row,column)
        time.sleep(0.1)
turnOffAll()

patternGreen = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternRed = [0x00,0x00,0xEF,0x00,0x00,0x00,0x00,0x00]
patternYellow = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
fastMultiplexing(patternGreen,patternRed,patternYellow,50)

patternGreen = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternRed = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
patternYellow = [0x00,0x00,0x18,0x3C,0x3C,0x18,0x00,0x00]
fastMultiplexing(patternGreen,patternRed,patternYellow,50)

continuing = True

if len(sys.argv) > 2:
   ledColor = sys.argv[1]
   text = sys.argv[2]
else:
    while (continuing == True):
        print "Choose text color: 1 for red, 2 for green, 3 for yellow."
        ledColor = sys.stdin.read() 
        print "\nEnter text to display and then press (Ctrl-D)."
        text = sys.stdin.read()
        textScroll(ledColor,text)
        print "\nDo you wish to enter more text?"
        text = sys.stdin.read()
        if (text == "yes\n" or text == "y\n"):
            
            continuing = True
        else:
            continuing = False

print "Finished"

