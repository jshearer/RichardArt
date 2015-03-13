import numpy as np
from grideye_comm import device
import time
#import gpio

class PresenceDetector(object):
	"""
	Presence is detected if any pixel is greater than threshold from its baseline value
	"""
	def __init__(self, true_cutoff=0.4, debounce_limit=2, trues_in_row=10):
		self.collect_baseline()

		self.debounce_limit = debounce_limit
		self.debounce_timer = time.time()
		self.last_value = False
		self.trues_in_a_row = trues_in_a_row

		self.num_trues = 0

		self.cutoff = true_cutoff

	def collect_avg(self,secs):
		avg = device.read_packet()
		samples = 1

		start = time.time()
		while (time.time()-start)<secs:
			avg = np.add(avg,device.read_packet())
			samples = samples + 1

		return np.divide(avg,samples)

	def collect_baseline(self,secs=5):
		raw_input("Point sensor at room, make sure it's stable, and that nobody is in the room.")		

		self.empty_baseline = self.collect_avg(secs)
		print("Empty baseline calculated: \n%s"%str(self.empty_baseline))

		raw_input("Point sensor at room, make sure it's stable, and that somebody is in the room.")

		self.occupied_baseline = self.collect_avg(secs*2)
		print("Occupied baseline calculated: \n%s"%str(self.occupied_baseline))

		self.threshold = np.abs(np.subtract(self.occupied_baseline,self.empty_baseline))

		print("Threshold calculated: \n%s"%str(self.threshold))

	def is_present(self, pkt=None):
		"""
		Reads a packet, and subtracts it from the baseline.
		Then checks to see if any pixels are higher than threshold.
		"""
		if not pkt:
			pkt = device.read_packet()
		diff_from_empty = np.abs(np.subtract(pkt,self.empty_baseline))
		any_gt_threshold = diff_from_empty>self.threshold

		#print("Recording: \n%s\nDifference from empty baseline: \n%s\nAny greater than threshold: \n%s"%(str(pkt),str(diff_from_empty),str(any_gt_threshold)))

		triggered_pixels = np.count_nonzero(any_gt_threshold)

		return float(triggered_pixels)/float(any_gt_threshold.size)>self.cutoff

	def debounce_present(self, pkt=None):
		"""
		If was false, true is immediatly accepted and sets timer
		If was true, true resets timer. False is accepted if timer is passed, else ignored.
		"""

		raw_presence = self.is_present(pkt)

		if raw_presence:
			self.num_trues = num_trues
			if self.num_trues<self.trues_in_row:
				raw_presence = False
		else:
			self.num_trues = 0

		if self.last_value:
			#If was true,
			if raw_presence:
				#true resets timer if it gets trues_in_a_row trues in a row
				self.num_trues = self.num_trues + 1
				self.debounce_timer = time.time()
				self.last_value = True
				return True
			else:
				#False is accepted if timer is passed, else ignored.
				if (time.time()-self.debounce_timer)>self.debounce_limit:
					self.last_value = False
					return False
				else:
					self.last_value = True
					return True
		else:
			#If was false
			if raw_presence:
				self.debounce_timer = time.time()
				self.last_value = True
				return True
			else:
				self.last_value = False
				return False



if __name__ == "__main__":
	detector = PresenceDetector()

	prev = False
	pin = 25

	#gpio.write(pin,prev)
	while True:
		present = detector.debounce_present()
		print("Presence detected!" if present else "Nobody in view.")
		if present is not prev:
			prev = present
			#gpio.write(pin,present)

	device.shutdown()