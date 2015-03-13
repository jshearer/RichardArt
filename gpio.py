import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

def write(pin, value):
	gpio.setup(pin,gpio.OUT)

	gpio.output(pin,value)

def read(pin):
	gpio.setup(pin, gpio.IN, gpio.PUD_UP)
	return gpio.input(pin)
