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
    
    
def generateSineWave(frequency, waveTable,soundLength = 10, amplitude=1, samplingFrequency=44100):
    phaseIndex = 0
    previousPhase = 0
    increment = float ((len(waveTable) * frequency)) / float(samplingFrequency)
    product = np.array([0 for x in range(len (waveTable) * soundLength)],np.float16)
    index = 0
    numberOfCycles  = 0
    while numberOfCycles != soundLength:
        while (phaseIndex != len(waveTable) and index != 4096*soundLength):
            phaseIndex = (previousPhase + increment) % len(waveTable)
            previousPhase = phaseIndex
            product[index] = amplitude*waveTable[int(phaseIndex)]
            index += 1
        numberOfCycles += 1
    return product
    
waveTable = generateLookUpTable(4096)
#print waveTable
pr.enable()
tone = generateSineWave(220, waveTable)
pr.disable()
s = io.StringIO()
pstats.Stats(pr).print_stats()
#print tone
play(tone)
#write('220hztone.wav',44100,tone)
#wavefile = wave.open('/home/pi/220hztone.wav', 'r')
#sampleRate = wavefile.getframerate()
#frameSize = 256
#output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
#output.setchannels(wavefile.getnchannels())
#output.setrate(sampleRate)
#output.setformat(aa.PCM_FORMAT_S16_LE)
#output.setperiodsize(frameSize)
#data = wavefile.readframes(frameSize)
#while len(data) != 0:
#    output.write(data)
#    data = wavefile.readframes(frameSize)
#output.close()

        
    
