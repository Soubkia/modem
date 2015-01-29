#mo.py
#To Do: Place this all in a nice template so it's just one import statment... no internet to check syntax
import pyaudio
import wave
import sys
import binascii
import math
import numpy
import threading
import time
from modem import BITRATE
from modem import RATE
from modem import HIGH_NOTE
from modem import LOW_NOTE
from modem import INPUT_FILE_BIN
from modem import START_TIME
from modem import OUTPUT_FILENAME

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=440, length=BITRATE, rate=RATE):
    chunks = []
    chunks.append(sine(frequency, length, rate))

    chunk = numpy.concatenate(chunks) * 0.25

    stream.write(chunk.astype(numpy.float32).tostring())

def play_file(high_note=HIGH_NOTE, low_note=LOW_NOTE, bitrate=BITRATE, rate=RATE, b=INPUT_FILE_BIN):
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,
	                channels=1, 
	                rate=RATE, 
	                output=1)

	sample_stream = []
	high_note = (b'\xFF'*100 + b'\0'*100) * 50
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

#TODO: Record the raw data instead of recording through a microphone
#	   Reorganize this function's initialization
def record_file(RECORD_SECONDS=len(INPUT_FILE_BIN)*BITRATE):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 #Mono

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play1():
    while time.time() <= START_TIME:
        pass
    threading.Thread(target=record_file).start()
def play2():
    while time.time() <= START_TIME:
        pass
    threading.Thread(target=play_file).start()

def main():
	threading.Thread(target=play1).start()
	threading.Thread(target=play2).start()

if __name__ == "__main__":
    main()