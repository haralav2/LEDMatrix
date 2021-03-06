#!/usr/bin/env python

import alsaaudio as aa
import smbus
from struct import unpack
import numpy as np
import wave
import time
import Bicolour_Interface


# Initialise matrix
Bicolour_Interface.initialise()
matrix = [0,0,0,0,0,0,0,0]
frequencyRange = []
scaling = [2,2,2,2,2,2,2,2]

# Set up audio

# Open the wave file
wavfile = wave.open('/home/pi/Beethoven_Symphony_n.wav','r')

# We are going to use the frame rate from the file as a
# sample rate in our output
sampleRate = wavfile.getframerate()

# Set the frame size - advisable to be  multiple of 8
frameSize = 2048

# Setup the output 
output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)

# Set the channels of the output to be the same as those of our file
output.setchannels(wavfile.getnchannels())
output.setrate(sampleRate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(frameSize)

# Gives us the size of each of the frequncy range grouped together
binWidth = frameSize / 8

def calculateColumns(data):
   global matrix
   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   
   # Use the fast fourier transform to convert a wave from the time 
   # domain to the frequency domain
   realFourier = np.fft.rfft(data)
   
   # With the absolute function only postive values remain   
   # 0.01 is added to deal with the case when a frequency range is
   # not present - sometimes in the beginning of a file there is silence
   # Keeps from log10(0) to throw an error later on 
   frequencyRange = np.log10(np.add(np.abs(realFourier),0.01))**2
   
   # Remove last element in array to make it the same size as frameSize
   frequencyRange=np.delete(frequencyRange,len(frequencyRange)-1)
   
   # Find average amplitude for specific frequency ranges in Hz
   matrix[0]= int(np.mean(frequencyRange[0                         
                                         :(frameSize - 7*binWidth)]))
   matrix[1]= int(np.mean(frequencyRange[(frameSize - 7*binWidth)
                                         :(frameSize - 6*binWidth)]))
   matrix[2]= int(np.mean(frequencyRange[(frameSize - 6*binWidth)
                                         :(frameSize - 5*binWidth)]))
   matrix[3]= int(np.mean(frequencyRange[(frameSize - 5*binWidth)
                                         :(frameSize - 4*binWidth)]))
   matrix[4]= int(np.mean(frequencyRange[(frameSize - 4*binWidth)
                                         :(frameSize - 3*binWidth)]))
   matrix[5]= int(np.mean(frequencyRange[(frameSize - 3*binWidth)
                                         :(frameSize - 2*binWidth)]))
   matrix[6]= int(np.mean(frequencyRange[(frameSize - 2*binWidth)
                                         :(frameSize - binWidth)]))
   matrix[7]= int(np.mean(frequencyRange[(frameSize - binWidth)
                                         :frameSize]))
    
   # Tidy up column values for the LED matrix
   matrix=np.divide(np.multiply(matrix,2),5)

   # Make sure all values are between 0 and 8 
   matrix=matrix.clip(0,8)
   return matrix

data = wavfile.readframes(frameSize)
while len(data) != 0:
   if len(data) == 4*frameSize:
       output.write(data)
       matrix=calculateColumns(data)
       for column in range (0,8):
         if (column<=2):
            Bicolour_Interface.setColumnGreen(matrix[column],column)
         elif (column>2 and column<=5):
            Bicolour_Interface.setColumnYellow(matrix[column],column)
         else:
            Bicolour_Interface.setColumnRed(matrix[column],column)
         Bicolour_Interface.turnOffAllAudio()
       Bicolour_Interface.turnOffAllAudio()
   data = wavfile.readframes(frameSize)
output.close()
