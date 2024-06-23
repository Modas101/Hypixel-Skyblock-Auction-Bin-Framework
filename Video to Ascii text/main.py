import time, os
import pyperclip

if __name__ == '__main__':
	f = open('play.txt', 'r')
	frame_raw = f.read()
	frame_raw = frame_raw.replace('.', ' ')
	f.close()
	frames = frame_raw.split('SPLIT')
	#os.system('mplayer test.mp4 &')

	stra = "{"
	for i in range(len(frames)):
		stra += fr"{repr(frames[i])},"

	stra += "}"

	pyperclip.copy(stra)

	init_time = time.time()
	if False:
		while time.time() <= init_time + 218:

			os.system('cls')
			print(frames[int((time.time()-init_time)*10)])
			time.sleep(0.016)

