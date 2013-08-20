#!/usr/bin/python

import time
import datetime
import font8x8
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 8x8 Pixel Display
# ===========================================================================

class EightByEight:
  disp = None

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    self.disp = LEDBackpack(address=address, debug=debug)

  def writeRowRaw(self, charNumber, value):
    "Sets a row of pixels using a raw 16-bit value"
    if (charNumber > 7):
      return
    # Set the appropriate row
    self.disp.setBufferRow(charNumber, value)

  def clearPixel(self, x, y):
    "A wrapper function to clear pixels (purely cosmetic)"
    self.setPixel(x, y, 0)

  def setPixel(self, x, y, color=1):
    "Sets a single pixel"
    if (x >= 8):
      return
    if (y >= 8):
      return    
    x += 7   # ATTN: This might be a bug?  On the color matrix, this causes x=0 to draw on the last line instead of the first.
    x %= 8
    # Set the appropriate pixel
    buffer = self.disp.getBuffer()
    if (color):
      self.disp.setBufferRow(y, buffer[y] | 1 << x)
    else:
      self.disp.setBufferRow(y, buffer[y] & ~(1 << x))

  def clear(self):
    "Clears the entire display"
    self.disp.clear()

class ColorEightByEight(EightByEight):
  def setPixel(self, x, y, color=1):
    "Sets a single pixel"
    if (x >= 8):
      return
    if (y >= 8):
      return

    x %= 8

    # Set the appropriate pixel
    buffer = self.disp.getBuffer()

    # TODO : Named color constants?
    # ATNN : This code was mostly taken from the arduino code, but with the addition of clearing the other bit when setting red or green.
    #        The arduino code does not do that, and might have the bug where if you draw red or green, then the other color, it actually draws yellow.
    #        The bug doesn't show up in the examples because it's always clearing.

    if (color == 1):
      self.disp.setBufferRow(y, (buffer[y] | (1 << x)) & ~(1 << (x+8)) )
    elif (color == 2):
      self.disp.setBufferRow(y, (buffer[y] | 1 << (x+8)) & ~(1 << x) )
    elif (color == 3):
      self.disp.setBufferRow(y, buffer[y] | (1 << (x+8)) | (1 << x) )
    else:
      self.disp.setBufferRow(y, buffer[y] & ~(1 << x) & ~(1 << (x+8)) )


  # Scrolling a pattern
  def scroll(self,pattern,bufferText):
    for row in range(0,8):
        pattern[row] >>= 1
        if self.bufferText[row] & 0x01:
            pattern[row] |= 0x80
        bufferText[row] >>= 1


  # Using the font display the text on the matrix
  def textScroll(self,ledColour,text):
    speed = 8
    pattern = [0,0,0,0,0,0,0,0]
    for character in text:
        self.bufferText = list(font8x8.font8x8[ord(character)])
        for count in range(0,8):
            self.multiplexingText(ledColour,pattern,speed)
            self.scroll(pattern,self.bufferText)

  # Going through all the rows quickly to create the illusion of a static image
  def multiplexingText(self,colour,pattern,count):
    if colour == "2\n" or colour == "green\n" or colour == "2" or colour == "green":
        for count in range(0,count):
            for row in range(0,8):
              self.writeRowRaw(row,pattern[row])
    elif colour == "3\n" or colour == "yellow\n" or colour == "3" or colour == "yellow":
        for count in range(0,count):
            for row in range(0,8):
              self.writeRowRaw(row,(pattern[row] ^ pattern[row]<<8))
    else:
        for count in range(0,count):
            for row in range(0,8):
              self.writeRowRaw(row,pattern[row]<<8)
    time.sleep(0.0002)
