import RPi.GPIO as gpio
import time

def write(pin, value):
	gpio.setmode(gpio.BCM)
	gpio.setup(pin,gpio.OUT)

	gpio.output(pin,value)