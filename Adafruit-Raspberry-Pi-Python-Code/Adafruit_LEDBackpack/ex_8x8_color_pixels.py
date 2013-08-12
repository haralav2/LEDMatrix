#!/usr/bin/python

import time
import datetime
from Adafruit_8x8 import ColorEightByEight

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = ColorEightByEight(address=0x70)

print "Press CTRL+Z to exit"

iter = 0
index = 0
# Continually update the 8x8 display one pixel at a time
while(index<3):
  iter += 1

  for x in range(0, 8):
    for y in range(0, 8):
      grid.setPixel(x, y, iter % 4 )
      time.sleep(0.02)
  index += 1
grid.clear()

for count in range(0,20):
  grid.writeRowRaw(1, 0b0000000011111111)
  grid.writeRowRaw(0, 0b0011000011100111)
  grid.writeRowRaw(2, 0x1c00)
  grid.writeRowRaw(3, 1<<2)
  grid.writeRowRaw(4, 1<<10)
  time.sleep(0.0002)
time.sleep(1)
grid.clear()
