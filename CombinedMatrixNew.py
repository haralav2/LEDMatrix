#############################################   Authors   ###########################################
###########################                     PiLight                  ############################
############################## Some of the code used here belongs to Al Sweigart  ###################
###########################    Inspired by the book - Making games with Python    ###################
###########################               Veneta Haralampieva           #############################





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
bgColor = BLACK

# The color of the text in the buttons
TEXTCOLOR = WHITE

LEDInitialColor = DARKGRAY

XMARGIN = int((WINDOWWIDTH - (LEDSIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2 + 60)
YMARGIN = int((WINDOWHEIGHT - (LEDSIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Rect objects for each of the 64 buttons using a numpy array
buttons = np.empty((8,8), dtype=object)
for rows in range(0,8):
    for columns in range(0,8):
        buttons[rows,columns] = pygame.Rect(XMARGIN + rows * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + columns * (LEDSIZE + BUTTONGAPSIZE),LEDSIZE, LEDSIZE)

# Numpy array, which stores all the colors of the corresponding buttons 
buttonsColor = np.empty((8,8), dtype=object)# I2C bus that controls the LED matrix
bus = smbus.SMBus(1)

# For the LED matrix - we need 6 arrays - 3 for rows and 3 for columns,where we will store the corresponding addresses
yellowArray = [0,0,0,0,0,0,0,0]
greenArray = [0,0,0,0,0,0,0,0]
redArray = [0,0,0,0,0,0,0,0]
    
# Main method
def main():
    global FPSCLOCK, yellowArray, redArray, greenArray, bus, piano1, piano2, piano3, piano4, piano5, piano6, piano7, piano8, DISPLAYSURF, NONE_SURF,NONE_BUTTON, BASICFONT, LEDInitialColor, GREEN_SURF, GREEN_BUTTON, YELLOW_SURF, YELLOW_BUTTON, RED_SURF, RED_BUTTON, SEE_SURF, SEE_BUTTON, BASICTEXTFONT, normalMode, yellowMode, redMode, DEMO_SURF, DEMO_BUTTON

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

    piano1 = pygame.mixer.Sound('piano-a.wav')
    piano2 = pygame.mixer.Sound('piano-b.wav')
    piano3 = pygame.mixer.Sound('piano-c.wav')
    piano4 = pygame.mixer.Sound('piano-#c.wav')
    piano5 = pygame.mixer.Sound('piano-d.wav')
    piano6 = pygame.mixer.Sound('piano-e.wav')
    piano7 = pygame.mixer.Sound('piano-f.wav')
    piano8 = pygame.mixer.Sound('piano-g.wav')

    

    GREEN_SURF,GREEN_BUTTON = makeText(' GREEN  ', TEXTCOLOR, GREEN, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 1 * (LEDSIZE + BUTTONGAPSIZE))
    YELLOW_SURF,YELLOW_BUTTON = makeText('YELLOW', TEXTCOLOR, YELLOW, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 2 * (LEDSIZE + BUTTONGAPSIZE))
    RED_SURF,RED_BUTTON = makeText('    RED    ', TEXTCOLOR, RED, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 3 * (LEDSIZE + BUTTONGAPSIZE))
    NONE_SURF,NONE_BUTTON = makeText('  NONE   ',TEXTCOLOR, DARKGRAY, XMARGIN - 2 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 4 * (LEDSIZE + BUTTONGAPSIZE))

    SEE_SURF, SEE_BUTTON = makeText('    SEE     ', TEXTCOLOR, BLUE, XMARGIN + 1.5 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))
    DEMO_SURF, DEMO_BUTTON = makeText('   DEMO   ', TEXTCOLOR, PURPLE, XMARGIN + 4.5 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of LEDs clicked
    
    # Set the color of all the LEDs to be the LEDColor
    initialColor(pattern)
            
    # When false it indicates that the player cannot click on the yellow buttons
    drawOnBoard = True
    normalMode = True
    redMode = False
    yellowMode = False
    
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
                    
        DISPLAYSURF.blit(infoSurfOne, infoRectOne)
        DISPLAYSURF.blit(infoSurfTwo, infoRectTwo)
        DISPLAYSURF.blit(infoSurfThree, infoRectThree)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)


                # If the pressed button was COLOUR - change the color of the whole matrix
                if clickedButton == GREEN:
                    normalMode = True
                    redMode = False
                    yellowMode = False
                elif clickedButton == YELLOW:
                    normalMode = False
                    redMode = False
                    yellowMode = True
                elif clickedButton == RED:
                    normalMode = False
                    redMode = True
                    yellowMode = False
                elif clickedButton == DARKGRAY:
                    normalMode = False
                    redMode = False
                    yellowMode = False

                #If the pressed button was SEE - display the pattern 
                elif clickedButton == BLUE:
                    drawOnBoard = False
                    if pattern == []:
                        drawOnBoard = True
                    else:
                        pygame.display.update()
                        pygame.time.wait(1000)
                        for button in pattern:
                            drawButtonWithColor(button, getButtonColor(button))
                        flashButtonAnimationBig(clickedButton)
                        for button in pattern:
                            flashColor(button)
                            if button != None:
                                turnOnLed(getFlashColor(button),getButtonColumn(button),getButtonRow(button))
                            pygame.time.wait(FLASHDELAY)
                        multiplexing(greenArray,redArray,yellowArray,300)
                        turnOffAll()
                        pattern = []
                        yellowArray = [0,0,0,0,0,0,0,0]
                        greenArray = [0,0,0,0,0,0,0,0]
                        redArray = [0,0,0,0,0,0,0,0]
                        for rows in range(0,8):
                            for columns in range(0,8):
                                buttonsColor[rows,columns] = DARKGRAY
                        pygame.display.update()
                        drawOnBoard = True

                # If the pressed button was purple - play the demo
                elif clickedButton == PURPLE:
                    flashButtonAnimationBig(clickedButton)
                    for index in range(0,5):
                        FlashDisplay(BRIGHTYELLOW)
                        drawAllButtonsWithColor(DARKGRAY)

                        # Turn on the Leds
                        turnOffAll()
                        pygame.display.update()
                        FlashDisplay(BRIGHTRED)
                        drawAllButtonsWithColor(DARKGRAY)

                        # Turn off the Leds
                        turnOffAll()
                        pygame.display.update()
                        FlashDisplay(BRIGHTGREEN)
                        drawAllButtonsWithColor(DARKGRAY)

                        # Turn on the Leds
                        turnOffAll()
                        pygame.display.update()
                        index = index + 1

                    # Show some random shapes
                    RaspberryPi()
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColor(DARKGRAY)
                    
                    Hi()
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColor(DARKGRAY)
                    

                    
                    FlashingDot(BRIGHTYELLOW)
                    turnOffAll()
                    

                    ChristmasTree()
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    
                    
                    drawAllButtonsWithColor(DARKGRAY)
                    pygame.display.update()
                    FlashingDot(BRIGHTGREEN)
                    turnOffAll()

                    Sun()
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColor(DARKGRAY)
                    pygame.display.update()
                    
                    FlashingDot(BRIGHTRED)
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColor(DARKGRAY)
                    pygame.display.update()
                    
                    
                    Present()
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColor(DARKGRAY)

                                        
                    Candle()
                    turnOffAll()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColor(DARKGRAY)
                    
                    ChasingLights()
                    turnOffAll()

                # Deal with buttons from the matrix pressed
                else:
                    if drawOnBoard:
                        previousColor = getButtonColor(clickedButton)
                        if clickedButton in pattern:
                            changeButtonColor(clickedButton,pattern)
                            arrayChangeColor(clickedButton,previousColor)
                        else:
                            changeButtonColor(clickedButton,pattern)
                            pattern.append(clickedButton)
                            arraysAdd(clickedButton)

            # Changing colors of individual Leds
            elif event.type == MOUSEBUTTONUP and event.button == 3:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
                if drawOnBoard:
                    previousColor = getButtonColor(clickedButton)
                    changeButtonColor(clickedButton,pattern)
                    if clickedButton in pattern:
                        arrayChangeColor(clickedButton,previousColor)
                    else:
                        pattern.append(clickedButton)
                        arraysAdd(clickedButton)
                
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
    


# Draw the buttons all with the same background color
def initialColor(array):
    for rows in range(0,8):
        for columns in range(0,8):
            if buttons[rows,columns] not in array:
                buttonsColor[rows,columns] = LEDInitialColor

# Light all the Leds that have been selected for some time
def flashColor(color, animationSpeed=100):
    for rows in range(0,8):
        for columns in range(0,8):
            if color == buttons[rows,columns]:
                sound = playSoundForButton(rows)
                flashColor = getFlashColor(buttons[rows,columns])
                rectangle = buttons[rows,columns]
                origSurf = DISPLAYSURF.copy()
                flashSurf = pygame.Surface((LEDSIZE, LEDSIZE))
                flashSurf = flashSurf.convert_alpha()
                r, g, b = flashColor
                sound.play()
                pygame.time.wait(200)
                for alpha in range(0, 255, animationSpeed):
                    checkForQuit()
                    DISPLAYSURF.blit(origSurf, (0,0))
                    flashSurf.fill((r, g, b, alpha))
                    DISPLAYSURF.blit(flashSurf,rectangle.topleft)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    
# Flash the draw, done and see buttons
def flashButtonAnimationBig(color, animationSpeed=50):
    if color == RED:
        flashColor = BRIGHTRED
        rectangle = RED_BUTTON
        buttonWidth = RED_BUTTON.width
        buttonHeight = RED_BUTTON.height
    elif color == BLUE:
        flashColor = BRIGHTBLUE
        rectangle = SEE_BUTTON
        buttonWidth = SEE_BUTTON.width
        buttonHeight = SEE_BUTTON.height
    elif color == YELLOW:
        flashColor = BRIGHTYELLOW
        rectangle = SEE_BUTTON
        buttonWidth = SEE_BUTTON.width
        buttonHeight = SEE_BUTTON.height
    elif color == GREEN:
        flashColor = BRIGHTGREEN
        rectangle = GREEN_BUTTON
        buttonWidth = GREEN_BUTTON.width
        buttonHeight = GREEN_BUTTON.height
    elif color == PURPLE:
        flashColor = BRIGHTPURPLE
        rectangle = DEMO_BUTTON
        buttonWidth = DEMO_BUTTON.width
        buttonHeight = DEMO_BUTTON.height
    elif color == DARKGRAY:
        flashColor = DARKGRAY
        rectangle = NONE_BUTTON
        buttonWidth = NONE_BUTTON.width
        buttonHeight = NONE_BUTTON.height


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

def drawButtonWithColor(button, color):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                pygame.draw.rect(DISPLAYSURF, color, button)


    DISPLAYSURF.blit(SEE_SURF, SEE_BUTTON)
    DISPLAYSURF.blit(DEMO_SURF, DEMO_BUTTON)
    DISPLAYSURF.blit(GREEN_SURF, GREEN_BUTTON)
    DISPLAYSURF.blit(YELLOW_SURF, YELLOW_BUTTON)
    DISPLAYSURF.blit(RED_SURF, RED_BUTTON)
    DISPLAYSURF.blit(NONE_SURF, NONE_BUTTON)
    
def drawAllButtonsWithColor(color):
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], color)

def drawAllButtons():
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], buttonsColor[rows,columns])
                
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

def changeButtonColor(button,array):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                if normalMode == True:
                    if buttonsColor[rows,columns] == DARKGRAY:
                        buttonsColor[rows,columns] = GREEN
                    elif buttonsColor[rows,columns] == GREEN:
                        buttonsColor[rows,columns] = YELLOW
                    elif buttonsColor[rows,columns] == YELLOW:
                        buttonsColor[rows,columns] = RED
                    elif buttonsColor[rows,columns] == RED:
                        buttonsColor[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                elif redMode == True:
                    if buttonsColor[rows,columns] == DARKGRAY:
                        buttonsColor[rows,columns] = RED
                    elif buttonsColor[rows,columns] == GREEN:
                        buttonsColor[rows,columns] = YELLOW
                    elif buttonsColor[rows,columns] == YELLOW:
                        buttonsColor[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                    elif buttonsColor[rows,columns] == RED:
                        buttonsColor[rows,columns] = GREEN
                        
                elif yellowMode == True:
                    if buttonsColor[rows,columns] == DARKGRAY:
                        buttonsColor[rows,columns] = YELLOW
                    elif buttonsColor[rows,columns] == GREEN:
                        buttonsColor[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                    elif buttonsColor[rows,columns] == YELLOW:
                        buttonsColor[rows,columns] = RED
                    elif buttonsColor[rows,columns] == RED:
                        buttonsColor[rows,columns] = GREEN
                else:
                    buttonsColor[rows,columns] = DARKGRAY
                    array.remove(button)
                    arraysRemove(button)
                        
                    
####################################################### Demo ########################################################################################
        
    
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
    
    for button in tree:
        drawButtonWithColor(button,getButtonColor(button))



def Sun():
    sun = (buttons[3,2], buttons[4,2], buttons[2,3], buttons[3,3], buttons[4,3], buttons[5,3], buttons[2,4], buttons[3,4],
           buttons[4,4], buttons[5,4], buttons[3,5], buttons[4,5])
    for index in range(0,12):
        drawButtonWithColor(sun[index],BRIGHTYELLOW)
        arraysAddColor(sun[index],YELLOW)
        pygame.display.update()
    pygame.display.update()    
    multiplexing(greenArray,redArray,yellowArray,500)
    
    for button in sun:
        drawButtonWithColor(button,getButtonColor(button))

def Present():
    present = (buttons[2,5], buttons[4,5], buttons[2,7], buttons[4,7], buttons[3,5], buttons[3,6], buttons[3,7], buttons[2,6], buttons[4,6], buttons[3,4])
    for index in range(0,4):
        drawButtonWithColor(present[index],BRIGHTRED)
        arraysAddColor(present[index],RED)
        pygame.display.update()
    for index in range(4,9):
        drawButtonWithColor(present[index],BRIGHTYELLOW)
        arraysAddColor(present[index],YELLOW)
        pygame.display.update()
    drawButtonWithColor(present[9],BRIGHTGREEN)
    arraysAddColor(present[9],GREEN)
    pygame.display.update()
    multiplexing(greenArray,redArray,yellowArray,500)

    for button in present:
        drawButtonWithColor(button,getButtonColor(button))

def Candle():
    for rows in range(4,8):
        for columns in range(2,5):
            drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
            arraysAddColor(buttons[columns,rows],BRIGHTYELLOW)
            pygame.display.update()
    drawButtonWithColor(buttons[3,2],BRIGHTRED)
    arraysAddColor(buttons[3,2],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[3,3],BRIGHTRED)
    arraysAddColor(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    multiplexing(greenArray,redArray,yellowArray,500)
    

def ChasingLights():
    for rows in range(0,8):
        if rows % 2 == 0:
            for columns in range(0,10):
                if columns >= 0 and columns < 8:
                    drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
                    turnOnLed(BRIGHTYELLOW,rows,columns)
                    pygame.display.update()
                if columns > 0 and columns < 9:
                    drawButtonWithColor(buttons[columns - 1,rows],BRIGHTGREEN)
                    turnOnLed(BRIGHTGREEN,rows,columns - 1)
                    pygame.display.update()
                if columns > 1:
                    drawButtonWithColor(buttons[columns - 2,rows],BRIGHTRED)
                    turnOnLed(BRIGHTRED,rows,columns - 2)
                    pygame.display.update()
        else:
            for columns in range(8,-3, -1):
                if columns < 8 and columns >= 0:
                    drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
                    turnOnLed(BRIGHTYELLOW,rows,columns)
                    pygame.display.update()
                if columns < 7 and columns >= -1 :
                    drawButtonWithColor(buttons[columns + 1,rows],BRIGHTGREEN)
                    turnOnLed(BRIGHTGREEN,rows,columns + 1)
                    pygame.display.update()
                if columns < 6 and columns >= -2:
                    drawButtonWithColor(buttons[columns + 2,rows],BRIGHTRED)
                    turnOnLed(BRIGHTRED,rows,columns + 2)
                    pygame.display.update()

            

def RaspberryPi():
    drawButtonWithColor(buttons[3,3],BRIGHTRED)
    arraysAddColor(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[4,3],BRIGHTRED)
    arraysAddColor(buttons[4,3],BRIGHTRED)
    pygame.display.update()
    
    for rows in range(4,7):
        for columns in range(2,6):
            drawButtonWithColor(buttons[columns,rows],BRIGHTRED)
            arraysAddColor(buttons[columns,rows],BRIGHTRED)
            pygame.display.update()
    drawButtonWithColor(buttons[3,7],BRIGHTRED)
    arraysAddColor(buttons[3,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[4,7],BRIGHTRED)
    arraysAddColor(buttons[4,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(buttons[4,2],BRIGHTGREEN)
    arraysAddColor(buttons[4,2],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColor(buttons[4,1],BRIGHTGREEN)
    arraysAddColor(buttons[4,1],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColor(buttons[5,1],BRIGHTGREEN)
    arraysAddColor(buttons[5,1],BRIGHTGREEN)
    pygame.display.update()

    multiplexing(greenArray,redArray,yellowArray,500)
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], YELLOW)


def Hi():
    hi = (buttons[1,2], buttons[1,3], buttons[1,4], buttons[1,5], buttons[1,6], buttons[2,4], buttons[3,2], buttons[3,3], buttons[3,4],
          buttons[3,5], buttons[3,6], buttons[5,2], buttons[6,2], buttons[7,2], buttons[6,3], buttons[6,4], buttons[6,5], buttons[6,6],
          buttons[7,6], buttons[5,6])
    for button in hi:
        drawButtonWithColor(button,BRIGHTYELLOW)
        arraysAddColor(button,BRIGHTYELLOW)
        pygame.display.update()

    multiplexing(greenArray,redArray,yellowArray,500)


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
            flashSurf = pygame.Surface((LEDSIZE, LEDSIZE))
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
                    turnOnLed(color,columns,rows)
            turnOffAll()
            DISPLAYSURF.blit(origSurf, (0, 0))
            
########## Dealing With Arrays and Multiplexing ######################## 

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

def arraysRemove(button):
    if button != None:
        color = getButtonColor(button)
        row = getButtonColumn(button)
        column = getButtonRow(button)
        temp = 1<<column
        if color == YELLOW or color == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] ^ temp
        elif color == RED or color == BRIGHTRED:
            redArray[row] = redArray[row] ^ temp
        elif color == GREEN or color == BRIGHTGREEN:
            greenArray[row] = greenArray[row] ^ temp

def arraysRemoveColor(button,color):
    if button != None:
        row = getButtonColumn(button)
        column = getButtonRow(button)
        temp = 1<<column
        if color == YELLOW or color == BRIGHTYELLOW:
            yellowArray[row] = yellowArray[row] ^ temp
        elif color == RED or color == BRIGHTRED:
            redArray[row] = redArray[row] ^ temp
        elif color == GREEN or color == BRIGHTGREEN:
            greenArray[row] = greenArray[row] ^ temp


def arrayChangeColor(button,previousColor):
    if button != None:
        newColor = getButtonColor(button)
        arraysAddColor(button,newColor)
        arraysRemoveColor(button,previousColor)
                      
            
################### Actual Matrix Visualisation ###############
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
            bus.write_byte_data(ADDRR,PORTA,0x00)
            greenOrYellow = patternGreen[row]|patternYellow[row]
            bus.write_byte_data(ADDRC,PORTA,~greenOrYellow)
            redOrYellow = patternRed[row]|patternYellow[row]
            bus.write_byte_data(ADDRC,PORTB,~redOrYellow)
            bus.write_byte_data(ADDRR,PORTA,1<<row)
            time.sleep(0.0002)
    turnOffAll()

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



