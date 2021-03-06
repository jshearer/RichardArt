from detect_presence import PresenceDetector
import gpio
import time
import subprocess
import os
import signal

play_audio = False
switch_on = False
play_video = True

switch_out_pin = 25
record_input_pin = 24

#True for high, False for low
record_switch_pressed_state = 0

is_recording = False

record_process = None
video_process = None
audio_process = None

video_file = 'IMG_0812_VFLIP.MOV'
audio_file = 'IMG_0813.mp3'

x_server = subprocess.Popen('X')

new_env = dict(os.environ, DISPLAY=":0")

while True:

	###### Handle record button ######
	record_pin_state = gpio.read(record_input_pin)

	if record_pin_state == record_switch_pressed_state:
		play_audio = True
		switch_on = True
	else:
		play_audio = False
		switch_on = False
	###### ###### ###### ###### ######

	###### Handle Audio Process ######
	if play_audio:
		if audio_process:
			if audio_process.poll() != None:
				#Process finished

				audio_process = subprocess.Popen(['omxplayer', audio_file], stdin=subprocess.PIPE)
				print("Restarting the audio.")
		else:
			audio_process = subprocess.Popen(['omxplayer', audio_file], stdin=subprocess.PIPE)
			print("Starting audio.")
	else:
		if audio_process:
			audio_process.stdin.write('q')
			audio_process.stdin.flush()
			audio_process.terminate()
			audio_process = None
			print("Killing audio.")
	###### ###### ###### ###### ######

	###### Handle Video Process ######
	if play_video:
		if video_process:
			if video_process.poll() != None:
				#Process finished
				video_process = subprocess.Popen(['omxplayer', video_file], env=new_env)
				print("Restarting video.")
		else:
			video_process = subprocess.Popen(['omxplayer', video_file], env=new_env)
			print("Starting video.")
	else:
		if video_process:
			video_process.stdin.write('q')
			video_process.stdin.flush()
			video_process.terminate()
			video_process = None
			print("Terminating video.")
	###### ###### ###### ###### ######

	###### Handle Switch Output ######
	gpio.write(switch_out_pin,switch_on)
	###### ###### ###### ###### ###### 