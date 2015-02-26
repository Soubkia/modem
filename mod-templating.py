#modulator class
class Config:
	def __init__():
		self.START_TIME = time.time()+1 						# Timekeeper (waits 1 second to start)
		self.HIGH_NOTE = 440 									# Note when 1
		self.LOW_NOTE = 220 									# Note when 0
		self.BITRATE = 0.5 										# Bits per second
		self.BPF = 1 											# Bits per frame
		self.RATE = 44100 										# Specifies the desired sample rate (in Hz)
		self.INPUT_FILENAME = "input.txt" 						# Input filename
		a = open(INPUT_FILENAME, 'r') 							# TODO: I think this is just getting the ascii binary not the full bytedata of the text file
		c = a.read()
		self.INPUT_FILE_BIN = bin(int(binascii.hexlify(c), 16)) # Binary data of input file
		self.OUTPUT_FILENAME = "output.wav" 					# Output filename



class Modulator:
	def __init__(self, fileName):
		self.config = GLOBAL
		self.fileName = fileName
		self.stream = None




