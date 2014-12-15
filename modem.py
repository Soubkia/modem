#modem.py
import binascii
import pyaudio
import wave
import sys

WAVE_OUTPUT_FILENAME = "test.wav"

a = open('test.txt', 'r')
c = a.read()
b = bin(int(binascii.hexlify(c), 16))

sample_stream = []
high_note = (b'\xFF'*100 + b'\0'*100) * 50
low_note = (b'\xFF'*50 + b'\0'*50) * 100
for bit in b[2:]:
    if bit == '1':
        sample_stream.extend(high_note)
    else:
        sample_stream.extend(low_note)

sample_buffer = b''.join(sample_stream)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True)
stream.write(sample_buffer)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(sample_stream))
wf.close()