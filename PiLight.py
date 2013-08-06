#############################################   Authors   ###########################################
###########################                     PiLight                  ############################  
###########################               Veneta Haralampieva           #############################





import random
import sys
import time
import smbus
import pygame
from pygame.locals import *
import numpy as np
from numpy import *
import Bicolour_Interface



# Definitions for the MCP23017
ADDRR = 0x20   # I2C bus address of the 23017 Rows
ADDRC = 0x21   # I2C bus address of the 23017 Columns
DIRA  = 0x00   # PortA I/O direction
DIRB  = 0x01   # PortB I/O direction
PORTA = 0x12   # PortA data register
PORTB = 0x13   # PortB data register

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
LEDSIZE = 60

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
GRAY         = (128, 128, 128)

# The Colour of the text in the buttons
TEXTColour = WHITE

# Initial colour of the matrix buttons displayed
LEDInitialColour = DARKGRAY

# Background colour
bgColour = BLACK

# Set the margin on the x axix
XMARGIN = int((WINDOWWIDTH - (LEDSIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2 + 60)

# Set the margin on the y axix
YMARGIN = int((WINDOWHEIGHT - (LEDSIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Rect objects for each of the 64 buttons using a numpy array
buttons = np.empty((8,8), dtype=object)
for rows in range(0,8):
    for columns in range(0,8):
        buttons[rows,columns] = pygame.Rect(XMARGIN + rows * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + columns * (LEDSIZE + BUTTONGAPSIZE),LEDSIZE, LEDSIZE)

# Numpy array, which stores all the Colours of the corresponding buttons 
buttonsColour = np.empty((8,8), dtype=object)

    
# Main method
def main():
    global FPSCLOCK, yellowArray, redArray, greenArray, bus, piano1, piano2, piano3, piano4, piano5, piano6, piano7, piano8, DISPLAYSURF, CLEAR_SURF, CLEAR_BUTTON, NONE_SURF,NONE_BUTTON, BASICFONT, LEDInitialColour, GREEN_SURF, GREEN_BUTTON, YELLOW_SURF, YELLOW_BUTTON, RED_SURF, RED_BUTTON, SEE_SURF, SEE_BUTTON, BASICTEXTFONT, DEMO_SURF, DEMO_BUTTON

    # I2C bus that controls the LED matrix
    bus = smbus.SMBus(1)

    # For the LED matrix - we need 3 arrays - one for each colour, where we will keep what values need to be send to the matrix to lit up a pattern
    yellowArray = [0,0,0,0,0,0,0,0]
    greenArray = [0,0,0,0,0,0,0,0]
    redArray = [0,0,0,0,0,0,0,0]
    
    # Initialising the game state
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Matrix')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    BASICTEXTFONT = pygame.font.Font('freesansbold.ttf', 30)
    infoSurfOne = BASICFONT.render('Choose your pattern. On your left you can select colours.', 2, WHITE)
    infoSurfTwo = BASICFONT.render('To change the colour of just one LED press on it one more time.', 2, WHITE)
    infoSurfThree = BASICFONT.render('To unselect a button press NONE. When you are finished press SEE.', 2, WHITE)
    infoRectOne = infoSurfOne.get_rect()
    infoRectOne.topleft = (10, WINDOWHEIGHT - 60)
    infoRectTwo = infoSurfTwo.get_rect()
    infoRectTwo.topleft = (10, WINDOWHEIGHT - 40)
    infoRectThree = infoSurfThree.get_rect()
    infoRectThree.topleft = (10, WINDOWHEIGHT - 20)

    # Sounds to play when a button is pressed
    piano1 = pygame.mixer.Sound('piano-a.wav')
    piano2 = pygame.mixer.Sound('piano-b.wav')
    piano3 = pygame.mixer.Sound('piano-c.wav')
    piano4 = pygame.mixer.Sound('piano-d.wav')
    piano5 = pygame.mixer.Sound('piano-e.wav')
    piano6 = pygame.mixer.Sound('piano-f.wav')
    piano7 = pygame.mixer.Sound('piano-#f.wav')
    piano8 = pygame.mixer.Sound('piano-g.wav')

    # Change LED colour buttons
    GREEN_SURF,GREEN_BUTTON = makeText(' GREEN  ', TEXTColour, GREEN, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 1 * (LEDSIZE + BUTTONGAPSIZE))
    YELLOW_SURF,YELLOW_BUTTON = makeText('YELLOW', TEXTColour, YELLOW, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 2 * (LEDSIZE + BUTTONGAPSIZE))
    RED_SURF,RED_BUTTON = makeText('    RED    ', TEXTColour, RED, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 3 * (LEDSIZE + BUTTONGAPSIZE))

    # Unselect a single button
    NONE_SURF,NONE_BUTTON = makeText('  NONE   ',TEXTColour, DARKGRAY, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 4 * (LEDSIZE + BUTTONGAPSIZE))

    # Clear the entira pattern
    CLEAR_SURF,CLEAR_BUTTON = makeText(' CLEAR  ',TEXTColour, GRAY, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 5 * (LEDSIZE + BUTTONGAPSIZE))

    SEE_SURF, SEE_BUTTON = makeText('    SEE     ', TEXTColour, BLUE, XMARGIN + 1.5 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))

    DEMO_SURF, DEMO_BUTTON = makeText('   DEMO   ', TEXTColour, PURPLE, XMARGIN + 4.5 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of LEDs clicked
    
    # Set the Colour of all the LEDs to be the LEDColour
    initialColour(pattern)
            
    # When false it indicates that the player cannot click on the gray buttons
    drawOnBoard = True
    global GREENMODE
    GREENMODE = 1
    global REDMODE
    REDMODE = 2
    global YELLOWMODE
    YELLOWMODE = 3
    global NONEMODE
    NONEMODE = 4
    global CLEARMODE
    CLEARMODE = 5
    global stateOfSelection
    stateOfSelection = GREENMODE
    global previousSelection
    previousSelection = 0
    while True: # main game loop

        Bicolour_Interface.turnOffAll()
        # Initialise the chip 
        Bicolour_Interface.initialise()
        
        
        clickedButton = None # button that was clicked 
        DISPLAYSURF.fill(bgColour)
        drawAllButtons()

        # If something is drawn it is shown on the board
        for button in pattern:
            drawButtonWithColour(button, getFlashColour(button))
                    
        DISPLAYSURF.blit(infoSurfOne, infoRectOne)
        DISPLAYSURF.blit(infoSurfTwo, infoRectTwo)
        DISPLAYSURF.blit(infoSurfThree, infoRectThree)
         
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
                if clickedButton == GREEN:
                    flashButtonAnimationBig(clickedButton)
                    stateOfSelection = GREENMODE
                elif clickedButton == YELLOW:
                    flashButtonAnimationBig(clickedButton)
                    stateOfSelection = YELLOWMODE
                elif clickedButton == RED:
                    flashButtonAnimationBig(clickedButton)
                    stateOfSelection = REDMODE
                elif clickedButton == DARKGRAY:
                    flashButtonAnimationBig(clickedButton)
                    previousSelection = stateOfSelection
                    stateOfSelection = NONEMODE
                elif clickedButton == GRAY:
                    flashButtonAnimationBig(clickedButton)
                    previousSelection = stateOfSelection
                    pattern = []
                    initialColour(pattern)
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]

                #If the pressed button was SEE - display the pattern 
                elif clickedButton == BLUE:
                    drawOnBoard = False
                    if pattern == []:
                        drawOnBoard = True
                    else:
                        pygame.display.update()
                        pygame.time.wait(1000)
                        for button in pattern:
                            drawButtonWithColour(button, getButtonColour(button))
                        flashButtonAnimationBig(clickedButton)
                        for button in pattern:
                            flashColour(button)
                            if button != None:
                                Bicolour_Interface.turnOnLed(getFlashColour(button),getButtonRow(button),getButtonColumn(button))
                            pygame.time.wait(FLASHDELAY)
                        Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,300)
                        Bicolour_Interface.turnOffAll()
                        pattern = []
                        yellowArray = [0,0,0,0,0,0,0,0]
                        greenArray = [0,0,0,0,0,0,0,0]
                        redArray = [0,0,0,0,0,0,0,0]
                        for rows in range(0,8):
                            for columns in range(0,8):
                                buttonsColour[rows,columns] = DARKGRAY
                        pygame.display.update()
                        drawOnBoard = True
                        normalMode = True

                # If the pressed button was DEMO - play the demo
                elif clickedButton == PURPLE:
                    flashButtonAnimationBig(clickedButton)
                    for index in range(0,5):
                        FlashDisplay(BRIGHTYELLOW)
                        drawAllButtonsWithColour(DARKGRAY)

                        # Turn on the Leds
                        Bicolour_Interface.turnOffAll()
                        pygame.display.update()
                        FlashDisplay(BRIGHTRED)
                        drawAllButtonsWithColour(DARKGRAY)

                        # Turn off the Leds
                        Bicolour_Interface.turnOffAll()
                        pygame.display.update()
                        FlashDisplay(BRIGHTGREEN)
                        drawAllButtonsWithColour(DARKGRAY)

                        # Turn on the Leds
                        Bicolour_Interface.turnOffAll()
                        pygame.display.update()
                        index = index + 1

                    # Show some random shapes
                    RaspberryPi()
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    
                    Hi()
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                   
                    FlashingDot(BRIGHTYELLOW)
                    Bicolour_Interface.turnOffAll()
                    
                    ChristmasTree()
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                                      
                    drawAllButtonsWithColour(DARKGRAY)
                    pygame.display.update()
                    FlashingDot(BRIGHTGREEN)
                    Bicolour_Interface.turnOffAll()

                    Sun()
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    pygame.display.update()
                    
                    FlashingDot(BRIGHTRED)
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    pygame.display.update()
                                        
                    Present()
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                                        
                    Candle()
                    Bicolour_Interface.turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    
                    ChasingLights()
                    Bicolour_Interface.turnOffAll()

                # Deal with buttons from the matrix pressed
                else:
                    if drawOnBoard:
                        previousColour = getButtonColour(clickedButton)
                        if clickedButton in pattern:
                            changeButtonColour(clickedButton,pattern)
                            arrayChangeColour(clickedButton,previousColour)
                        else:
                            changeButtonColour(clickedButton,pattern)
                            pattern.append(clickedButton)
                            arraysAdd(clickedButton)
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Stop the game        
def terminate():
    pygame.quit()
    sys.exit()

# Make text appear
def makeText(text, Colour, bgColour, top, left):
    textSurf = BASICTEXTFONT.render(text, True, Colour, bgColour)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
        Bicolour_Interface.turnOffAll()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
            Bicolour_Interface.turnOffAll()
        pygame.event.post(event) # put the other KEYUP event objects back

def playSoundForButton(col):
    if col == 0:
        return piano1
    elif col == 1:
        return piano2
    elif col == 2:
        return piano3
    elif col == 3:
        return piano4
    elif col == 4:
        return piano5
    elif col == 5:
        return piano6
    elif col == 6:
        return piano7
    elif col == 7:
        return piano8
    else:
        print "playing0"
        return piano1
    


# Draw the buttons all with the same background Colour
def initialColour(array):
    for rows in range(0,8):
        for columns in range(0,8):
            if buttons[rows,columns] not in array:
                buttonsColour[rows,columns] = LEDInitialColour

# Light all the Leds that have been selected for some time
def flashColour(Colour, animationSpeed=100):
    for rows in range(0,8):
        for columns in range(0,8):
            if Colour == buttons[rows,columns]:
                sound = playSoundForButton(rows)
                flashColour = getFlashColour(buttons[rows,columns])
                rectangle = buttons[rows,columns]
                origSurf = DISPLAYSURF.copy()
                flashSurf = pygame.Surface((LEDSIZE, LEDSIZE))
                flashSurf = flashSurf.convert_alpha()
                r, g, b = flashColour
                sound.play()
                pygame.time.wait(200)
                for alpha in range(0, 255, animationSpeed):
                    checkForQuit()
                    DISPLAYSURF.blit(origSurf, (0,0))
                    flashSurf.fill((r, g, b, alpha))
                    DISPLAYSURF.blit(flashSurf,rectangle.topleft)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    
# Flash the menu buttons -  RED, YELLOW, GREEN, SEE, DEMO, NONE and CLEAR
def flashButtonAnimationBig(colour, animationSpeed=50):
    if colour == RED:
        flashColour = BRIGHTRED
        rectangle = RED_BUTTON
        buttonWidth = RED_BUTTON.width
        buttonHeight = RED_BUTTON.height
    elif colour == BLUE:
        flashColour = BRIGHTBLUE
        rectangle = SEE_BUTTON
        buttonWidth = SEE_BUTTON.width
        buttonHeight = SEE_BUTTON.height
    elif colour == YELLOW:
        flashColour = BRIGHTYELLOW
        rectangle = YELLOW_BUTTON
        buttonWidth = YELLOW_BUTTON.width
        buttonHeight = YELLOW_BUTTON.height
    elif colour == GREEN:
        flashColour = BRIGHTGREEN
        rectangle = GREEN_BUTTON
        buttonWidth = GREEN_BUTTON.width
        buttonHeight = GREEN_BUTTON.height
    elif colour == PURPLE:
        flashColour = BRIGHTPURPLE
        rectangle = DEMO_BUTTON
        buttonWidth = DEMO_BUTTON.width
        buttonHeight = DEMO_BUTTON.height
    elif colour == DARKGRAY:
        flashColour = DARKGRAY
        rectangle = NONE_BUTTON
        buttonWidth = NONE_BUTTON.width
        buttonHeight = NONE_BUTTON.height
    elif colour == GRAY:
        flashColour = GRAY
        rectangle = CLEAR_BUTTON
        buttonWidth = CLEAR_BUTTON.width
        buttonHeight = CLEAR_BUTTON.height


    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((buttonWidth, buttonHeight))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColour
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))

def drawButtonWithColour(button, Colour):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                pygame.draw.rect(DISPLAYSURF, Colour, button)
                
    DISPLAYSURF.blit(SEE_SURF, SEE_BUTTON)
    DISPLAYSURF.blit(DEMO_SURF, DEMO_BUTTON)
    DISPLAYSURF.blit(GREEN_SURF, GREEN_BUTTON)
    DISPLAYSURF.blit(YELLOW_SURF, YELLOW_BUTTON)
    DISPLAYSURF.blit(RED_SURF, RED_BUTTON)
    DISPLAYSURF.blit(NONE_SURF, NONE_BUTTON)
    DISPLAYSURF.blit(CLEAR_SURF, CLEAR_BUTTON)
    
def drawAllButtonsWithColour(colour):
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColour(buttons[rows,columns], colour)

def drawAllButtons():
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColour(buttons[rows,columns], buttonsColour[rows,columns])
                
def getButtonClicked(x, y):
    for rows in range(0,8):
        for columns in range(0,8):
            if buttons[rows,columns].collidepoint( (x,y) ):
                return buttons[rows,columns]
    if RED_BUTTON.collidepoint( (x, y) ):
        return RED
    elif GREEN_BUTTON.collidepoint( (x, y) ):
        return GREEN
    elif YELLOW_BUTTON.collidepoint( (x, y) ):
        return YELLOW
    elif NONE_BUTTON.collidepoint( (x, y) ):
        return DARKGRAY
    elif SEE_BUTTON.collidepoint( (x, y) ):
        return BLUE
    elif DEMO_BUTTON.collidepoint( (x, y) ):
        return PURPLE
    elif CLEAR_BUTTON.collidepoint( (x, y) ):
        return GRAY
    
    return None

# When supplying a row and column number return the corresponding
# button in the array
def getButton(row,col):
    return buttons[row,col]

# Given a button and returns the row number 
def getButtonRow(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[columns,rows]:
                return rows

# Given a button and returns the row number 
def getButtonColumn(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[columns,rows]:
                return columns
    
# Given a button return its colour in the colour matrix    
def getButtonColour(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                return buttonsColour[rows,columns]

# Get the appropriate flash colour for the button
def getFlashColour(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                if buttonsColour[rows,columns] == YELLOW:
                    return BRIGHTYELLOW
                elif buttonsColour[rows,columns] == RED:
                    return BRIGHTRED
                elif buttonsColour[rows,columns] == GREEN:
                    return BRIGHTGREEN

# Change the button colours to match the selected mode - yellow, green or red
# The normal mode is selecting green leds
def changeButtonColour(button,array):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                if stateOfSelection == GREENMODE:
                    if buttonsColour[rows,columns] == DARKGRAY:
                        buttonsColour[rows,columns] = GREEN
                    elif buttonsColour[rows,columns] == RED:
                        buttonsColour[rows,columns] = GREEN
                    elif buttonsColour[rows,columns] == YELLOW:
                        buttonsColour[rows,columns] = GREEN
                    elif buttonsColour[rows,columns] == GREEN:
                        buttonsColour[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                elif stateOfSelection == REDMODE:
                    if buttonsColour[rows,columns] == DARKGRAY:
                        buttonsColour[rows,columns] = RED
                    elif buttonsColour[rows,columns] == GREEN:
                        buttonsColour[rows,columns] = RED
                    elif buttonsColour[rows,columns] == YELLOW:
                        buttonsColour[rows,columns] = RED
                    elif buttonsColour[rows,columns] == RED:
                        buttonsColour[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                        
                elif stateOfSelection == YELLOWMODE:
                    if buttonsColour[rows,columns] == DARKGRAY:
                        buttonsColour[rows,columns] = YELLOW
                    elif buttonsColour[rows,columns] == GREEN:
                        buttonsColour[rows,columns] = YELLOW
                    elif buttonsColour[rows,columns] == YELLOW:
                        buttonsColour[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                    elif buttonsColour[rows,columns] == RED:
                        buttonsColour[rows,columns] = YELLOW
                elif stateOfSelection == NONEMODE:
                    buttonsColour[rows,columns] = DARKGRAY
                    if button in array:
                        array.remove(button)
                        arraysRemove(button)
                    global stateOfSelection
                    global previousSelection
                    stateOfSelection = previousSelection
                            
                        
                    
########## Dealing With Arrays and Multiplexing ######################## 

# When a button is pressed 
def arraysAdd(button):
    if button != None:
        colour = getButtonColour(button)
        column = getButtonColumn(button)
        row = getButtonRow(button)
        temp = 1<<column
        if colour == YELLOW or colour == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] | temp
        elif colour == RED or colour == BRIGHTRED:
            redArray[row] = redArray[row] | temp
        elif colour == GREEN or colour == BRIGHTGREEN:
            greenArray[row] = greenArray[row] | temp

# Add colours to the array to make the LED matrix
# turn on the corresponding LED and colour
def arraysAddColour(button,colour):
    if button != None:
        column = getButtonColumn(button)
        row = getButtonRow(button)
        temp = 1<<column
        if colour == YELLOW or colour == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] | temp
        elif colour == RED or colour == BRIGHTRED:
            redArray[row] = redArray[row] | temp
        elif colour == GREEN or colour == BRIGHTGREEN:
            greenArray[row] = greenArray[row] | temp

# Remove a button from the array - the LED that corresponds
# to this button will not flash
def arraysRemove(button):
    if button != None:
        colour = getButtonColour(button)
        column = getButtonColumn(button)
        row = getButtonRow(button)
        temp = 1<<column
        if colour == YELLOW or colour == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] ^ temp
        elif colour == RED or colour == BRIGHTRED:
            redArray[row] = redArray[row] ^ temp
        elif colour == GREEN or colour == BRIGHTGREEN:
            greenArray[row] = greenArray[row] ^ temp

# Remove a button from the array - the LED that corresponds
# to this button will not flash, the colour is supplied as an argument
# and not obtained from the colour matrix
def arraysRemoveColour(button,colour):
    if button != None:
        column = getButtonColumn(button)
        row = getButtonRow(button)
        temp = 1<<column
        if colour == YELLOW or colour == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] ^ temp
        elif colour == RED or colour == BRIGHTRED:
            redArray[row] = redArray[row] ^ temp
        elif colour == GREEN or colour == BRIGHTGREEN:
            greenArray[row] = greenArray[row] ^ temp


# Change the colour in the array - ensures an LED flashes with
# the appropriate colour
def arrayChangeColour(button,previousColour):
    if button != None:
        newColour = getButtonColour(button)
        arraysAddColour(button,newColour)
        arraysRemoveColour(button,previousColour)

####################################################### Demo ########################################################################################
        
    
def ChristmasTree():
    tree = (buttons[4,0], buttons[3,1], buttons[4,1], buttons[5,1], buttons[2,2], buttons[3,2], buttons[4,2], buttons[5,2], buttons[6,2], buttons[2,3],
            buttons[3,3], buttons[4,3], buttons[5,3], buttons[6,3], buttons[1,4], buttons[2,4], buttons[3,4], buttons[4,4], buttons[5,4], buttons[6,4],
            buttons[7,4], buttons[1,5], buttons[2,5], buttons[3,5], buttons[4,5], buttons[5,5], buttons[6,5], buttons[7,5], buttons[0,6], buttons[1,6],
            buttons[2,6], buttons[3,6], buttons[5,6], buttons[6,6], buttons[7,6], buttons[4,6], buttons[4,7])

    for index in range(0,35):
        drawButtonWithColour(tree[index],BRIGHTGREEN)
        arraysAddColour(tree[index],GREEN)
        pygame.display.update()
    drawButtonWithColour(tree[35],BRIGHTRED)
    arraysAddColour(tree[35],RED)
    pygame.display.update()
    drawButtonWithColour(tree[36],BRIGHTRED)
    arraysAddColour(tree[36],RED)
    pygame.display.update()
    Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,500)
    Bicolour_Interface.turnOffAll()
    for button in tree:
        drawButtonWithColour(button,getButtonColour(button))



def Sun():
    sun = (buttons[3,2], buttons[4,2], buttons[2,3], buttons[3,3], buttons[4,3], buttons[5,3], buttons[2,4], buttons[3,4],
           buttons[4,4], buttons[5,4], buttons[3,5], buttons[4,5])
    for index in range(0,12):
        drawButtonWithColour(sun[index],BRIGHTYELLOW)
        arraysAddColour(sun[index],YELLOW)
        pygame.display.update()
    pygame.display.update()    
    Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,500)
    Bicolour_Interface.turnOffAll()
    for button in sun:
        drawButtonWithColour(button,getButtonColour(button))

def Present():
    present = (buttons[2,5], buttons[4,5], buttons[2,7], buttons[4,7], buttons[3,5], buttons[3,6], buttons[3,7], buttons[2,6], buttons[4,6], buttons[3,4])
    for index in range(0,4):
        drawButtonWithColour(present[index],BRIGHTRED)
        arraysAddColour(present[index],RED)
        pygame.display.update()
    for index in range(4,9):
        drawButtonWithColour(present[index],BRIGHTYELLOW)
        arraysAddColour(present[index],YELLOW)
        pygame.display.update()
    drawButtonWithColour(present[9],BRIGHTGREEN)
    arraysAddColour(present[9],GREEN)
    pygame.display.update()
    Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,500)
    Bicolour_Interface.turnOffAll()

    for button in present:
        drawButtonWithColour(button,getButtonColour(button))

def Candle():
    for rows in range(4,8):
        for columns in range(2,5):
            drawButtonWithColour(buttons[columns,rows],BRIGHTYELLOW)
            arraysAddColour(buttons[columns,rows],BRIGHTYELLOW)
            pygame.display.update()
    drawButtonWithColour(buttons[3,2],BRIGHTRED)
    arraysAddColour(buttons[3,2],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[3,3],BRIGHTRED)
    arraysAddColour(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,500)
    Bicolour_Interface.turnOffAll()
    

def ChasingLights():
    for rows in range(0,8):
        if rows % 2 == 0:
            for columns in range(0,10):
                if columns >= 0 and columns < 8:
                    drawButtonWithColour(buttons[columns,rows],BRIGHTYELLOW)
                    Bicolour_Interface.turnOnLed(BRIGHTYELLOW,rows,columns)
                    pygame.display.update()
                if columns > 0 and columns < 9:
                    drawButtonWithColour(buttons[columns - 1,rows],BRIGHTGREEN)
                    Bicolour_Interface.turnOnLed(BRIGHTGREEN,rows,columns - 1)
                    pygame.display.update()
                if columns > 1:
                    drawButtonWithColour(buttons[columns - 2,rows],BRIGHTRED)
                    Bicolour_Interface.turnOnLed(BRIGHTRED,rows,columns - 2)
                    pygame.display.update()
        else:
            for columns in range(8,-3, -1):
                if columns < 8 and columns >= 0:
                    drawButtonWithColour(buttons[columns,rows],BRIGHTYELLOW)
                    Bicolour_Interface.turnOnLed(BRIGHTYELLOW,rows,columns)
                    pygame.display.update()
                if columns < 7 and columns >= -1 :
                    drawButtonWithColour(buttons[columns + 1,rows],BRIGHTGREEN)
                    Bicolour_Interface.turnOnLed(BRIGHTGREEN,rows,columns + 1)
                    pygame.display.update()
                if columns < 6 and columns >= -2:
                    drawButtonWithColour(buttons[columns + 2,rows],BRIGHTRED)
                    Bicolour_Interface.turnOnLed(BRIGHTRED,rows,columns + 2)
                    pygame.display.update()

            

def RaspberryPi():
    drawButtonWithColour(buttons[3,3],BRIGHTRED)
    arraysAddColour(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[4,3],BRIGHTRED)
    arraysAddColour(buttons[4,3],BRIGHTRED)
    pygame.display.update()
    
    for rows in range(4,7):
        for columns in range(2,6):
            drawButtonWithColour(buttons[columns,rows],BRIGHTRED)
            arraysAddColour(buttons[columns,rows],BRIGHTRED)
            pygame.display.update()
    drawButtonWithColour(buttons[3,7],BRIGHTRED)
    arraysAddColour(buttons[3,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[4,7],BRIGHTRED)
    arraysAddColour(buttons[4,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[4,2],BRIGHTGREEN)
    arraysAddColour(buttons[4,2],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColour(buttons[4,1],BRIGHTGREEN)
    arraysAddColour(buttons[4,1],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColour(buttons[5,1],BRIGHTGREEN)
    arraysAddColour(buttons[5,1],BRIGHTGREEN)
    pygame.display.update()

    Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,500)
    Bicolour_Interface.turnOffAll()
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColour(buttons[rows,columns], DARKGRAY)
    


def Hi():
    hi = (buttons[1,2], buttons[1,3], buttons[1,4], buttons[1,5], buttons[1,6], buttons[2,4], buttons[3,2], buttons[3,3], buttons[3,4],
          buttons[3,5], buttons[3,6], buttons[5,2], buttons[6,2], buttons[7,2], buttons[6,3], buttons[6,4], buttons[6,5], buttons[6,6],
          buttons[7,6], buttons[5,6])
    for button in hi:
        drawButtonWithColour(button,BRIGHTYELLOW)
        arraysAddColour(button,BRIGHTYELLOW)
        pygame.display.update()

    Bicolour_Interface.multiplexing(greenArray,redArray,yellowArray,500)


def FlashDisplay(Colour):
    drawAllButtonsWithColour(Colour)
    pygame.display.update()
    Bicolour_Interface.turnOnAll(Colour)
    pygame.time.wait(500)
    
def FlashingDot(Colour,animationSpeed = 100):
    for rows in range(0,8):
        for columns in range(0,8):
            flashColour = Colour
            rectangle = buttons[rows,columns]
            origSurf = DISPLAYSURF.copy()
            flashSurf = pygame.Surface((LEDSIZE, LEDSIZE))
            flashSurf = flashSurf.convert_alpha()
            r, g, b = flashColour
            for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
                for alpha in range(start, end, animationSpeed * step):
                    checkForQuit()
                    DISPLAYSURF.blit(origSurf, (0, 0))
                    flashSurf.fill((r, g, b, alpha))
                    DISPLAYSURF.blit(flashSurf, rectangle.topleft)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    Bicolour_Interface.turnOnLed(Colour,columns,rows)
            Bicolour_Interface.turnOffAll()
            DISPLAYSURF.blit(origSurf, (0, 0))
            
###################################################################################################################################################

    
if __name__ == '__main__':
    main()



