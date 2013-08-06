import math
import wave
from scipy.io.wavfile import write
import alsaaudio as aa
import numpy as np
import cProfile, pstats, io
from scikits.audiolab import play


pr = cProfile.Profile()

# Generates sine wave samples 
def generateLookUpTable(tableLength):
    numberOfEntries = 0
    # The sine of the first angle to be put into the matrix
    currentAngle = 0
    # Look up table to store the samples
    lookUpTable = np.array([0 for x in range(tableLength + 1)],np.float16)
    while(numberOfEntries != tableLength + 1):
        lookUpTable[numberOfEntries] = float (math.sin(math.radians(currentAngle)))
        numberOfEntries += 1
        currentAngle += (360 / float (tableLength))
    return lookUpTable
    
    
def generateSineWave(increment, waveTable, soundLength = 20, amplitude=1, samplingFrequency=44100):
    # Index that goes through the look-up table
    phaseIndex = 0

    # The previous index from the look-up table
    previousPhase = 0
    
    # Determine the frequency depending on the increment, the sampling
    # frequency and the wavetavle length
    frequency = float (increment*samplingFrequency)/float(len (waveTable))
    print frequency
    
    #increment = float ((len(waveTable) * frequency)) / float(samplingFrequency)
    product = np.array([0 for x in range(int(len (waveTable) / increment))],np.float16)

    # Index going through a new array that will contain only some of the samples from the
    # look-up table
    index = 0
    while (index != int(len(waveTable) / increment)):
        if index > int(len(waveTable) / (increment * 2)):
            product[index] = amplitude*waveTable[int(phaseIndex)]
        else:
            product[index] = waveTable[int(phaseIndex)]
                       
        phaseIndex = (previousPhase + increment) % len(waveTable)
        previousPhase = phaseIndex
        index += 1

    # Filling the array with a desired amount of samples to ensure length
    product = np.tile(product,int(increment))
    newProduct = np.tile(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct


    
waveTable = generateLookUpTable(4096)
pr.enable()
tone = generateSineWave(20, waveTable,amplitude=5)
pr.disable()
s = io.StringIO()
pstats.Stats(pr).print_stats()
pr.enable()
play(tone)
pr.disable()
s = io.StringIO()
pstats.Stats(pr).print_stats()
tone1 = generateSineWave(20,waveTable)
play(tone1)
harmonic1 = generateSineWave(40.9,waveTable)
play(harmonic1)
harmonic2 = generateSineWave(2*40.9,waveTable)
play(harmonic2)




        
    
