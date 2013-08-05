import math
import wave
from scipy.io.wavfile import write
import alsaaudio as aa
import numpy as np
import cProfile, pstats, io
from scikits.audiolab import play


pr = cProfile.Profile()

def generateLookUpTable(tableLength):
    numberOfEntries = 0
    currentAngle = 0
    lookUpTable = np.array([0 for x in range(tableLength + 1)],np.float16)
    while(numberOfEntries != tableLength + 1):
        lookUpTable[numberOfEntries] = float (math.sin(math.radians(currentAngle)))
        numberOfEntries += 1
        currentAngle += (360 / float (tableLength))
    return lookUpTable
    
    
def generateSineWave(increment, waveTable,soundLength = 20, amplitude=1, samplingFrequency=44100):
    phaseIndex = 0
    previousPhase = 0
    frequency = float (increment*samplingFrequency)/float(len (waveTable))
    print frequency
    #increment = float ((len(waveTable) * frequency)) / float(samplingFrequency)
    product = np.array([0 for x in range(int(len (waveTable) / increment))],np.float16)
    index = 0
    numberOfCycles  = 0
    while (index != int(len(waveTable) / increment)):
        product[index] = amplitude*waveTable[int(phaseIndex)]
        phaseIndex = (previousPhase + increment) % len(waveTable)
        previousPhase = phaseIndex
        index += 1
    product = np.tile(product,int(increment-1))
    product = np.tile(product,soundLength)
    return product
    
waveTable = generateLookUpTable(4096)
#print waveTable
pr.enable()
tone = generateSineWave(40, waveTable)
pr.disable()
s = io.StringIO()
pstats.Stats(pr).print_stats()
#print tone
play(tone)
tone1 = generateSineWave(64,waveTable)
play(tone1)


        
    
