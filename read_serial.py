from serial import Serial
import struct
import numpy

port = Serial(port='/dev/ttyUSB0',baudrate=115200)

def read_packet():
	#Thermistor
	port.read(2)
	
	data = struct.unpack('h'*64,str(port.read(128)))

	data = numpy.fliplr(numpy.reshape(data,(8,8)))

	print("Got data! Wheee: \n%s"%str(data))


#Initialize the device with '*'
port.write('*')

while True:
	while port.read() is not '*':
		print("Got something, not asterisk, continuing.")
		continue
	port.read(2)
	#At start of data

	print("Reached Asterisk. Now at start of data.")

	read_packet()


