'''
Show all different interpolation methods for imshow
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from grideye_comm import device

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

grid = device.read_packet().astype(float)

# grid = np.subtract(grid,np.min(grid))
# grid = np.divide(grid,np.max(grid))
# grid = np.multiply(200,grid)

print(grid)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

hImage = ax.imshow(grid, interpolation='lanczos', vmin=0, vmax=200)

avg_count = 2
avg_current = 0

avg = grid

while True:
	if avg_current>=avg_count:
		avg_current = 0
		avg = np.divide(avg,avg_count)
		hImage.set_data(avg)		
		plt.draw()
		plt.pause(0.02)

	grid = device.read_packet().astype(float)
	
	# grid = np.subtract(grid,np.min(grid))
	# grid = np.divide(grid,np.max(grid))
	# grid = np.multiply(200,grid)

	avg = np.add(avg,grid)
	avg_current += 1

device.shutdown()