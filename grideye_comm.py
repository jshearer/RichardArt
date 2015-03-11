from serial import Serial
import struct
import numpy

def read_packet(port):

	while port.read() is not '*':
		continue

	two_stars = struct.unpack('cc',port.read(2))

	if two_stars[0] == '*' and two_stars[1] == '*':
		print("Got three *'s")
	else:
		print("Falied to get three *'s. Got instead: %s"%str(two_stars))
	
	#Thermistor
	port.read(2)
	
	data = struct.unpack('h'*64,str(port.read(128)))

	data = numpy.fliplr(numpy.reshape(data,(8,8)))

	print("Got data! Wheee: \n%s"%str(data))

	return data

def initialize_device(port='/dev/ttyUSB0'):
	port = Serial(port=port,baudrate=115200)
	#Initialize the device with '*'
	port.write('*')

	return port

