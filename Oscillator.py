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
    
    
def generateSineWave(increment, waveTable, phaseIndex=0, soundLength=20, amplitude=1, samplingFrequency=44100):
    # Index that goes through the look-up table
    #phaseIndex = 0

    # The previous index from the look-up table
    previousPhase = phaseIndex
    
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


def generateSineWaveRepeat(increment, waveTable, phaseIndex=0, soundLength=20, amplitude=1, samplingFrequency=44100):
    # Index that goes through the look-up table
    #phaseIndex = 0

    # The previous index from the look-up table
    previousPhase = phaseIndex
    
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
        product[index] = amplitude*waveTable[int(phaseIndex)]                      
        phaseIndex = (previousPhase + increment) % len(waveTable)
        previousPhase = phaseIndex
        index += 1

    # Filling the array with a desired amount of samples to ensure length
    product = np.tile(product,int(increment))
    newProduct = np.repeat(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct
    
waveTable = generateLookUpTable(4096)
pr.enable()
tone = generateSineWave(20, waveTable,amplitude=1.005)
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
tone2 = generateSineWave(20,waveTable,phaseIndex=500)
play(tone2)
tone1diff = generateSineWaveRepeat(20,waveTable)
play(tone1diff)


harmonic1 = generateSineWave(40.9,waveTable)
play(harmonic1)
#######################################################################################
key50 = generateSineWave(43.3,waveTable)
play(key50)
key51 = generateSineWave(45.89,waveTable)
play(key51)
key52 = generateSineWave(48.6,waveTable)
play(key52)
key53 = generateSineWave(51.5,waveTable)
play(key53)
key54 = generateSineWave(54.57,waveTable)
play(key54)
key55 = generateSineWave(57.8,waveTable)
play(key55)
key56 = generateSineWave(61.28,waveTable)
play(key56)
key57 = generateSineWave(64.9,waveTable)
play(key57)
key58 = generateSineWave(68.7,waveTable)
play(key58)
key59 = generateSineWave(72.8,waveTable)
play(key59)
key60 = generateSineWave(77.15,waveTable)
play(key60)
#######################################################################################
harmonic2 = generateSineWave(2*40.9,waveTable)
play(harmonic2)




        
    
