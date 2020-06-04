# ===============================================
# 					LCARS Keyboard
# 	Author: @ZooL_Smith
#
# using "keyboard" and "mouse" by BoppreH
# 		https://pypi.org/project/keyboard/
# 		https://pypi.org/project/mouse/
#
# and "simpleaudio" by Joe Hamilton
#		https://pypi.org/project/simpleaudio/
# ===============================================


import keyboard
import mouse
import simpleaudio
import time
import glob
import random
import os.path

debug = True
scrollDelay = 0.075
enabled = True

prefixFolder = "./sounds/"
def getSounds(folder):
	return glob.glob(prefixFolder+folder+"/*.wav")

soundsDefault = 		getSounds("default")
soundsEnter = 			getSounds("enter")
soundsEscape = 			getSounds("escape")
soundsTab = 			getSounds("tab")
soundsDn = 				getSounds("down")
soundsUp = 				getSounds("up")
soundsLeft = 			getSounds("left")
soundsRight = 			getSounds("right")
soundsSpace = 			getSounds("space")
soundsBack = 			getSounds("back")
soundsCtrl = 			getSounds("ctrl")
soundsShift = 			getSounds("shift")
soundsAlt = 			getSounds("alt")
soundsLogo = 			getSounds("logo")
soundsNumbers = 		getSounds("num")
soundsFunction = 		getSounds("func")
soundsGoto = 			getSounds("goto")
soundsSpecialFunction = getSounds("specialfunc")

soundsWheelDn = 		getSounds("wheeldown")
soundsWheelUp = 		getSounds("wheelup")
soundsClickLeft = 		getSounds("clickleft")
soundsClickRight = 		getSounds("clickright")
soundsClickOther = 		getSounds("clickother")

soundsEnabled = 		getSounds("enabled")
soundsDisabled = 		getSounds("disabled")


global currentSound
currentSound = simpleaudio.WaveObject.from_wave_file(random.choice(soundsEnabled)).play()

def getSndMouse(key):
	if(not enabled): return
	if(isinstance(key, mouse.MoveEvent)):
		return
	if(isinstance(key, mouse.ButtonEvent) and key.event_type == 'up'):
		return
		
	if(isinstance(key, mouse.ButtonEvent)):
		if(key.button == 'left'):		playFile(getRandom(soundsClickLeft))
		elif(key.button == 'right'):	playFile(getRandom(soundsClickRight))
		else:							playFile(getRandom(soundsClickOther))
		
	elif(isinstance(key, mouse.WheelEvent)):
		if(key.delta>0.20):				playFileScrollDelay(getRandom(soundsWheelUp),key.time)
		elif(key.delta<-0.20):			playFileScrollDelay(getRandom(soundsWheelDn),key.time)
		
	if(debug): print(key)
	
lastScroll = 0
heldArray = []

def releaseKeyboard(key):
	if(not enabled): return
	if(heldArray.count(key.scan_code)>0):
		heldArray.remove(key.scan_code)

def pressKeyboard(key):
	if(debug): print(("{M} " if not enabled else "") + str(key.scan_code),"-","["+key.name+"]")
	if(not enabled): return
	getSndKeyboard(key)
	if(heldArray.count(key.scan_code)<1):
		heldArray.append(key.scan_code)

def getSndKeyboard(key):
	global currentSound
	currentSound.stop()
	sc = key.scan_code
	
	if(sc == 1):					playFile(getRandom(soundsEscape))	# Escape key
	elif(key.is_keypad and ((sc>78 and sc<82)or(sc>74 and sc<78)or(sc>70 and sc<74))):	playFile(getRandom(soundsNumbers))	# Numpad Numbers
	elif(sc == 73 or sc == 72):		playFile(getRandom(soundsUp))				# Up and PGUP
	elif(sc == 81 or sc == 80):		playFile(getRandom(soundsDn))				# Down and PGDN
	elif(sc == 75):					playFile(getRandom(soundsLeft))				# Left arrow
	elif(sc == 77):					playFile(getRandom(soundsRight))			# Right arrow
	elif(sc == 28):					playFile(getRandom(soundsEnter))			# Enter keys
	elif(sc == 57):					playFile(getRandom(soundsSpace))			# Spacebar
	elif(sc == 15):					playFile(getRandom(soundsTab))				# Tab
	elif(sc == 71 or sc == 79):		playFile(getRandom(soundsGoto))				# Home and End
	elif(sc == 14 or sc == 83):		playFile(getRandom(soundsBack))				# Backspace and del
	elif(sc>1 and sc<14):			playFile(getRandom(soundsNumbers))			# Number keys
	elif(sc == 29):					playFileNoHold(getRandom(soundsCtrl), sc)	# CTRLs
	elif(sc == 56 or sc == 541):	playFileNoHold(getRandom(soundsAlt), sc)	# ALT and ALTGR
	elif(sc == 42 or sc == 54):		playFileNoHold(getRandom(soundsShift), sc)	# Shifts
	elif(sc == 91 or sc == 92):		playFileNoHold(getRandom(soundsLogo), sc)	# Window keys
	elif(sc>58 and sc<69)or(sc>86 and sc<89):					playFileNoHold(getRandom(soundsFunction), sc)	# Function keys
	elif((sc==55 and not key.is_keypad) or sc==69 or sc==70 or sc==58):	playFileNoHold(getRandom(soundsSpecialFunction), sc) # Special keys, locks
	else:							playFile(0)		# Unknown or default keys
	

def getRandom(arr):
	if(len(arr)<1):
		return 0
	else:
		return random.choice(arr)

def playFileScrollDelay(fileName, t):
	global lastScroll
	global scrollDelay
	if(t>lastScroll+scrollDelay):
		playFile(fileName)
		lastScroll = t

def playFileNoHold(fileName, sc):
	if(heldArray.count(sc)<1):
		playFile(fileName)

def playFile(fileName):
	if(fileName == 0):
		if(len(soundsDefault)>0):
			currentSound = simpleaudio.WaveObject.from_wave_file(random.choice(soundsDefault)).play()
		else:
			print("NO DEFAULT FILES!")
	else:
		currentSound = simpleaudio.WaveObject.from_wave_file(fileName).play()
	
def toggleEnabled():
	global enabled
	enabled = not enabled
	print("LCARSKeyboard is now", "enabled" if enabled else "disabled" )
	if(enabled):
		playFile(getRandom(soundsEnabled))
	else:
		playFile(getRandom(soundsDisabled))

mouse.hook(getSndMouse)
keyboard.on_press(pressKeyboard)
keyboard.on_release(releaseKeyboard)
keyboard.add_word_listener("lcars", toggleEnabled, triggers=['backspace'], match_suffix=False, timeout=10)

while True:
	time.sleep(1000)