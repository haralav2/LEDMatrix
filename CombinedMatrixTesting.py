#############################################   Authors   ###########################################
###########################                     PiLight                  ############################
############################## Some of the code used here belongs to Al Sweigart  ###################
###########################    Inspired by the book - Making games with Python    ###################
###########################               Veneta Haralampieva           #############################





import random, sys, time, smbus, pygame
from pygame.locals import *
import numpy as np
from numpy import *



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

XMARGIN = int((WINDOWWIDTH - (LEDSIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (LEDSIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Rect objects for each of the 64 buttons using a numpy array
buttons = np.empty((8,8), dtype=object)
for rows in range(0,8):
    for columns in range(0,8):
        buttons[rows,columns] = pygame.Rect(XMARGIN + rows * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + columns * (LEDSIZE + BUTTONGAPSIZE),LEDSIZE, LEDSIZE)

# Numpy array, which stores all the colors of the corresponding buttons 
buttonsColor = np.empty((8,8), dtype=object)



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
    infoSurfOne = BASICFONT.render('Choose your pattern.Start by pressing DRAW,when you are finished pressed SEE.', 2, DARKGRAY)
    infoSurfTwo = BASICFONT.render('To change the colour of one LED press the right mouse button.', 2, DARKGRAY)
    infoSurfThree = BASICFONT.render('To change the colour of all LED press COLOUR.', 2, DARKGRAY)
    infoRectOne = infoSurfOne.get_rect()
    infoRectOne.topleft = (10, WINDOWHEIGHT - 60)
    infoRectTwo = infoSurfTwo.get_rect()
    infoRectTwo.topleft = (10, WINDOWHEIGHT - 40)
    infoRectThree = infoSurfThree.get_rect()
    infoRectThree.topleft = (10, WINDOWHEIGHT - 20)

    DRAW_SURF, DRAW_BUTTON = makeText('DRAW', TEXTCOLOR, BLUE, XMARGIN + 0 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))
    COLOR_SURF, COLOR_BUTTON = makeText('COLOUR', TEXTCOLOR, COLORColor, XMARGIN + 2.1 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))
    SEE_SURF, SEE_BUTTON = makeText('SEE', TEXTCOLOR, SEEColor, XMARGIN +4.8 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))
    DEMO_SURF, DEMO_BUTTON = makeText('DEMO', TEXTCOLOR, PURPLE, XMARGIN + 6.45 * (LEDSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (LEDSIZE + BUTTONGAPSIZE))

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of LEDs clicked
    
    # Set the color of all the LEDs to be the LEDColor
    initialColor(pattern)
            
    # When false it indicates that the player cannot click on the yellow buttons
    drawOnBoard = False
    
    while True: # main game loop

        


        
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
                    initialColor(pattern)

                #If the pressed button was SEE - display the pattern 
                elif clickedButton == GREEN:
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
                            #flashButtonAnimation(button)
                            changeColor(button)
                            
                            pygame.time.wait(FLASHDELAY)
                        pattern = []
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
                        pygame.display.update()
                        FlashDisplay(BRIGHTRED)
                        drawAllButtonsWithColor(GREEN)

                        # Turn off the Leds
                        pygame.display.update()
                        FlashDisplay(BRIGHTGREEN)
                        drawAllButtonsWithColor(YELLOW)

                        # Turn on the Leds
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
                        else:
                            pattern.append(clickedButton)

            # Changing colors of individual Leds
            elif event.type == MOUSEBUTTONUP and event.button == 3:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
                if drawOnBoard:
                    previousColor = getButtonColor(clickedButton)
                    changeButtonColor(clickedButton)
                    pattern.append(clickedButton)
                
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
                DISPLAYSURF.blit(origSurf, (0, 0))

# Draw the buttons all with the same background color
def initialColor(array):
    for rows in range(0,8):
        for columns in range(0,8):
            if buttons[rows,columns] not in array:
                buttonsColor[rows,columns] = LEDColor

# Light all the Leds that have been selected for some time
def changeColor(color, animationSpeed=100):
    for rows in range(0,8):
        for columns in range(0,8):
            if color == buttons[rows,columns]:
                flashColor = getFlashColor(buttons[rows,columns])
                rectangle = buttons[rows,columns]
                origSurf = DISPLAYSURF.copy()
                flashSurf = pygame.Surface((LEDSIZE, LEDSIZE))
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
        pygame.display.update()
    drawButtonWithColor(tree[35],BRIGHTRED)
    pygame.display.update()
    drawButtonWithColor(tree[36],BRIGHTRED)
    pygame.display.update()
    
    for button in tree:
        drawButtonWithColor(button,getButtonColor(button))



def Sun():
    sun = (buttons[3,2], buttons[4,2], buttons[2,3], buttons[3,3], buttons[4,3], buttons[5,3], buttons[2,4], buttons[3,4],
           buttons[4,4], buttons[5,4], buttons[3,5], buttons[4,5])
    for index in range(0,12):
        drawButtonWithColor(sun[index],BRIGHTYELLOW)
        pygame.display.update()
    pygame.display.update()    
    
    for button in sun:
        drawButtonWithColor(button,getButtonColor(button))

def Present():
    present = (buttons[2,5], buttons[4,5], buttons[2,7], buttons[4,7], buttons[3,5], buttons[3,6], buttons[3,7], buttons[2,6], buttons[4,6], buttons[3,4])
    for index in range(0,4):
        drawButtonWithColor(present[index],BRIGHTRED)
        pygame.display.update()
    for index in range(4,9):
        drawButtonWithColor(present[index],BRIGHTYELLOW)
        pygame.display.update()
    drawButtonWithColor(present[9],BRIGHTGREEN)
    pygame.display.update()

    for button in present:
        drawButtonWithColor(button,getButtonColor(button))

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
    
    for rows in range(0,8):
            for columns in range(0,8):
                drawButtonWithColor(buttons[rows,columns], YELLOW)



def ChasingLights():
    for rows in range(0,8):
        if rows % 2 == 0:
            for columns in range(0,10):
                if columns >= 0 and columns < 8:
                    drawButtonWithColor(buttons[columns,rows],BRIGHTYELLOW)
                    pygame.display.update()
                if columns > 0 and columns < 9:
                    drawButtonWithColor(buttons[columns - 1,rows],BRIGHTGREEN)
                    pygame.display.update()
                if columns > 1:
                    drawButtonWithColor(buttons[columns - 2,rows],BRIGHTRED)
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
            DISPLAYSURF.blit(origSurf, (0, 0))


            


    
if __name__ == '__main__':
    main()



