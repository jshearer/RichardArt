from serial import Serial
import struct
import numpy
import time

class GrideyeComm(object):
	def __init__(self, port='/dev/ttyUSB0'):
		self.port = Serial(port=port,baudrate=115200)
		self.last = time.time()
		self.port.write('*')

	def shutdown(self):
		self.port.write('~')

	def read_packet(self):

		if (time.time()-self.last)>0.11:
			self.port.flushInput()

		while self.port.read() is not '*':
			continue

		two_stars = struct.unpack('cc',self.port.read(2))

		# if two_stars[0] == '*' and two_stars[1] == '*':
		# 	pass#print("Got three *'s")
		# else:
		# 	print("Falied to get three *'s. Got instead: %s"%str(two_stars))
		
		#Thermistor
		self.port.read(2)
		
		data = struct.unpack('H'*64,str(self.port.read(128)))

		data = numpy.fliplr(numpy.reshape(data,(8,8)))

		if numpy.amax(data)>200:
			# print("Got junk data!!!!! Here it is:\n%s"%str(data))
			return self.read_packet()

		#print("Got data! Wheee: \n%s"%str(data))

		self.last = time.time()
		return data

device = GrideyeComm()