from serial import Serial
import struct
import numpy

def read_packet(port):
	#Thermistor
	port.read(2)
	
	data = struct.unpack('h'*64,str(port.read(128)))

	data = numpy.fliplr(numpy.reshape(data,(8,8)))

	print("Got data! Wheee: \n%s"%str(data))

def initialize_device(port='/dev/ttyUSB0'):
	port = Serial(port=port,baudrate=115200)
	#Initialize the device with '*'
	port.write('*')

	while port.read() is not '*':
		print("Got something, not asterisk, continuing.")
		continue
	port.read(2)
	#At start of data

	print("Reached Asterisk. Now at start of data.")

	return port

