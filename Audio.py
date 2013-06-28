#!/usr/bin/env python

# 8 band Audio equaliser from wav file

import alsaaudio as aa
import smbus
from struct import unpack
import numpy as np
import wave

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
   bus.write_byte_data(ADDRR,PORTB,0x00)

def Set_Column(row, col):
   bus.write_byte_data(ADDRR,PORTB,row)
   bus.write_byte_data(ADDRC,PORTA, col)
   #bus.write_byte_data(ADDR, PORTA, col)
   #bus.write_byte_data(ADDR, PORTB, row)
   
# Initialise matrix
TurnOffLEDS()
matrix    = [0,0,0,0,0,0,0,0]
power     = []
weighting = [2,2,8,8,16,32,64,64] # Change these according to taste

# Set up audio
wavfile = wave.open('/home/pi/test3.wav','r')
sample_rate = wavfile.getframerate()
no_channels = wavfile.getnchannels()
chunk       = 4096 # Use a multiple of 8
output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(no_channels)
output.setrate(sample_rate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(chunk)

# Return power array index corresponding to a particular frequency
def piff(val):
   return int(2*chunk*val/sample_rate)

def calculate_levels(data, chunk,sample_rate):
   global matrix
   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Apply FFT - real data
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   # Find average 'amplitude' for specific frequency ranges in Hz
   power = np.abs(fourier)
   matrix[0]= int(np.mean(power[piff(0)    :piff(156):1]))
   matrix[1]= int(np.mean(power[piff(156)  :piff(313):1]))
   matrix[2]= int(np.mean(power[piff(313)  :piff(625):1]))
   matrix[3]= int(np.mean(power[piff(625)  :piff(1250):1]))
   matrix[4]= int(np.mean(power[piff(1250) :piff(2500):1]))
   matrix[5]= int(np.mean(power[piff(2500) :piff(5000):1]))
   matrix[6]= int(np.mean(power[piff(5000) :piff(10000):1]))
   matrix[7]= int(np.mean(power[piff(10000):piff(20000):1]))
   # Tidy up column values for the LED matrix
   matrix=np.divide(np.multiply(matrix,weighting),1000000)
   # Set floor at 0 and ceiling at 8 for LED matrix
   matrix=matrix.clip(0,8) 
   return matrix


print "Processing....."
data = wavfile.readframes(chunk)
while data!='':
    output.write(data)
    matrix=calculate_levels(data, chunk,sample_rate)
    for i in range (0,8):
        Set_Column((1<<matrix[i])-1,0xFF^(1<<i))
    data = wavfile.readframes(chunk)
    TurnOffLEDS()
