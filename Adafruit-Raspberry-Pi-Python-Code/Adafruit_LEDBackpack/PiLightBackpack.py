#!/usr/bin/python

#########                    PiLight                  ##################
#########                    Authors                  ################## 
#########               Veneta Haralampieva           ##################


import random, sys, time, smbus, pygame
from pygame.locals import *
import numpy as np
from numpy import *
from Adafruit_8x8 import ColorEightByEight

grid = ColorEightByEight(address=0x70)

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
bgColour = BLACK

# The Colour of the text in the buttons
TEXTColour = WHITE

LEDInitialColour = DARKGRAY

XMARGIN = int((WINDOWWIDTH - (LEDSIZE*BOARDWIDTH + (BOARDWIDTH - 1))) / 2 + 60)
YMARGIN = int((WINDOWHEIGHT - (LEDSIZE*BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Rect objects for each of the 64 buttons using a numpy array
buttons = np.empty((8,8), dtype=object)
for rows in range(0,8):
    for columns in range(0,8):
        buttons[rows,columns] = pygame.Rect(XMARGIN + rows*(LEDSIZE + BUTTONGAPSIZE),
                                            YMARGIN + columns*(LEDSIZE + BUTTONGAPSIZE),
                                            LEDSIZE, LEDSIZE)

# Numpy array, which stores all the Colours of the corresponding buttons 
buttonsColour = np.empty((8,8), dtype=object)# I2C bus that controls the LED matrix


# Main method
def main():
    global FPSCLOCK, yellowArray, redArray, greenArray, bus, piano1, \
           piano2, piano3, piano4, piano5, piano6, piano7, piano8, \
           DISPLAYSURF, CLEAR_SURF, CLEAR_BUTTON, NONE_SURF, \
           NONE_BUTTON, BASICFONT, LEDInitialColour, GREEN_SURF, \
           GREEN_BUTTON, YELLOW_SURF, YELLOW_BUTTON, RED_SURF, \
           RED_BUTTON, SEE_SURF, SEE_BUTTON, BASICTEXTFONT, \
           DEMO_SURF, DEMO_BUTTON, stateOfSelection, previousSelection, \
           GREENMODE, REDMODE, YELLOWMODE, NONEMODE
    
    # For the LED matrix - we need 3 arrays - one for each colour,
    # where we will keep what values need to be send to the matrix to
    # lit up a pattern
    yellowArray = [0,0,0,0,0,0,0,0]
    greenArray = [0,0,0,0,0,0,0,0]
    redArray = [0,0,0,0,0,0,0,0]
    

    # Initialising the game state
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pi Light)

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    BASICTEXTFONT = pygame.font.Font('freesansbold.ttf', 30)
    infoSurfOne = BASICFONT.render('Choose your pattern. On your left you can select colours.',
                                   2, WHITE)
    infoSurfTwo = BASICFONT.render('To change the colour of just one LED press on it one more time.',
                                   2, WHITE)
    infoSurfThree = BASICFONT.render('To unselect a button press NONE. When you are finished press SEE.',
                                     2, WHITE)
    infoRectOne = infoSurfOne.get_rect()
    infoRectOne.topleft = (10, WINDOWHEIGHT - 60)
    infoRectTwo = infoSurfTwo.get_rect()
    infoRectTwo.topleft = (10, WINDOWHEIGHT - 40)
    infoRectThree = infoSurfThree.get_rect()
    infoRectThree.topleft = (10, WINDOWHEIGHT - 20)

    piano1 = pygame.mixer.Sound('piano-a.wav')
    piano2 = pygame.mixer.Sound('piano-b.wav')
    piano3 = pygame.mixer.Sound('piano-c.wav')
    piano4 = pygame.mixer.Sound('piano-d.wav')
    piano5 = pygame.mixer.Sound('piano-e.wav')
    piano6 = pygame.mixer.Sound('piano-f.wav')
    piano7 = pygame.mixer.Sound('piano-#f.wav')
    piano8 = pygame.mixer.Sound('piano-g.wav')

    # Change LED colour buttons
    GREEN_SURF,GREEN_BUTTON = makeText(' GREEN  ',TEXTColour,GREEN,
                                       XMARGIN - 2*(LEDSIZE + BUTTONGAPSIZE),
                                       YMARGIN + 1*(LEDSIZE + BUTTONGAPSIZE))
    YELLOW_SURF,YELLOW_BUTTON = makeText('YELLOW',TEXTColour,YELLOW,
                                         XMARGIN - 2*(LEDSIZE + BUTTONGAPSIZE),
                                         YMARGIN + 2*(LEDSIZE + BUTTONGAPSIZE))
    RED_SURF,RED_BUTTON = makeText('    RED    ',TEXTColour,RED,
                                   XMARGIN - 2*(LEDSIZE + BUTTONGAPSIZE),
                                   YMARGIN + 3*(LEDSIZE + BUTTONGAPSIZE))

    # Unselect a single button
    NONE_SURF,NONE_BUTTON = makeText('  NONE   ',TEXTColour,DARKGRAY,
                                     XMARGIN - 2*(LEDSIZE + BUTTONGAPSIZE),
                                     YMARGIN + 4*(LEDSIZE + BUTTONGAPSIZE))

    # Clear the entira pattern
    CLEAR_SURF,CLEAR_BUTTON = makeText(' CLEAR  ',TEXTColour,GRAY,
                                       XMARGIN - 2*(LEDSIZE + BUTTONGAPSIZE),
                                       YMARGIN + 5*(LEDSIZE + BUTTONGAPSIZE))

    SEE_SURF, SEE_BUTTON = makeText('    SEE     ',TEXTColour,BLUE,
                                    XMARGIN + 1.5*(LEDSIZE + BUTTONGAPSIZE),
                                    YMARGIN + 8*(LEDSIZE + BUTTONGAPSIZE))

    DEMO_SURF, DEMO_BUTTON = makeText('   DEMO   ',TEXTColour,PURPLE,
                                      XMARGIN + 4.5*(LEDSIZE + BUTTONGAPSIZE),
                                      YMARGIN + 8*(LEDSIZE + BUTTONGAPSIZE))
    
    # Initialize some variables for a new game
    pattern = [] # stores the pattern of LEDs clicked
    
    # Set the Colour of all the LEDs to be the LEDColour
    initialColour(pattern)
            
    # When false it indicates that the player cannot click on the gray buttons
    drawOnBoard = True

    # Light green LEDs
    GREENMODE = 1

    # Light red LEDs
    REDMODE = 2

    # Light yellow LEDs
    YELLOWMODE = 3

    # Unselect a LED
    NONEMODE = 4

    # Which of the above is selected, initially green 
    stateOfSelection = GREENMODE

    # Which mode was previously selected
    previousSelection = 0
    while True: # main game loop

        clickedButton = None # button that was clicked 
        DISPLAYSURF.fill(bgColour)
        drawAllButtons()
        
        #initialColour()

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
                    if stateOfSelection == NONEMODE:
                        stateOfSelection = previousSelection
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
                            drawButtonWithColour(button,
                                                 getButtonColour(button))
                        flashButtonAnimationBig(clickedButton)
                        for button in pattern:
                            flashColour(button)
                            if button != None:
                                colour = 0
                                if getFlashColour(button) == BRIGHTRED:
                                    colour = 2
                                elif getFlashColour(button) == BRIGHTGREEN:
                                    colour = 1
                                elif getFlashColour(button) == BRIGHTYELLOW:
                                    colour = 3
                                grid.setPixel(getButtonRow(button),
                                              getButtonColumn(button),
                                              colour)
                            pygame.time.wait(FLASHDELAY)
                        #grid.multiplexing(greenArray,redArray,yellowArray,300)
                        pygame.time.wait(5000)
                        grid.clear()
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

                # If the pressed button was purple - play the demo
                elif clickedButton == PURPLE:
                    flashButtonAnimationBig(clickedButton)
                    for index in range(0,5):
                        FlashDisplay(BRIGHTYELLOW)
                        drawAllButtonsWithColour(DARKGRAY)

                        pygame.display.update()
                        FlashDisplay(BRIGHTRED)
                        drawAllButtonsWithColour(DARKGRAY)

                        pygame.display.update()
                        FlashDisplay(BRIGHTGREEN)
                        drawAllButtonsWithColour(DARKGRAY)

                        pygame.display.update()
                        index = index + 1

                    # Show some random shapes
                    RaspberryPi()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    
                    Hi()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    

                    
                    FlashingDot(BRIGHTYELLOW)
                    

                    ChristmasTree()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    
                    
                    drawAllButtonsWithColour(DARKGRAY)
                    pygame.display.update()
                    FlashingDot(BRIGHTGREEN)

                    Sun()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    pygame.display.update()
                    
                    FlashingDot(BRIGHTRED)
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    pygame.display.update()
                    
                    
                    Present()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)

                                        
                    Candle()
                    yellowArray = [0,0,0,0,0,0,0,0]
                    greenArray = [0,0,0,0,0,0,0,0]
                    redArray = [0,0,0,0,0,0,0,0]
                    drawAllButtonsWithColour(DARKGRAY)
                    
                    ChasingLights()

                # Deal with buttons from the matrix pressed
                else:
                    if drawOnBoard:
                        previousColour = getButtonColour(clickedButton)
                        if clickedButton in pattern:
                            changeButtonColour(clickedButton,pattern)
                            arrayChangeColour(clickedButton,previousColour)
                        else:
                            if stateOfSelection != NONEMODE:
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
    # get all the QUIT events
    for event in pygame.event.get(QUIT):
        # terminate if any QUIT events are present
        terminate() 
        Bicolour_Interface.turnOffAll()
        # get all the KEYUP events
    for event in pygame.event.get(KEYUP): 
        if event.key == K_ESCAPE:
            # terminate if the KEYUP event was for the Esc key
            terminate() 
            Bicolour_Interface.turnOffAll()
        # put the other KEYUP event objects back
        pygame.event.post(event)
        
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

    
# Flash the draw, done and see buttons
def flashButtonAnimationBig(Colour, animationSpeed=50):
    if Colour == RED:
        flashColour = BRIGHTRED
        rectangle = RED_BUTTON
        buttonWidth = RED_BUTTON.width
        buttonHeight = RED_BUTTON.height
    elif Colour == BLUE:
        flashColour = BRIGHTBLUE
        rectangle = SEE_BUTTON
        buttonWidth = SEE_BUTTON.width
        buttonHeight = SEE_BUTTON.height
    elif Colour == YELLOW:
        flashColour = BRIGHTYELLOW
        rectangle = YELLOW_BUTTON
        buttonWidth = YELLOW_BUTTON.width
        buttonHeight = YELLOW_BUTTON.height
    elif Colour == GREEN:
        flashColour = BRIGHTGREEN
        rectangle = GREEN_BUTTON
        buttonWidth = GREEN_BUTTON.width
        buttonHeight = GREEN_BUTTON.height
    elif Colour == PURPLE:
        flashColour = BRIGHTPURPLE
        rectangle = DEMO_BUTTON
        buttonWidth = DEMO_BUTTON.width
        buttonHeight = DEMO_BUTTON.height
    elif Colour == DARKGRAY:
        flashColour = DARKGRAY
        rectangle = NONE_BUTTON
        buttonWidth = NONE_BUTTON.width
        buttonHeight = NONE_BUTTON.height
    elif Colour == GRAY:
        flashColour = GRAY
        rectangle = CLEAR_BUTTON
        buttonWidth = CLEAR_BUTTON.width
        buttonHeight = CLEAR_BUTTON.height


    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((buttonWidth, buttonHeight))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColour
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
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
    
def drawAllButtonsWithColour(Colour):
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColour(buttons[rows,columns], Colour)

def drawAllButtons():
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColour(buttons[rows,columns], buttonsColour[rows,columns])
                
# Function that returns the button which has been clicked                
def getButtonClicked(x,y):
    for rows in range(0,8):
        for columns in range(0,8):
            if buttons[rows,columns].collidepoint((x,y)):
                return buttons[rows,columns]
    if RED_BUTTON.collidepoint((x,y)):
        return RED
    elif GREEN_BUTTON.collidepoint((x,y)):
        return GREEN
    elif YELLOW_BUTTON.collidepoint((x,y)):
        return YELLOW
    elif NONE_BUTTON.collidepoint((x,y)):
        return DARKGRAY
    elif SEE_BUTTON.collidepoint((x,y)):
        return BLUE
    elif DEMO_BUTTON.collidepoint((x,y)):
        return PURPLE
    elif CLEAR_BUTTON.collidepoint((x,y)):
        return GRAY
    
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
    
    
def getButtonColour(button):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                return buttonsColour[rows,columns]

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

def changeButtonColour(button,array):
    for rows in range(0,8):
        for columns in range(0,8):
            if button == buttons[rows,columns]:
                if stateOfSelection == GREENMODE:
                    if buttonsColour[rows,columns] == GREEN:
                        buttonsColour[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                    else:
                        buttonsColour[rows,columns] = GREEN
                elif stateOfSelection == REDMODE:
                    if buttonsColour[rows,columns] == RED:
                        buttonsColour[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                    else:
                        buttonsColour[rows,columns] = RED
                elif stateOfSelection == YELLOWMODE:
                    if buttonsColour[rows,columns] == YELLOW:
                        buttonsColour[rows,columns] = DARKGRAY
                        array.remove(button)
                        arraysRemove(button)
                    else:
                        buttonsColour[rows,columns] = YELLOW
                elif stateOfSelection == NONEMODE:
                    buttonsColour[rows,columns] = DARKGRAY
                    if button in array:
                        array.remove(button)
                        arraysRemove(button)
                            
                        
                    
############################ Demo ######################################
        
    
def ChristmasTree():
    tree = (buttons[4,0], buttons[3,1], buttons[4,1], buttons[5,1],
            buttons[2,2], buttons[3,2], buttons[4,2], buttons[5,2],
            buttons[6,2], buttons[2,3], buttons[3,3], buttons[4,3],
            buttons[5,3], buttons[6,3], buttons[1,4], buttons[2,4],
            buttons[3,4], buttons[4,4], buttons[5,4], buttons[6,4],
            buttons[7,4], buttons[1,5], buttons[2,5], buttons[3,5],
            buttons[4,5], buttons[5,5], buttons[6,5], buttons[7,5],
            buttons[0,6], buttons[1,6], buttons[2,6], buttons[3,6],
            buttons[5,6], buttons[6,6], buttons[7,6], buttons[4,6],
            buttons[4,7])

    for index in range(0,35):
        drawButtonWithColour(tree[index],BRIGHTGREEN)
        grid.setPixel(getButtonRow(tree[index]),getButtonColumn(tree[index]),1)
        arraysAddColour(tree[index],GREEN)
        pygame.display.update()
    drawButtonWithColour(tree[35],BRIGHTRED)
    grid.setPixel(getButtonRow(tree[35]),getButtonColumn(tree[35]),2)
    arraysAddColour(tree[35],RED)
    pygame.display.update()
    drawButtonWithColour(tree[36],BRIGHTRED)
    grid.setPixel(getButtonRow(tree[36]),getButtonColumn(tree[36]),2)
    arraysAddColour(tree[36],RED)
    pygame.display.update()
    pygame.time.wait(3000)
    grid.clear()
    for button in tree:
        drawButtonWithColour(button,getButtonColour(button))
        



def Sun():
    sun = (buttons[3,2], buttons[4,2], buttons[2,3], buttons[3,3],
           buttons[4,3], buttons[5,3], buttons[2,4], buttons[3,4],
           buttons[4,4], buttons[5,4], buttons[3,5], buttons[4,5])
    for index in range(0,12):
        drawButtonWithColour(sun[index],BRIGHTYELLOW)
        grid.setPixel(getButtonRow(sun[index]),getButtonColumn(sun[index]),3)
        arraysAddColour(sun[index],YELLOW)
        pygame.display.update()
    pygame.display.update()
    pygame.time.wait(3000)
    grid.clear()
    for button in sun:
        drawButtonWithColour(button,getButtonColour(button))

def Present():
    present = (buttons[2,5], buttons[4,5], buttons[2,7], buttons[4,7],
               buttons[3,5], buttons[3,6], buttons[3,7], buttons[2,6],
               buttons[4,6], buttons[3,4])
    for index in range(0,4):
        drawButtonWithColour(present[index],BRIGHTRED)
        grid.setPixel(getButtonRow(present[index]),getButtonColumn(present[index]),2)
        arraysAddColour(present[index],RED)
        pygame.display.update()
    for index in range(4,9):
        drawButtonWithColour(present[index],BRIGHTYELLOW)
        grid.setPixel(getButtonRow(present[index]),getButtonColumn(present[index]),3)
        arraysAddColour(present[index],YELLOW)
        pygame.display.update()
    drawButtonWithColour(present[9],BRIGHTGREEN)
    grid.setPixel(getButtonRow(present[9]),getButtonColumn(present[9]),1)
    arraysAddColour(present[9],GREEN)
    pygame.display.update()
    pygame.time.wait(3000)
    grid.clear()

    for button in present:
        drawButtonWithColour(button,getButtonColour(button))

def Candle():
    for rows in range(4,8):
        for columns in range(2,5):
            drawButtonWithColour(buttons[columns,rows],BRIGHTYELLOW)
            grid.setPixel(getButtonRow(buttons[columns,rows]),
                          getButtonColumn(buttons[columns,rows]),3)
            arraysAddColour(buttons[columns,rows],BRIGHTYELLOW)
            pygame.display.update()
    drawButtonWithColour(buttons[3,2],BRIGHTRED)
    grid.setPixel(getButtonRow(buttons[3,2]),getButtonColumn(buttons[3,2]),2)
    arraysAddColour(buttons[3,2],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[3,3],BRIGHTRED)
    grid.setPixel(getButtonRow(buttons[3,3]),getButtonColumn(buttons[3,3]),2)
    arraysAddColour(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    pygame.time.wait(3000)
    grid.clear()
    

def ChasingLights():
    for rows in range(0,8):
        if rows % 2 == 0:
            for columns in range(0,10):
                if columns >= 0 and columns < 8:
                    drawButtonWithColour(buttons[columns,rows],
                                         BRIGHTYELLOW)
                    grid.setPixel(getButtonRow(buttons[columns,rows]),
                                  getButtonColumn(buttons[columns,rows]),3)
                    pygame.display.update()
                if columns > 0 and columns < 9:
                    drawButtonWithColour(buttons[columns - 1,rows],
                                         BRIGHTGREEN)
                    grid.setPixel(getButtonRow(buttons[columns - 1,rows]),
                                  getButtonColumn(buttons[columns - 1,rows]),1)
                    pygame.display.update()
                if columns > 1:
                    drawButtonWithColour(buttons[columns - 2,rows],
                                         BRIGHTRED)
                    grid.setPixel(getButtonRow(buttons[columns - 2,rows]),
                                  getButtonColumn(buttons[columns - 2,rows]),2)
                    pygame.display.update()
        else:
            for columns in range(8,-3, -1):
                if columns < 8 and columns >= 0:
                    drawButtonWithColour(buttons[columns,rows],
                                         BRIGHTYELLOW)
                    grid.setPixel(getButtonRow(buttons[columns,rows]),
                                  getButtonColumn(buttons[columns,rows]),3)
                    pygame.display.update()
                if columns < 7 and columns >= -1 :
                    drawButtonWithColour(buttons[columns + 1,rows],
                                         BRIGHTGREEN)
                    grid.setPixel(getButtonRow(buttons[columns + 1,rows]),
                                  getButtonColumn(buttons[columns + 1,rows]),1)
                    pygame.display.update()
                if columns < 6 and columns >= -2:
                    drawButtonWithColour(buttons[columns + 2,rows],
                                         BRIGHTRED)
                    grid.setPixel(getButtonRow(buttons[columns + 2,rows]),
                                  getButtonColumn(buttons[columns + 2,rows]),2)
                    pygame.display.update()

    grid.clear()

            

def RaspberryPi():
    drawButtonWithColour(buttons[3,3],BRIGHTRED)
    grid.setPixel(getButtonRow(buttons[3,3]),getButtonColumn(buttons[3,3]),2)
    arraysAddColour(buttons[3,3],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[4,3],BRIGHTRED)
    grid.setPixel(getButtonRow(buttons[4,3]),getButtonColumn(buttons[4,3]),2)
    arraysAddColour(buttons[4,3],BRIGHTRED)
    pygame.display.update()
    
    for rows in range(4,7):
        for columns in range(2,6):
            drawButtonWithColour(buttons[columns,rows],BRIGHTRED)
            grid.setPixel(getButtonRow(buttons[columns,rows]),
                          getButtonColumn(buttons[columns,rows]),2)
            arraysAddColour(buttons[columns,rows],BRIGHTRED)
            pygame.display.update()
    drawButtonWithColour(buttons[3,7],BRIGHTRED)
    grid.setPixel(getButtonRow(buttons[3,7]),
                  getButtonColumn(buttons[3,7]),2)
    arraysAddColour(buttons[3,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[4,7],BRIGHTRED)
    grid.setPixel(getButtonRow(buttons[4,7]),
                  getButtonColumn(buttons[4,7]),2)
    arraysAddColour(buttons[4,7],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColour(buttons[4,2],BRIGHTGREEN)
    grid.setPixel(getButtonRow(buttons[4,2]),
                  getButtonColumn(buttons[4,2]),1)
    arraysAddColour(buttons[4,2],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColour(buttons[4,1],BRIGHTGREEN)
    grid.setPixel(getButtonRow(buttons[4,1]),
                  getButtonColumn(buttons[4,1]),1)
    arraysAddColour(buttons[4,1],BRIGHTGREEN)
    pygame.display.update()
    drawButtonWithColour(buttons[5,1],BRIGHTGREEN)
    grid.setPixel(getButtonRow(buttons[5,1]),
                  getButtonColumn(buttons[5,1]),1)
    arraysAddColour(buttons[5,1],BRIGHTGREEN)
    pygame.display.update()
    pygame.time.wait(3000)
    grid.clear()



def Hi():
    hi = (buttons[1,2], buttons[1,3], buttons[1,4], buttons[1,5],
          buttons[1,6], buttons[2,4], buttons[3,2], buttons[3,3],
          buttons[3,4], buttons[3,5], buttons[3,6], buttons[5,2],
          buttons[6,2], buttons[7,2], buttons[6,3], buttons[6,4],
          buttons[6,5], buttons[6,6], buttons[7,6], buttons[5,6])
    for button in hi:
        drawButtonWithColour(button,BRIGHTYELLOW)
        grid.setPixel(getButtonRow(button),getButtonColumn(button),3)
        arraysAddColour(button,BRIGHTYELLOW)
        pygame.display.update()
    pygame.time.wait(3000)
    grid.clear()




def FlashDisplay(Colour):
    drawAllButtonsWithColour(Colour)
    colour = 0
    if Colour == BRIGHTRED:
        for rows in range(0,8):
            grid.writeRowRaw(rows,0b1111111100000000)
    elif Colour == BRIGHTGREEN:
        for rows in range(0,8):
            grid.writeRowRaw(rows,0b0000000011111111)
    elif Colour == BRIGHTYELLOW:
        for rows in range(0,8):
            grid.writeRowRaw(rows,0b1111111111111111)
    
    
    pygame.display.update()
    pygame.time.wait(500)
    grid.clear()
    
def FlashingDot(colour,animationSpeed = 100):
    for rows in range(0,8):
        for columns in range(0,8):
            flashColour = colour
            rectangle = buttons[rows,columns]
            origSurf = DISPLAYSURF.copy()
            flashSurf = pygame.Surface((LEDSIZE, LEDSIZE))
            flashSurf = flashSurf.convert_alpha()
            r, g, b = flashColour
            colour = 0
            if flashColour == BRIGHTRED:
                colour = 2
            elif flashColour == BRIGHTGREEN:
                colour = 1
            elif flashColour == BRIGHTYELLOW:
                colour = 3
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, animationSpeed * step):
                    checkForQuit()
                    DISPLAYSURF.blit(origSurf, (0, 0))
                    flashSurf.fill((r, g, b, alpha))
                    DISPLAYSURF.blit(flashSurf, rectangle.topleft)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    grid.setPixel(rows,columns,colour)
                    pygame.time.wait(20)
            grid.clearPixel(rows,columns)
            DISPLAYSURF.blit(origSurf, (0, 0))
            
########## Dealing With Arrays and Multiplexing ######################## 

def arraysAdd(button):
    if button != None:
        Colour = getButtonColour(button)
        row = getButtonColumn(button)
        column = getButtonRow(button)
        if Colour == YELLOW or Colour == BRIGHTYELLOW:
            tempOne = 1<<column
            tempTwo = 1<<(column+8)
            temp = tempOne & tempTwo
            yellowArray[row] = yellowArray[row] | temp
        elif Colour == RED or Colour == BRIGHTRED:
            temp = 1<<(column+8)
            redArray[row] = redArray[row] | temp
        elif Colour == GREEN or Colour == BRIGHTGREEN:
            temp = 1<<column
            greenArray[row] = greenArray[row] | temp

def arraysAddColour(button,Colour):
    if button != None:
        row = getButtonColumn(button)
        column = getButtonRow(button)
        
        if Colour == YELLOW or Colour == BRIGHTYELLOW:
            tempOne = 1<<column
            tempTwo = 1<<(column+8)
            temp = tempOne & tempTwo
            yellowArray[row] = yellowArray[row] | temp
        elif Colour == RED or Colour == BRIGHTRED:
            temp = 1<<(column+8)
            redArray[row] = redArray[row] | temp
        elif Colour == GREEN or Colour == BRIGHTGREEN:
            temp = 1<<column
            greenArray[row] = greenArray[row] | temp

def arraysRemove(button):
    if button != None:
        Colour = getButtonColour(button)
        row = getButtonColumn(button)
        column = getButtonRow(button)
        if Colour == YELLOW or Colour == BRIGHTYELLOW:
            tempOne = 1<<column
            tempTwo = 1<<(column+8)
            temp = tempOne & tempTwo
            yellowArray[row] = yellowArray[row] ^ temp
        elif Colour == RED or Colour == BRIGHTRED:
            temp = 1<<(column+8)
            redArray[row] = redArray[row] ^ temp
        elif Colour == GREEN or Colour == BRIGHTGREEN:
            temp = 1<<column
            greenArray[row] = greenArray[row] ^ temp

def arraysRemoveColour(button,Colour):
    if button != None:
        row = getButtonColumn(button)
        column = getButtonRow(button)
        if Colour == YELLOW or Colour == BRIGHTYELLOW:
            tempOne = 1<<column
            tempTwo = 1<<(column+8)
            temp = tempOne & tempTwo
            yellowArray[row] = yellowArray[row] ^ temp
        elif Colour == RED or Colour == BRIGHTRED:
            temp = 1<<(column+8)
            redArray[row] = redArray[row] ^ temp
        elif Colour == GREEN or Colour == BRIGHTGREEN:
            temp = 1<<column
            greenArray[row] = greenArray[row] ^ temp


def arrayChangeColour(button,previousColour):
    if button != None:
        newColour = getButtonColour(button)
        arraysAddColour(button,newColour)
        arraysRemoveColour(button,previousColour)
                      
            
########################################################################
    
if __name__ == '__main__':
    main()



