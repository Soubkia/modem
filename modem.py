#modem.py
import pyaudio
import wave
import sys
import binascii
import math
import numpy
import threading
import time

START_TIME = time.time()+1 #Timekeeper (waits 1 second to start)
HIGH_NOTE = 440 #Note when 1
LOW_NOTE = 220 #Note when 0
BITRATE = 0.5 #Bits per second
RATE = 44100 #Specifies the desired sample rate (in Hz)
INPUT_FILENAME = "input.txt" #File to be played
a = open(INPUT_FILENAME, 'r') #TODO: I think this is just getting the ascii binary not the full bytedata of the text file
c = a.read()
INPUT_FILE_BIN = bin(int(binascii.hexlify(c), 16)) #Binary data of input file
OUTPUT_FILENAME = "output.wav" #Output filename
