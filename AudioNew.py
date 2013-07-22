#!/usr/bin/env python

# 8 band Audio equaliser from wav file

import alsaaudio as aa
import smbus
from struct import unpack
import numpy as np
import wave
import time

bus=smbus.SMBus(1)    #Use '1' for newer Pi boards;

# Definitions for the MCP23017
ADDRR = 0x20   # I2C bus address of the 23017 Rows
ADDRC = 0x21   # I2C bus address of the 23017 Columns
DIRA  = 0x00   # PortA I/O direction
DIRB  = 0x01   # PortB I/O direction
PORTA = 0x12   # PortA data register
PORTB = 0x13   # PortB data register


#Set up the 23017 for 16 output pins
bus.write_byte_data(ADDRR,DIRA,0x00)   # All outputs on PortA address 0x20
bus.write_byte_data(ADDRR,DIRB,0x00)   # All outputs on PortB address 0x20
bus.write_byte_data(ADDRC,DIRA,0x00)   # All outputs on PortA address 0x21 - green
bus.write_byte_data(ADDRC,DIRB,0x00)   # All outputs on PortB address 0x21 - red


def turnOffLEDS ():
   bus.write_byte_data(ADDRC,PORTA,0x00)
   bus.write_byte_data(ADDRC,PORTB,0x00)
   bus.write_byte_data(ADDRR,PORTA,0x00)

def setColumnRed(row, col):
   bus.write_byte_data(ADDRR,PORTA,row)
   bus.write_byte_data(ADDRC,PORTA,0xFF)
   bus.write_byte_data(ADDRC,PORTB,col)

def setColumnGreen(row,col):
   bus.write_byte_data(ADDRR,PORTA,row)
   bus.write_byte_data(ADDRC,PORTB,0xFF)
   bus.write_byte_data(ADDRC,PORTA,col)

def setColumnYellow(row,col):
   bus.write_byte_data(ADDRR,PORTA,row)
   bus.write_byte_data(ADDRC,PORTB,row)
   bus.write_byte_data(ADDRC,PORTA,col)
   
# Initialise matrix
turnOffLEDS()
matrix    = [0,0,0,0,0,0,0,0]
power     = []
scaling = [2,2,2,2,2,2,2,2]

# Set up audio
wavfile = wave.open('/home/pi/BassCannon0.wav','r')
#wavfile = wave.open('/home/pi/Beethoven_Symphony_n.wav','r')
sampleRate = wavfile.getframerate()
frameSize       = 2048 # Use a multiple of 8
output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(wavfile.getnchannels())
output.setrate(sampleRate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(frameSize)

binWidth = frameSize / 8

def calculateColumns(data):
   global matrix
   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Use the fast fourier transform to convert a wave from the time domain
   # to the frequency domain
   realFourier = np.fft.rfft(data)
   # With the absolute function only postive values remain
   #print np.abs(realFourier)
   power = np.log10(np.add(np.abs(realFourier),0.01))**2
   #print power
   # Remove last element in array to make it the same size as frameSize
   power=np.delete(power,len(power)-1)
   # Find average 'amplitude' for specific frequency ranges in Hz
   matrix[0]= int(np.mean(power[0                         :(frameSize - 7*binWidth)]))
   matrix[1]= int(np.mean(power[(frameSize - 7*binWidth)  :(frameSize - 6*binWidth)]))
   matrix[2]= int(np.mean(power[(frameSize - 6*binWidth)  :(frameSize - 5*binWidth)]))
   matrix[3]= int(np.mean(power[(frameSize - 5*binWidth)  :(frameSize - 4*binWidth)]))
   matrix[4]= int(np.mean(power[(frameSize - 4*binWidth)  :(frameSize - 3*binWidth)]))
   matrix[5]= int(np.mean(power[(frameSize - 3*binWidth)  :(frameSize - 2*binWidth)]))
   matrix[6]= int(np.mean(power[(frameSize - 2*binWidth)  :(frameSize - binWidth)]))
   matrix[7]= int(np.mean(power[(frameSize - binWidth)    :frameSize]))
    
   # Tidy up column values for the LED matrix
   matrix=np.divide(np.multiply(matrix,2),5)
   # Make sure all values are between 0 and 8 
   matrix=matrix.clip(0,8)
   
   return matrix


print "Processing....."
data = wavfile.readframes(frameSize)
while data!='':
    output.write(data)
    matrix=calculateColumns(data)
    for i in range (0,8):
      if (i<=2):
         setColumnGreen((1<<matrix[i])-1,~(1<<i))
      elif (i>2 and i<=5):
         setColumnYellow((1<<matrix[i])-1,~(1<<i))
      else:
         setColumnRed((1<<matrix[i])-1,~(1<<i))
    data = wavfile.readframes(frameSize)
