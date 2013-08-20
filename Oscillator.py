#!/usr/bin/python

import math
import numpy as np
#import cProfile, pstats, io
from scikits.audiolab import play
from pylab import plot,show,axis, title, xlabel, ylabel, subplot, suptitle
import sys

#pr = cProfile.Profile()

''' Generates sine wave samples '''
def generateLookUpTable(tableLength):
    numberOfEntries = 0
    # The sine of the first angle to be put into the matrix
    currentAngle = 0
    # Look up table to store the samples
    lookUpTable = np.array([0 for x in range(tableLength + 1)]
                           ,np.float16)
    while(numberOfEntries != tableLength + 1):
        lookUpTable[numberOfEntries] = float(math.sin
                                             (math.radians
                                              (currentAngle)))
        numberOfEntries += 1
        currentAngle += (360 / float (tableLength))
    return lookUpTable
    

''' Generate a sine wave by suppling an increment - the rate at which to
   scan the look up table, supplying the look-up table is also necessary
'''
def generateSineWave(increment, waveTable, phaseIndex=0, soundLength=20,
                     amplitude=1, samplingFrequency=44100):
    # The previous index from the look-up table
    previousPhase = phaseIndex
    
    # Determine the frequency depending on the increment, the sampling
    # frequency and the wavetavle length
    frequency = (float (increment*samplingFrequency)
                 / float(len (waveTable)))
    print frequency
    product = np.array([0 for x in range(int(len (waveTable)
                                             / increment))],np.float16)

    # Index going through a new array that will contain only some of
    # the samples from the look-up table
    index = 0
    while (index != int(len(waveTable) / increment)):
        product[index] = amplitude*waveTable[int(phaseIndex)]                       
        phaseIndex = (previousPhase + increment) % len(waveTable)
        previousPhase = phaseIndex
        index += 1

    # Filling the array with a desired amount of samples to make
    # a signal the desired length
    product = np.tile(product,int(increment))
    newProduct = np.tile(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct


''' Generate a sine wave by suppling the desired frequency , supplying
    the look-up table is also necessary
'''
def generateSineWaveFrequency(frequency, waveTable, phaseIndex=0,
                              soundLength=20, amplitude=1,
                              samplingFrequency=44100):
    # The previous index from the look-up table
    previousPhase = phaseIndex    
    print frequency    
    increment = float ((len(waveTable) * float(frequency))
                       / float(samplingFrequency))
    product = np.array([0 for x in range(int(len (waveTable)
                                             / increment))],np.float16)

    # Index going through a new array that will contain only some of
    # the samples from the look-up table
    index = 0
    while (index != int(len(waveTable) / increment)):
        product[index] = amplitude*waveTable[int(phaseIndex)]                 
        phaseIndex = (previousPhase + increment) % len(waveTable)
        previousPhase = phaseIndex
        index += 1

    # Filling the array with a desired amount of samples to make
    # a signal the desired length
    product = np.tile(product,int(increment))
    newProduct = np.tile(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct


def generateSineWaveRepeat(increment, waveTable, phaseIndex=0,
                           soundLength=20, amplitude=1,
                           samplingFrequency=44100):
    # The previous index from the look-up table
    previousPhase = phaseIndex
    
    # Determine the frequency depending on the increment, the sampling
    # frequency and the wavetavle length
    frequency = (float (increment*samplingFrequency)
                 / float(len (waveTable)))
    print frequency
    product = np.array([0 for x in range(int(len (waveTable)
                                             / increment))],np.float16)

    # Index going through a new array that will contain only some of 
    # the samples from the look-up table
    index = 0
    while (index != int(len(waveTable) / increment)):
        product[index] = amplitude*waveTable[int(phaseIndex)]                      
        phaseIndex = (previousPhase + increment) % len(waveTable)
        previousPhase = phaseIndex
        index += 1

    # Filling the array with a desired amount of samples to make
    # a signal the desired length
    product = np.tile(product,int(increment))
    newProduct = np.repeat(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct


''' Generating a square wave by filling an array with only 0s and 1s '''
def generateSquareWave(tableLength, soundLength=20, amplitude=1, index=0):
    numberOfEntries = 0
    # The sine of the first angle to be put into the matrix
    currentAngle = 0
    # Look up table to store the samples
    lookUpTable = np.array([0 for x in range(tableLength + 1)],
                           np.float16)
    while(numberOfEntries != tableLength + 1):
        lookUpTable[numberOfEntries] = (amplitude * float
                                        (math.sin(math.radians
                                                  (currentAngle))))
        numberOfEntries += 1
        if currentAngle == 180:
            currentAngle = 0
        if (index % 4) == 0: 
            currentAngle += 90
        index += 1
    lookUpTable = np.repeat(lookUpTable,soundLength)
    return lookUpTable


########################################################################

continuing = True
print 'Choose how many table entries you would like your look up table to have?'
number = sys.stdin.read()
waveTable = generateLookUpTable(int(number))
while continuing == True:
    print 'Please supply the desired frequncy in Hz'
    suppliedFrequency = sys.stdin.read()
    #print 'Please define an amplitude - default is set to 1'
    #suppliedAmplitude = sys.stdin.read()
    print 'Supply signal length in seconds please'
    suppliedLength = 10*float(sys.stdin.read())
    generated = generateSineWaveFrequency(float(suppliedFrequency),
                                          waveTable,
                                          soundLength = suppliedLength)
    play(generated)
    plot(np.linspace(0, len(generated)/44100, len(generated)),generated)
    axis([0,0.01,-2,2])
    show()
    print 'Do you want to make another signal?'
    text = sys.stdin.read()
    if (text == "yes\n" or text == "y\n" or text == "yes" or text == "y"):
        continuing = True
    else:
        continuing = False

#pr.enable()

####################  Amplitude distortion  ############################

tone = generateSineWave(20,waveTable,amplitude=0.7)
#pr.disable()
#s = io.StringIO()
#pstats.Stats(pr).print_stats()
#pr.enable()
play(tone)
#pr.disable()
#s = io.StringIO()
#pstats.Stats(pr).print_stats()
plot(np.linspace(0, len(tone) / 44100, len(tone)), tone)
axis([0,0.01,-2,2])
show()


########################################################################

tone1 = generateSineWave(20,waveTable)
play(tone1)
plot(np.linspace(0, len(tone1) / 44100, len(tone1)), tone1)
axis([0,0.01,-2,2])
show()

sawtooth = generateSineWave(20,waveTable)
for index in range(1,13):
    sawtooth += generateSineWave(index*40.9,waveTable)
plot(np.linspace(0, len(sawtooth) / 44100, len(sawtooth)), sawtooth)
axis([0,0.01,-10,10])
show()
play(sawtooth)    

####################  Phase distortion  ################################
tone2 = generateSineWave(20,waveTable,phaseIndex=500)
plot(np.linspace(0, len(tone2) / 44100, len(tone2)), tone2)
axis([0,0.01,-2,2])
show()
play(tone2)

tone3 = generateSineWave(2,waveTable,phaseIndex=500)
plot(np.linspace(0, len(tone3) / 44100, len(tone3)), tone3)
axis([0,0.01,-2,2])
show()
play(tone3)
########################################################################

tone1diff = generateSineWaveRepeat(20,waveTable)
plot(np.linspace(0, len(tone1diff) / 44100, len(tone1diff)), tone1diff)
axis([0,0.01,-3,3])
show()
play(tone1diff)

####################  Piano keys  ######################################

key50 = generateSineWave(43.3,waveTable)
play(key50)
plot(np.linspace(0, len(key50) / 44100, len(key50)), key50)
axis([0,0.01,-2,2])
show()
key51 = generateSineWave(45.89,waveTable,amplitude=0.7)
play(key51)
key52 = generateSineWave(48.6,waveTable,amplitude=0.7)
play(key52)
key53 = generateSineWave(51.5,waveTable,amplitude=0.7)
play(key53)
key54 = generateSineWave(54.57,waveTable,amplitude=0.7)
play(key54)
key55 = generateSineWave(57.8,waveTable,amplitude=0.7)
play(key55)
key56 = generateSineWave(61.28,waveTable,amplitude=0.7)
play(key56)
key57 = generateSineWave(64.9,waveTable,amplitude=0.7)
play(key57)
key58 = generateSineWave(68.7,waveTable,amplitude=0.7)
play(key58)
key59 = generateSineWave(72.8,waveTable,amplitude=0.7)
play(key59)
key60 = generateSineWave(77.15,waveTable,amplitude=0.7)
play(key60)
plot(np.linspace(0, len(key60) / 44100, len(key60)), key60)
axis([0,0.01,-2,2])
show()

#####################  Harmonics  ######################################

harmonic1 = generateSineWave(40.9,waveTable)
play(harmonic1)
harmonic1diff = generateSineWaveFrequency(440,waveTable)
play(harmonic1diff)
harmonic2 = generateSineWave(2*40.9,waveTable)
play(harmonic2)
harmonic2diff = generateSineWaveFrequency(2*440,waveTable)
play(harmonic2diff)
harmonic3 = generateSineWave(3*40.9,waveTable)
play(harmonic3)
harmonic3diff = generateSineWaveFrequency(3*440,waveTable)
play(harmonic3diff)
harmonic4 = generateSineWave(4*40.9,waveTable)
play(harmonic4)
harmonic4diff = generateSineWaveFrequency(4*440,waveTable)
play(harmonic4diff)

########################################################################

###################  Harmonics distortion  #############################

tonesum = tone1 + harmonic4
subplot(3,1,1)
plot(np.linspace(0, len(tone1) / 44100, len(tone1)),tone1)
axis([0,0.01,-2,2])
subplot(3,1,2)
plot(np.linspace(0, len(harmonic4) / 44100, len(harmonic4)),harmonic4)
axis([0,0.01,-2,2])
subplot(3,1,3)
plot(np.linspace(0, len(tonesum) / 44100, len(tonesum)),tonesum)
axis([0,0.01,-2,2])
suptitle('Adding a tone and the 4th harmonic',fontsize=14,
         fontweight='bold')
show()
play(tonesum)

tone3 = generateSineWave(20,waveTable,amplitude=0.5)
play(tone3)

tonesum1 = tone3 + harmonic2
subplot(3,1,1)
plot(np.linspace(0,len(tone3) / 44100,len(tone3)),tone3)
axis([0,0.01,-2,2])
subplot(3,1,2)
plot(np.linspace(0,len(harmonic2) / 44100,len(harmonic2)),harmonic2)
axis([0,0.01,-2,2])
subplot(3,1,3)
plot(np.linspace(0,len(tonesum1) / 44100,len(tonesum1)),tonesum1)
axis([0,0.01,-2,2])
suptitle('Adding a tone and the 2nd harmonic',fontsize=14,
         fontweight='bold')
show()
play(tonesum)
            
squaretone = generateSquareWave(4096)
play(squaretone)
plot(np.linspace(0, len(squaretone) / 44100,len(squaretone)),squaretone)
axis([0,0.01,-2,2])
show()

squareandharmonic = squaretone + harmonic2
subplot(3,1,1)
plot(np.linspace(0,len(squaretone) / 44100,len(squaretone)),squaretone)
axis([0,0.01,-2,2])
subplot(3,1,2)
plot(np.linspace(0,len(harmonic2) / 44100,len(harmonic2)),harmonic2)
axis([0,0.01,-2,2])
subplot(3,1,3)
plot(np.linspace(0,len(squareandharmonic) / 44100,
                 len(squareandharmonic)),squareandharmonic)
axis([0,0.01,-2,2])
suptitle('Adding a square wave and a 2nd harmonic',fontsize=14,
         fontweight='bold')
show()
play(squareandharmonic)


squareandtone = squaretone + tone1
subplot(3,1,1)
plot(np.linspace(0,len(squaretone) / 44100,len(squaretone)),squaretone)
axis([0,0.01,-2,2])
subplot(3,1,2)
plot(np.linspace(0,len(tone1) / 44100,len(tone1)),tone1)
axis([0,0.01,-2,2])
subplot(3,1,3)
plot(np.linspace(0,len(squareandtone) / 44100,
                 len(squareandtone)),squareandtone)
axis([0,0.01,-2,2])
suptitle('Adding a square wave and 215 Hz tone',fontsize=14,
         fontweight='bold')
show()
play(squareandtone)
