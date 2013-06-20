import random, sys, time, pygame
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

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, DRAW_SURF, DRAW_BUTTON, COLOR_SURF, COLOR_BUTTON, SEE_SURF, SEE_BUTTON, BASICTEXTFONT, LEDColor, COLORColor, SEEColor, LEDFlashColor, COLORFlashColor,SEEFlashColor,DEMO_SURF, DEMO_BUTTON

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Matrix')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    BASICTEXTFONT = pygame.font.Font('freesansbold.ttf', 35)
    infoSurf = BASICFONT.render('Choose your pattern.Start by pressing DRAW,when finished - press DONE,to see what you have drawn press SEE', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 20)

    DRAW_SURF, DRAW_BUTTON = makeText('DRAW', TEXTCOLOR, BLUE, XMARGIN + 0 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))
    COLOR_SURF, COLOR_BUTTON = makeText('COLOUR', TEXTCOLOR, COLORColor, XMARGIN + 2 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))
    SEE_SURF, SEE_BUTTON = makeText('SEE', TEXTCOLOR, SEEColor, XMARGIN + 4.3 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))
    DEMO_SURF, DEMO_BUTTON = makeText('DEMO', TEXTCOLOR, PURPLE, XMARGIN + 5.5 * (BUTTONSIZE + BUTTONGAPSIZE),YMARGIN + 8 * (BUTTONSIZE + BUTTONGAPSIZE))

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of LEDs clicked

    # Set the color of all the LEDs to be the LEDColor
    for rows in range(0,8):
        for columns in range(0,8):
            buttonsColor[rows,columns] = LEDColor
            
    # When false it indicates that the player cannot click on the yellow buttons
    drawOnBoard = False
    
    while True: # main game loop
        clickedButton = None # button that was clicked 
        DISPLAYSURF.fill(bgColor)
        drawAllButtons()

        # If something is drawn it is shown on the board        
        for button in pattern:
            drawButtonWithColor(button, getFlashColor(button))

        
        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
                if clickedButton == BLUE:
                    pygame.display.update()
                    pygame.time.wait(1000)
                    drawOnBoard = True
                    flashButtonAnimationBig(clickedButton)
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
                    for rows in range(0,8):
                        for columns in range(0,8):
                            buttonsColor[rows,columns] = LEDColor
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
                        pygame.time.wait(FLASHDELAY)
                    pygame.time.wait(5000)
                    pattern = []
                elif clickedButton == PURPLE:
                    flashButtonAnimationBig(clickedButton)
                    for index in range(0,5):
                        FlashDisplay(BRIGHTYELLOW)
                        drawAllButtonsWithColor(RED)
                        pygame.display.update()
                        FlashDisplay(BRIGHTRED)
                        drawAllButtonsWithColor(GREEN)
                        pygame.display.update()
                        FlashDisplay(BRIGHTGREEN)
                        drawAllButtonsWithColor(YELLOW)
                        pygame.display.update()
                        index = index + 1
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
                else:
                    if drawOnBoard:
                        if clickedButton in pattern:
                            pattern.remove(clickedButton)
                        else:
                            pattern.append(clickedButton)                  
            elif event.type == MOUSEBUTTONUP and event.button == 3:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
                changeButtonColor(clickedButton)
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def terminate():
    pygame.quit()
    sys.exit()

def makeText(text, color, bgcolor, top, left):
    textSurf = BASICTEXTFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
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

def drawButtons(color):

    for rows in range(0,8):
        for columns in range(0,8):
             pygame.draw.rect(DISPLAYSURF, color, buttons[rows,columns])

    
    DISPLAYSURF.blit(DRAW_SURF, DRAW_BUTTON)
    DISPLAYSURF.blit(COLOR_SURF, COLOR_BUTTON)
    DISPLAYSURF.blit(SEE_SURF, SEE_BUTTON)    
    DISPLAYSURF.blit(DEMO_SURF, DEMO_BUTTON)

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
    pygame.time.wait(500)
    
def FlashingDot(color,animationSpeed = 50):
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
            DISPLAYSURF.blit(origSurf, (0, 0))    

     
if __name__ == '__main__':
    main()



