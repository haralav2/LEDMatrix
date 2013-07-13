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


def TurnOffLEDS ():
   bus.write_byte_data(ADDRC,PORTA,0x00)
   bus.write_byte_data(ADDRC,PORTB,0x00)
   bus.write_byte_data(ADDRR,PORTA,0x00)

def Set_ColumnRed(row, col):
   bus.write_byte_data(ADDRR,PORTA,row)
   bus.write_byte_data(ADDRC,PORTA,0xFF)
   bus.write_byte_data(ADDRC,PORTB,col)

def Set_ColumnGreen(row,col):
   bus.write_byte_data(ADDRR,PORTA,row)
   bus.write_byte_data(ADDRC,PORTB,0xFF)
   bus.write_byte_data(ADDRC,PORTA,col)

def Set_ColumnYellow(row,col):
   bus.write_byte_data(ADDRR,PORTA,row)
   bus.write_byte_data(ADDRC,PORTB,row)
   bus.write_byte_data(ADDRC,PORTA,col)
   
# Initialise matrix
TurnOffLEDS()
matrix    = [0,0,0,0,0,0,0,0]
power     = []
weighting = [16,16,16,16,32,64,64,64]
#weighting = [2,2,8,8,16,32,64,64] # Change these according to taste

# Set up audio
wavfile = wave.open('/home/pi/Beethoven_Symphony_n.wav','r')
sample_rate = wavfile.getframerate()
no_channels = wavfile.getnchannels()
chunk       = 2048 # Use a multiple of 8
output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(no_channels)
output.setrate(sample_rate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(chunk)

# Return power array index corresponding to a particular frequency
def piff(val):
   return int(2*chunk*val/sample_rate)

power156 = 2*chunk*156/sample_rate
power313 = 2*chunk*313/sample_rate
power625 = 2*chunk*625/sample_rate
power1250 = 2*chunk*1250/sample_rate
power2500 = 2*chunk*2500/sample_rate
power5000 = 2*chunk*5000/sample_rate
power10000 = 2*chunk*10000/sample_rate
power20000 = 2*chunk*20000/sample_rate

def calculate_levels(data):
   global matrix
   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Apply FFT - real data
   power=np.abs(np.fft.rfft(data))
   # Remove last element in array to make it the same size as chunk
   power=np.delete(power,len(power)-1)
   # Find average 'amplitude' for specific frequency ranges in Hz
   matrix[0]= int(np.mean(power[0          :power156]))
   matrix[1]= int(np.mean(power[power156   :power313]))
   matrix[2]= int(np.mean(power[power313   :power625]))
   matrix[3]= int(np.mean(power[power625   :power1250]))
   matrix[4]= int(np.mean(power[power1250  :power2500]))
   matrix[5]= int(np.mean(power[power2500  :power5000]))
   matrix[6]= int(np.mean(power[power5000  :power10000]))
   matrix[7]= int(np.mean(power[power10000 :power20000]))
   # Tidy up column values for the LED matrix
   matrix=np.divide(np.multiply(matrix,weighting),1000000)
   print matrix
   # Set floor at 0 and ceiling at 8 for LED matrix
   matrix=np.divide(matrix,3)
   matrix=matrix.clip(0,8)
   #print matrix
   return matrix


print "Processing....."
data = wavfile.readframes(chunk)
while data!='':
    output.write(data)
    matrix=calculate_levels(data)
    for i in range (0,8):
      if (i<=2):
         Set_ColumnGreen((1<<matrix[i])-1,~(1<<i))
      elif (i>2 and i<=4):
         Set_ColumnYellow((1<<matrix[i])-1,~(1<<i))
      else:
         Set_ColumnRed((1<<matrix[i])-1,~(1<<i))
    time.sleep(0.5)
    data = wavfile.readframes(chunk)
    #TurnOffLEDS()
