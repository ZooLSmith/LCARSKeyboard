# ===============================================
# 					LCARS Keyboard
# 	Author: @ZooL_Smith
#
#
# using "keyboard" and "mouse" by BoppreH
# 		https://pypi.org/project/keyboard/
# 		https://pypi.org/project/mouse/
# ===============================================







import keyboard
import mouse
import simpleaudio
import time
import glob
import random
import os.path

debug = False

prefixFolder = "./sounds/"
def getSounds(folder):
	return glob.glob(prefixFolder+folder+"/*.wav")

soundsDefault = getSounds("default")
soundsEnter = getSounds("enter")
soundsEscape = getSounds("escape")
soundsTab = getSounds("tab")
soundsDn = getSounds("down")
soundsUp = getSounds("up")
soundsLeft = getSounds("left")
soundsRight = getSounds("right")
soundsSpace = getSounds("space")
soundsReturn = getSounds("return")
soundsCtrl = getSounds("ctrl")
soundsShift = getSounds("shift")
soundsWheelDn = getSounds("wheeldown")
soundsWheelUp = getSounds("wheelup")
soundsClickLeft = getSounds("clickleft")
soundsClickRight = getSounds("clickright")
soundsClickOther = getSounds("space")


global currentSound
currentSound = simpleaudio.WaveObject.from_wave_file(soundsDefault[0]).play()

def getSndMouse(key):
	if(isinstance(key, mouse.MoveEvent)):
		return
	if(isinstance(key, mouse.ButtonEvent) and key.event_type == 'up'):
		return
		
	if(isinstance(key, mouse.ButtonEvent)):
		if(key.button == 'left'):		playFile(getRandom(soundsClickLeft))
		elif(key.button == 'right'):	playFile(getRandom(soundsClickRight))
		else:							playFile(getRandom(soundsClickOther))
		
	elif(isinstance(key, mouse.WheelEvent)):
		if(key.delta>0.99):				playFile(getRandom(soundsWheelUp))
		elif(key.delta<-0.99):			playFile(getRandom(soundsWheelDn))
		
		
	print(key)
	
heldArray = []

def releaseKeyboard(key):
	if(heldArray.count(key.scan_code)>0):
		heldArray.remove(key.scan_code)
	
def pressKeyboard(key):
	getSndKeyboard(key)
	if(heldArray.count(key.scan_code)<1):
		heldArray.append(key.scan_code)

def getSndKeyboard(key):
	global currentSound
	currentSound.stop()
	sc = key.scan_code
	
	if(sc == 1):					playFile(getRandom(soundsEscape))
	elif(sc == 73 or sc == 72):		playFile(getRandom(soundsUp))
	elif(sc == 81 or sc == 80):		playFile(getRandom(soundsDn))
	elif(sc == 75):					playFile(getRandom(soundsLeft))
	elif(sc == 77):					playFile(getRandom(soundsRight))
	elif(sc == 28):					playFile(getRandom(soundsEnter))
	elif(sc == 57):					playFile(getRandom(soundsSpace))
	elif(sc == 15):					playFile(getRandom(soundsTab))
	elif(sc == 14):					playFile(getRandom(soundsReturn))
	elif(sc == 29):					playFileNoHold(getRandom(soundsCtrl), sc)
	elif(sc == 42 or sc == 54):		playFileNoHold(getRandom(soundsShift), sc)
	else:							playFile(0)
	
	if(debug): print(key.scan_code)
	

def getRandom(arr):
	if(len(arr)<1):
		return 0
	else:
		return random.choice(arr)
	
def playFileNoHold(fileName, sc):
	if(heldArray.count(sc)<1):
		playFile(fileName)

def playFile(fileName):
	if(fileName == 0):
		if(len(soundsDefault)>0):
			currentSound = simpleaudio.WaveObject.from_wave_file(random.choice(soundsDefault)).play()
		else:
			print("NO DEFAULT FILE!")
	else:
		currentSound = simpleaudio.WaveObject.from_wave_file(fileName).play()
	



mouse.hook(getSndMouse)
keyboard.on_press(pressKeyboard)
keyboard.on_release(releaseKeyboard)

while True:
	time.sleep(1)