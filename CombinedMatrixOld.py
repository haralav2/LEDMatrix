import random, sys, time, smbus, pygame
from pygame.locals import *
import numpy as np
from numpy import *

##############################################################
# Definitions for the MCP23017
ADDRR = 0x20   # I2C bus address of the 23017 Rows
ADDRC = 0x21   # I2C bus address of the 23017 Columns
DIRA  = 0x00   # PortA I/O direction
DIRB  = 0x01   # PortB I/O direction
PORTA = 0x12   # PortA data register
PORTB = 0x13   # PortB data register
##############################################################

# Defining some constant variables
FPS = 30
BOARDWIDTH = 10
BOARDHEIGHT = 10

# The width of the window for the program
WINDOWWIDTH = 800

# The height of the window for the game
WINDOWHEIGHT = 800


FLASHSPEED = 500 # in milliseconds
FLASHDELAY = 200 # in milliseconds

# Size of the buttons that represent the LEDS
BUTTONSIZE = 60

# How much space would be required between the buttons
BUTTONGAPSIZE = 15

# The font size of the text
BASICFONTSIZE = 20

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
PURPLE       = ( 75,   0, 130)
BRIGHTPURPLE = (102,   0, 153)
bgColor = BLACK

# The color of the text in the buttons
TEXTCOLOR = WHITE

# The initial color of the LEDs
LEDColor = YELLOW

# The color of the COLOR button
COLORColor = RED

# The color of the SEE button
SEEColor = GREEN

# The initial flashing color for the LED
LEDFlashColor = BRIGHTYELLOW

# The SEE button flash color
SEEFlashColor = BRIGHTGREEN

# The COLOR button flash color
COLORFlashColor = BRIGHTRED

XMARGIN = int((WINDOWWIDTH - (BUTTONSIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BUTTONSIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Rect objects for each of the 64 buttons using a numpy array
buttons = np.empty((8,8), dtype=object)
for rows in range(0,8):
    for columns in range(0,8):
        buttons[rows,columns] = pygame.Rect(XMARGIN + rows * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + columns * (BUTTONSIZE + BUTTONGAPSIZE),BUTTONSIZE, BUTTONSIZE)

# Numpy array, which stores all the colors of the corresponding buttons 
buttonsColor = np.empty((8,8), dtype=object)

# I2C bus that controls the LED matrix
bus = smbus.SMBus(1)

# For the LED matrix - we need 6 arrays - 3 for rows and 3 for columns,where we will store the corresponding addresses
yellowArray = [0,0,0,0,0,0,0,0]
greenArray = [0,0,0,0,0,0,0,0]
redArray = [0,0,0,0,0,0,0,0]
    
# Main method
def main():
    global FPSCLOCK, yellowArray, redArray, greenArray, bus, DISPLAYSURF, BASICFONT, DRAW_SURF, DRAW_BUTTON, COLOR_SURF, COLOR_BUTTON, SEE_SURF, SEE_BUTTON, BASICTEXTFONT, LEDColor, COLORColor, SEEColor, LEDFlashColor, COLORFlashColor,SEEFlashColor,DEMO_SURF, DEMO_BUTTON

    # Initialising the game state
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Matrix')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    BASICTEXTFONT = pygame.font.Font('freesansbold.ttf', 35)
    infoSurf = BASICFONT.render('Choose your pattern.Start by pressing DRAW,', 2, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 20)

    DRAW_SURF, DRAW_BUTTON = makeText('DRAW', TEXTCOLOR, BLUE, XMARGIN + 0 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))
    COLOR_SURF, COLOR_BUTTON = makeText('COLOUR', TEXTCOLOR, COLORColor, XMARGIN + 2 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))
    SEE_SURF, SEE_BUTTON = makeText('SEE', TEXTCOLOR, SEEColor, XMARGIN + 4.3 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))
    DEMO_SURF, DEMO_BUTTON = makeText('DEMO', TEXTCOLOR, PURPLE, XMARGIN + 5.5 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of LEDs clicked
    
    # Set the color of all the LEDs to be the LEDColor
    initialColor()
            
    # When false it indicates that the player cannot click on the yellow buttons
    drawOnBoard = False
    
    while True: # main game loop

        
        #################
        # Initialise the chip 
        initialise()
        #################

        
        clickedButton = None # button that was clicked 
        DISPLAYSURF.fill(bgColor)
        drawAllButtons()
        
        #initialColor()

        # If something is drawn it is shown on the board
        for button in pattern:
            drawButtonWithColor(button, getFlashColor(button))
                    
        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)

                # If the pressed button was DRAW
                if clickedButton == BLUE:
                    pygame.display.update()
                    pygame.time.wait(1000)
                    drawOnBoard = True
                    flashButtonAnimationBig(clickedButton)

                # If the pressed button was COLOUR - change the color of the whole matrix
                elif clickedButton == RED:
                    pygame.display.update()
                    pygame.time.wait(1000)
                    flashButtonAnimationBig(clickedButton)
                    previousLED = LEDColor
                    previousLEDFlashColor = LEDFlashColor
                    LEDColor = COLORColor
                    LEDFlashColor = COLORFlashColor
                    COLORColor = SEEColor
                    COLORFlashColor = SEEFlashColor
                    SEEColor = previousLED
                    SEEFlashColor = previousLEDFlashColor
                    initialColor()

                #If the pressed button was SEE - display the pattern 
                elif clickedButton == GREEN:
                    drawOnBoard = False
                    pygame.display.update()
                    pygame.time.wait(1000)
                    for button in pattern:
                        drawButtonWithColor(button, getButtonColor(button))
                    flashButtonAnimationBig(clickedButton)
                    for button in pattern:
                        #flashButtonAnimation(button)
                        changeColor(button)
                        if button != None:
                            turnOnLed(getFlashColor(button),getButtonColumn(button),getButtonRow(button))
                        pygame.time.wait(FLASHDELAY)
                    multiplexing(greenArray,redArray,yellowArray,500)
                    turnOffAll()
                    
                    #LightPattern()
                    pygame.time.wait(5000)
                    pattern = []
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    for rows in range(0,8):
                        for columns in range(0,8):
                            buttonsColor[rows,columns] = LEDColor
                    pygame.display.update()
                    drawOnBoard = True

                # If the pressed button was purple - play the demo
                elif clickedButton == PURPLE:
                    flashButtonAnimationBig(clickedButton)
                    for index in range(0,5):
                        FlashDisplay(BRIGHTYELLOW)
                        drawAllButtonsWithColor(RED)

                        # Turn on the Leds
                        turnOffAll()
                        pygame.display.update()
                        FlashDisplay(BRIGHTRED)
                        drawAllButtonsWithColor(GREEN)

                        # Turn off the Leds
                        turnOffAll()
                        pygame.display.update()
                        FlashDisplay(BRIGHTGREEN)
                        drawAllButtonsWithColor(YELLOW)

                        # Turn on the Leds
                        turnOffAll()
                        pygame.display.update()
                        index = index + 1

                    # Show some random shapes
                    RaspberryPi()
                    Hi()
                    FlashingDot(BRIGHTYELLOW)
                    ChristmasTree()
                    drawAllButtonsWithColor(GREEN)
                    pygame.display.update()
                    FlashingDot(BRIGHTGREEN)
                    Sun()
                    drawAllButtonsWithColor(RED)
                    pygame.display.update()
                    FlashingDot(BRIGHTRED)
                    drawAllButtonsWithColor(YELLOW)
                    pygame.display.update()
                    Present()
                    Candle()
                    ChasingLights()

                # Deal with buttons from the matrix pressed
                else:
                    if drawOnBoard:
                        if clickedButton in pattern:
                            pattern.remove(clickedButton)
                            arraysAdd(clickedButton)
                        else:
                            pattern.append(clickedButton)
                            arraysAdd(clickedButton)

            # Changing colors of individual Leds
            elif event.type == MOUSEBUTTONUP and event.button == 3:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
                changeButtonColor(clickedButton)
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Stop the game        
def terminate():
    pygame.quit()
    sys.exit()

# Make text appear
def makeText(text, color, bgcolor, top, left):
    textSurf = BASICTEXTFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
        turnOffAll()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
            turnOffAll()
        pygame.event.post(event) # put the other KEYUP event objects back

# Flash the matrix buttons
def flashButtonAnimation(color, animationSpeed=50):
    for rows in range(0,8):
        for columns in range(0,8):
            if color == buttons[rows,columns]:
                flashColor = BRIGHTYELLOW
                rectangle = buttons[rows,columns]
                origSurf = DISPLAYSURF.copy()
                flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
                flashSurf = flashSurf.convert_alpha()
                r, g, b = flashColor
                for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
                    for alpha in range(start, end, animationSpeed * step):
                        checkForQuit()
                        DISPLAYSURF.blit(origSurf, (0, 0))
                        flashSurf.fill((r, g, b, alpha))
                        DISPLAYSURF.blit(flashSurf, rectangle.topleft)
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                DISPLAYSURF.blit(origSurf, (0, 0))

# Draw the buttons all with the same background color
def initialColor():
    for rows in range(0,8):
        for columns in range(0,8):
            buttonsColor[rows,columns] = LEDColor

# Light all the Leds that have been selected for some time
def changeColor(color, animationSpeed=100):
    for rows in range(0,8):
        for columns in range(0,8):
            if color == buttons[rows,columns]:
                flashColor = getFlashColor(buttons[rows,columns])
                rectangle = buttons[rows,columns]
                origSurf = DISPLAYSURF.copy()
                flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
                flashSurf = flashSurf.convert_alpha()
                r, g, b = flashColor
                for alpha in range(0, 255, animationSpeed):
                    checkForQuit()
                    DISPLAYSURF.blit(origSurf, (0,0))
                    flashSurf.fill((r, g, b, alpha))
                    DISPLAYSURF.blit(flashSurf,rectangle.topleft)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    
# Flash the draw, done and see buttons
def flashButtonAnimationBig(color, animationSpeed=50):
    if color == BLUE:
        flashColor = BRIGHTBLUE
        rectangle = DRAW_BUTTON
        buttonWidth = DRAW_BUTTON.width
        buttonHeight = DRAW_BUTTON.height
    elif color == RED:
        flashColor = BRIGHTRED
        rectangle = COLOR_BUTTON
        buttonWidth = COLOR_BUTTON.width
        buttonHeight = COLOR_BUTTON.height
    elif color == GREEN:
        flashColor = BRIGHTGREEN
        rectangle = SEE_BUTTON
        buttonWidth = SEE_BUTTON.width
        buttonHeight = SEE_BUTTON.height
    elif color == PURPLE:
        flashColor = BRIGHTPURPLE
        rectangle = DEMO_BUTTON
        buttonWidth = DEMO_BUTTON.width
        buttonHeight = DEMO_BUTTON.height


    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((buttonWidth, buttonHeight))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))
'''
def drawButtons(color):

    for rows in range(0,8):
        for columns in range(0,8):
             pygame.draw.rect(DISPLAYSURF, color, buttons[rows,columns])

    
    DISPLAYSURF.blit(DRAW_SURF, DRAW_BUTTON)
    DISPLAYSURF.blit(COLOR_SURF, COLOR_BUTTON)
    DISPLAYSURF.blit(SEE_SURF, SEE_BUTTON)    
    DISPLAYSURF.blit(DEMO_SURF, DEMO_BUTTON)
'''
def drawButtonWithColor(button, color):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                pygame.draw.rect(DISPLAYSURF, color, button)

    DISPLAYSURF.blit(DRAW_SURF, DRAW_BUTTON)
    DISPLAYSURF.blit(COLOR_SURF, COLOR_BUTTON)
    DISPLAYSURF.blit(SEE_SURF, SEE_BUTTON)
    DISPLAYSURF.blit(DEMO_SURF, DEMO_BUTTON)
    
                
def getButtonClicked(x, y):
    for rows in range(0,8):
        for columns in range(0,8):
            if buttons[rows,columns].collidepoint( (x,y) ):
                return buttons[rows,columns]
    if DRAW_BUTTON.collidepoint( (x, y) ):
        return BLUE
    elif COLOR_BUTTON.collidepoint( (x, y) ):
        return RED
    elif SEE_BUTTON.collidepoint( (x, y) ):
        return GREEN
    elif DEMO_BUTTON.collidepoint( (x, y) ):
        return PURPLE
    return None

def getButton(row,col):
    return buttons[row,col]

def getButtonRow(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                return rows

def getButtonColumn(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                return columns
    
    
def getButtonColor(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                return buttonsColor[rows,columns]

def getFlashColor(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                if buttonsColor[rows,columns] == YELLOW:
                    return BRIGHTYELLOW
                elif buttonsColor[rows,columns] == RED:
                    return BRIGHTRED
                elif buttonsColor[rows,columns] == GREEN:
                    return BRIGHTGREEN

def changeButtonColor(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                if buttonsColor[rows,columns] == YELLOW:
                    buttonsColor[rows,columns] = RED
                elif buttonsColor[rows,columns] == RED:
                    buttonsColor[rows,columns] = GREEN
                elif buttonsColor[rows,columns] == GREEN:
                    buttonsColor[rows,columns] = YELLOW
                
        
     

def ChristmasTree():
    tree = (buttons[4,0], buttons[3,1], buttons[4,1], buttons[5,1], buttons[2,2], buttons[3,2], buttons[4,2], buttons[5,2], buttons[6,2], buttons[2,3],
            buttons[3,3], buttons[4,3], buttons[5,3], buttons[6,3], buttons[1,4], buttons[2,4], buttons[3,4], buttons[4,4], buttons[5,4], buttons[6,4],
            buttons[7,4], buttons[1,5], buttons[2,5], buttons[3,5], buttons[4,5], buttons[5,5], buttons[6,5], buttons[7,5], buttons[0,6], buttons[1,6],
            buttons[2,6], buttons[3,6], buttons[5,6], buttons[6,6], buttons[7,6], buttons[4,6], buttons[4,7])

    for index in range(0,35):
        drawButtonWithColor(tree[index],BRIGHTGREEN)
        arraysAddColor(tree[index],GREEN)
        pygame.display.update()
    drawButtonWithColor(tree[35],BRIGHTRED)
    arraysAddColor(tree[35],RED)
    pygame.display.update()
    drawButtonWithColor(tree[36],BRIGHTRED)
    arraysAddColor(tree[36],RED)
    pygame.display.update()
    multiplexing(greenArray,redArray,yellowArray,500)
    pygame.time.wait(5000)
    
    for button in tree:
        drawButtonWithColor(button,getButtonColor(button))
    pygame.time.wait(500)


def Sun():
    sun = (buttons[3,2], buttons[4,2], buttons[2,3], buttons[3,3], buttons[4,3], buttons[5,3], buttons[2,4], buttons[3,4],
           buttons[4,4], buttons[5,4], buttons[3,5], buttons[4,5])
    for index in range(0,12):
        drawButtonWithColor(sun[index],BRIGHTYELLOW)
        pygame.display.update()
    pygame.display.update()
    pygame.time.wait(5000)
    
    for button in sun:
        drawButtonWithColor(button,getButtonColor(button))
    pygame.time.wait(500)

def Present():
    present = (buttons[2,5], buttons[4,5], buttons[2,7], buttons[4,7], buttons[3,5], buttons[3,6], buttons[3,7], buttons[2,6], buttons[4,6], buttons[3,4])
    for index in range(0,4):
        drawButtonWithColor(present[index],BRIGHTRED)
        pygame.display.update()
    for index in range(4,10):
        drawButtonWithColor(present[index],BRIGHTYELLOW)
        pygame.display.update()
    drawButtonWithColor(present[index],BRIGHTGREEN)
    pygame.display.update()
    pygame.time.wait(5000)

    for button in present:
        drawButtonWithColor(button,getButtonColor(button))
    pygame.time.wait(500)

def Candle():
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], GREEN)
    for rows in range(4,8):
        for columns in range(2,5):
            drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
            pygame.display.update()
    drawButtonWithColor(buttons[3,2],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    pygame.time.wait(5000)
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], YELLOW)

def ChasingLights():
    for rows in range(0,8):
        if rows % 2 == 0:
            for columns in range(0,10):
                if columns >= 0 and columns < 8:
                    drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
                    turnOnLed(BRIGHTYELLOW,columns,rows)
                    pygame.display.update()
                if columns > 0 and columns < 9:
                    drawButtonWithColor(buttons[columns - 1,rows],BRIGHTGREEN)
                    turnOnLed(BRIGHTGREEN,columns,rows)
                    pygame.display.update()
                if columns > 1:
                    drawButtonWithColor(buttons[columns - 2,rows],BRIGHTRED)
                    turnOnLed(BRIGHTRED,columns,rows)
                    pygame.display.update()
        else:
            for columns in range(8,-3, -1):
                if columns < 8 and columns >= 0:
                    drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
                    pygame.display.update()
                if columns < 7 and columns >= -1 :
                    drawButtonWithColor(buttons[columns + 1,rows],BRIGHTGREEN)
                    pygame.display.update()
                if columns < 6 and columns >= -2:
                    drawButtonWithColor(buttons[columns + 2,rows],BRIGHTRED)
                    pygame.display.update()
    pygame.time.wait(5000)
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], YELLOW)

def RaspberryPi():
    drawButtonWithColor(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[4,3],BRIGHTRED)
    pygame.display.update()
    for rows in range(4,7):
        for columns in range(2,6):
            drawButtonWithColor(buttons[columns,rows],BRIGHTRED)
            pygame.display.update()
    drawButtonWithColor(buttons[3,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[4,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[4,2],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColor(buttons[4,1],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColor(buttons[5,1],BRIGHTGREEN)
    pygame.display.update()
    pygame.time.wait(5000)
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], YELLOW)

def Hi():
    hi = (buttons[1,2], buttons[1,3], buttons[1,4], buttons[1,5], buttons[1,6], buttons[2,4], buttons[3,2], buttons[3,3], buttons[3,4],
          buttons[3,5], buttons[3,6], buttons[5,2], buttons[6,2], buttons[7,2], buttons[6,3], buttons[6,4], buttons[6,5], buttons[6,6],
          buttons[7,6], buttons[5,6])
    drawAllButtonsWithColor(RED)
    pygame.display.update()
    for button in hi:
        drawButtonWithColor(button,BRIGHTYELLOW)
        pygame.display.update()
    pygame.time.wait(5000)
    drawAllButtonsWithColor(YELLOW)
    pygame.display.update()
    

def drawAllButtonsWithColor(color):
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], color)

def drawAllButtons():
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], buttonsColor[rows,columns])

def FlashDisplay(color):
    drawAllButtonsWithColor(color)
    pygame.display.update()
    turnOnAll(color)
    pygame.time.wait(500)
    
def FlashingDot(color,animationSpeed = 100):
    for rows in range(0,8):
        for columns in range(0,8):
            flashColor = color
            rectangle = buttons[rows,columns]
            origSurf = DISPLAYSURF.copy()
            flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
            flashSurf = flashSurf.convert_alpha()
            r, g, b = flashColor
            for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
                for alpha in range(start, end, animationSpeed * step):
                    checkForQuit()
                    DISPLAYSURF.blit(origSurf, (0, 0))
                    flashSurf.fill((r, g, b, alpha))
                    DISPLAYSURF.blit(flashSurf, rectangle.topleft)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    ######
                    turnOnLed(color,columns,rows)
                    ######
            turnOffAll()
            DISPLAYSURF.blit(origSurf, (0, 0))

def arraysAdd(button):
    if button != None:
        color = getButtonColor(button)
        row = getButtonColumn(button)
        column = getButtonRow(button)
        temp = 1<<column
        if color == YELLOW or color == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] | temp
        elif color == RED or color == BRIGHTRED:
            redArray[row] = redArray[row] | temp
        elif color == GREEN or color == BRIGHTGREEN:
            greenArray[row] = greenArray[row] | temp

def arraysAddColor(button,color):
    if button != None:
        row = getButtonColumn(button)
        column = getButtonRow(button)
        temp = 1<<column
        if color == YELLOW or color == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] | temp
        elif color == RED or color == BRIGHTRED:
            redArray[row] = redArray[row] | temp
        elif color == GREEN or color == BRIGHTGREEN:
            greenArray[row] = greenArray[row] | temp
        
                      
            
##########################################################
def initialise():
    # Set all 16 pins to be output
    bus.write_byte_data(ADDRR,DIRA,0x00)   # All outputs on PortA address 0x20
    bus.write_byte_data(ADDRR,DIRB,0x00)   # All outputs on PortB address 0x20
    bus.write_byte_data(ADDRC,DIRA,0x00)   # All outputs on PortA address 0x21 - green
    bus.write_byte_data(ADDRC,DIRB,0x00)   # All outputs on PortB address 0x21 - red
    bus.write_byte_data(ADDRR,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)

def turnOnLed(color,row,column):
    # Turn on individual LED with a specific color - green,red ot yellow
    if color == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,0xFF)
    elif color == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
        bus.write_byte_data(ADDRC,PORTB,0xFF)
    elif color == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,~(1<<column))
        bus.write_byte_data(ADDRC,PORTA,~(1<<column))
    bus.write_byte_data(ADDRR,PORTA,1<<row)

def LightPattern():
    rowSum = 0
    columnSum = 0
    for row in yellowRow:
        rowSum = rowSum | row
    for column in yellowColumn:
        columnSum = columnSum | column
    bus.write_byte_data(ADDRC,PORTB,columnSum)
    bus.write_byte_data(ADDRC,PORTA,columnSum)
    bus.write_byte_data(ADDRR,PORTA,~rowSum)

    rowSum = 0
    columnSum = 0
    for index in range (0,len(redRow)):
        for index in range (0,len(redColumn)):
            columnSum = columnSum | redColumn[index]
        bus.write_byte_data(ADDRC,PORTB,columnSum)
        bus.write_byte_data(ADDRR,PORTB,~redRow[index])
        time.sleep(0.1)
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRR,PORTB,0x00)
        #rowSum = rowSum | redRow[index]
        #columnSum = columnSum | redColumn[index]
        #bus.write_byte_data(ADDRC,PORTB,columnSum)
        #bus.write_byte_data(ADDRR,PORTB,~rowSum)
        #time.sleep(0.1)

    rowSum = 0
    columnSum = 0
    for row in greenRow:
        rowSum |= row
    for column in greenColumn:
        columnSum |= column
    bus.write_byte_data(ADDRC,PORTA,columnSum)
    bus.write_byte_data(ADDRR,PORTA,~rowSum)

def turnOnAll(color):
    # Turn on all LEDs
    if color == BRIGHTRED:
        bus.write_byte_data(ADDRC,PORTA,0xFF)
        bus.write_byte_data(ADDRC,PORTB,0x00)
    elif color == BRIGHTGREEN:
        bus.write_byte_data(ADDRC,PORTB,0xFF)
        bus.write_byte_data(ADDRC,PORTA,0x00)
    elif color == BRIGHTYELLOW:
        bus.write_byte_data(ADDRC,PORTB,0x00)
        bus.write_byte_data(ADDRC,PORTA,0x00)    
    bus.write_byte_data(ADDRR,PORTA,0xFF)

def turnOffAll():
    # Turn off all LEDs
    bus.write_byte_data(ADDRR,PORTA,0x00)
    bus.write_byte_data(ADDRC,PORTB,0x00)
    bus.write_byte_data(ADDRC,PORTA,0x00)

def multiplexing(patternGreen,patternRed,patternYellow,count):
    for count in range(0,count):
        for row in range(0,8):
            turnOnLeds(GREEN,row,patternGreen[row])
            turnOnLeds(RED,row,patternRed[row])
            turnOnLeds(YELLOW,row,patternYellow[row])

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
##########################################################

    
if __name__ == '__main__':
    main()



