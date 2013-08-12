import math
import wave
from scipy.io.wavfile import write
import alsaaudio as aa
import numpy as np
import cProfile, pstats, io
from scikits.audiolab import play
from pylab import plot,show,axis, title, xlabel, ylabel, subplot

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
    newProduct = np.tile(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct

def generateSineWaveFrequency(frequency, waveTable, phaseIndex=0, soundLength=20, amplitude=1, samplingFrequency=44100):
    # The previous index from the look-up table
    previousPhase = phaseIndex
    
    print frequency    
    increment = float ((len(waveTable) * frequency)) / float(samplingFrequency)
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
    newProduct = np.tile(product,soundLength)
    if (len(newProduct) < (len(waveTable)*soundLength)):
        indexing = len(waveTable)*soundLength - len(newProduct)
        newProduct = np.hstack((newProduct,product[0:indexing]))
    return newProduct


def generateSineWaveRepeat(increment, waveTable, phaseIndex=0, soundLength=20, amplitude=1, samplingFrequency=44100):
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

###############  Amplitude distortion  ######################
tone = generateSineWave(20,waveTable,amplitude=0.7)
pr.disable()
s = io.StringIO()
pstats.Stats(pr).print_stats()
pr.enable()
play(tone)
plot(np.linspace(0, len(tone) / 44100, len(tone)), tone)
axis([0,0.01,-2,2])
show()
pr.disable()
s = io.StringIO()
pstats.Stats(pr).print_stats()

#############################################################

tone1 = generateSineWave(20,waveTable)
play(tone1)
plot(np.linspace(0, len(tone1) / 44100, len(tone1)), tone1)
axis([0,0.01,-2,2])
show()


############  Phase distortion  #############################
tone2 = generateSineWave(20,waveTable,phaseIndex=500)
plot(np.linspace(0, len(tone2) / 44100, len(tone2)), tone2)
axis([0,0.01,-2,2])
show()
play(tone2)
#############################################################

tone1diff = generateSineWaveRepeat(20,waveTable)
play(tone1diff)

####################  Piano keys  ###########################
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

#####################  Harmonics  ###########################
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
#############################################################

###################  Harmonics distortion  ##################
tonesum = tone1 + harmonic4
subplot(3,1,1)
plot(np.linspace(0, len(tone1) / 44100, len(tone1)), tone1)
axis([0,0.01,-2,2])
subplot(3,1,2)
plot(np.linspace(0, len(harmonic4) / 44100, len(harmonic4)), harmonic4)
axis([0,0.01,-2,2])
subplot(3,1,3)
plot(np.linspace(0, len(tonesum) / 44100, len(tonesum)), tonesum)
axis([0,0.01,-2,2])
show()
play(tonesum)
        
    
