#modem.py
"""
PyAudio example: Record a few seconds of audio and save to a WAVE
file.
"""
import pyaudio
import wave
import sys
import binascii
import math
import numpy

HIGH_NOTE = 440 #Note when 1
LOW_NOTE = 220 #Note when 0
BITRATE = 0.1 #Bits per second
RATE = 44100 #Specifies the desired sample rate (in Hz)
INPUT_FILE = "input.txt"

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=440, length=BITRATE, rate=RATE):
    chunks = []
    chunks.append(sine(frequency, length, rate))

    chunk = numpy.concatenate(chunks) * 0.25

    stream.write(chunk.astype(numpy.float32).tostring())

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1, rate=RATE, output=1)

a = open(INPUT_FILE, 'r')
c = a.read()
b = bin(int(binascii.hexlify(c), 16))

sample_stream = []
high_note = (b'\xFF'*100 + b'\0'*100) * 50 #TODO: Also record whats being played to a file
low_note = (b'\xFF'*50 + b'\0'*50) * 100
for bit in b[2:]:
    if bit == '1':
    	play_tone(stream, HIGH_NOTE)
        sample_stream.extend(high_note)
    else:
    	play_tone(stream, LOW_NOTE)
        sample_stream.extend(low_note)

sample_buffer = b''.join(sample_stream)

stream.close()
p.terminate()
