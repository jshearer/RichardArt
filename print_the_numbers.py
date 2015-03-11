import grideye_comm as geye

gport = geye.initialize_device()

while True:
	grid = geye.read_packet(gport)