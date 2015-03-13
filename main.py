from detect_presence import PresenceDetector
import gpio
import time
import subprocess
import os

detector = PresenceDetector()

play_audio = False
switch_on = False
play_video = True

switch_out_pin = 25
record_input_pin = 24

#True for high, False for low
record_switch_pressed_state = True

is_recording = False

record_process = None
video_process = None
audio_process = None

video_file = 'IMG_0812.MOV'
audio_file = 'IMG_0813.mp3'

x_server = subprocess.popen('X')

new_env = dict(os.environ, DISPLAY=":0")

while True:
	######   Handle Detection   ######
	if detector.is_present():
		play_audio = True
		switch_on = True
	else:
		play_audio = False
		switch_on = False
	###### ###### ###### ###### ######


	###### Handle record button ######
	record_pin_state = gpio.read(record_input_pin)

	if record_pin_state == record_switch_pressed_state:
		if not is_recording:
			record_process = subprocess.popen(['arecord',str(time.time())+'.wav'])
			is_recording = True
	else:
		if is_recording:
			record_process.terminate()
			is_recording = False
	###### ###### ###### ###### ######

	###### Handle Audio Process ######
	if play_audio:
		if audio_process:
			if audio_process.poll() != None:
				#Process finished
				audio_process = subprocess.popen(['omxplayer', audio_file], env=new_env)
		else:
			audio_process = subprocess.popen(['omxplayer', audio_file], env=new_env)
	else:
		if audio_process:
			audio_process.terminate()
	###### ###### ###### ###### ######

	###### Handle Video Process ######
	if play_video:
		if video_process:
			if video_process.poll() != None:
				#Process finished
				video_process = subprocess.popen(['omxplayer', video_file], env=new_env)
		else:
			video_process = subprocess.popen(['omxplayer', video_file], env=new_env)
	else:
		if video_process:
			video_process.terminate()
	###### ###### ###### ###### ######

	###### Handle Switch Output ######
	gpio.write(switch_out_pin,switch_on)
	###### ###### ###### ###### ###### 