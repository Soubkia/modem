# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np
from modem import BITRATE
from modem import RATE
from modem import HIGH_NOTE
from modem import LOW_NOTE
from modem import INPUT_FILE_BIN
from modem import START_TIME
from modem import OUTPUT_FILENAME

chunk = 1024
# http://en.wikipedia.org/wiki/Goertzel_algorithm
# open up a wave
wf = wave.open('output.wav', 'rb')
swidth = wf.getsampwidth() # Each sample is 2 bytes
RATE = wf.getframerate() # 44100 samples are taken per second (356352 total frames currently)
chunk = int(RATE*BITRATE)
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

# read some data
data = wf.readframes(chunk)
count = 0 # Debug
# play stream and find the frequency of each chunk
while len(data) == chunk*swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print "The freq is %f Hz. (frame %s)" % (thefreq, count)
    else:
        thefreq = which*RATE/chunk
        print "The freq is %f Hz. (frame %s)" % (thefreq, count)
    # read some more data
    data = wf.readframes(chunk)
    count = count + 1 # Debug
if data:
    stream.write(data)
stream.close()
p.terminate()
