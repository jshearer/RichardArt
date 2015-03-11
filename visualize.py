'''
Show all different interpolation methods for imshow
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import grideye_comm as geye

gport = geye.initialize_device()

# from the docs:

# If interpolation is None, default to rc image.interpolation. See also
# the filternorm and filterrad parameters. If interpolation is 'none', then
# no interpolation is performed on the Agg, ps and pdf backends. Other
# backends will fall back to 'nearest'.
#
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.imshow

#methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
#           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
#           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

grid = geye.read_packet(gport)
grid = np.subtract(np.min(grid),grid)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

hImage = ax.imshow(grid, interpolation='none')

while True:
	hImage.set_data(grid)
	plt.draw()
	plt.pause(0.02)
	grid = geye.read_packet(gport)
	grid = np.subtract(np.min(grid),grid)