# Author: Frak Al-Nuaimy
# email: frakman@hotmail.com
#https://github.com/frakman1/lifxscreen2/issues/1

#my goal is to use that with Itunes visualizer
#toDo: change c.saturation and c.luminance to 1

#toDo: change the decimate+mean to another system (edge detection filter+mediane of pixels grabbed?)
#toDo: In case of more than 85 ms transition(DURATION), add to the 2D pixels accumulator a time one (i.e. do an average in time too)
#toDo: Use GPU for image processing

#toDo: use music bpm to change lights accordingly (predict lag/having a lag time multiple of the beats?)
#an idea is to grab iTunes notification (music title) and check on Mixxx the BPM
#toDo add on readme "download mixxx, settings, library, "export: write modified metadata from the library into file tag""
#if the curently played music on iTunes has bpm metadata, then the lifx will switch color accordingly

#todo add a more robust beat detection (i.e. call a shazam-like music recognition, then sync lights)

import lazylights
import time
from PIL import ImageGrab
#from PIL import Image
import os
from colour import Color
import sys
import math
import binascii
import threading
import random

#//////////////////////////////////////////////////////////////////////////////////////////////////////////
# GLOBAL DEFINES
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#from typing import Any, Union

KELVIN           = 0    # 2000 to 8000, where 2000 is the warmest and 8000 is the coolest
DECIMATE         = 9   # skip every DECIMATE number of pixels to speed up calculation
DURATION         = 3000  # The time over which to change the colour of the lights in ms. Use 100 for faster transitions
SLOW_DOWN        = 1 # integer to decrease stroboscopic effect

#Information and basic source from
#http://www.macosxautomation.com/applescript/features/scriptingbridge.html
from Foundation import *
from ScriptingBridge import *
import time


iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")

#print iTunes.currentTrack().name()
#print iTunes.currentTrack().artist()
#print iTunes.currentTrack().album()

outputString = iTunes.currentTrack().name()# + "[" + iTunes.currentTrack().album()

print outputString
bpmTrack=0#int
bpmTrack=iTunes.currentTrack().bpm()

#toDo check music lenght then do a counter (while music)do DURATION and then check the other music bpm
#------------------------------------------------------------------------------------------------------------
# I use this to manually create a bulb using IP and MAC address.
def createBulb(ip, macString, port = 56700):
    return lazylights.Bulb(b'LIFXV2', binascii.unhexlify(macString.replace(':', '')), (ip,port))
#------------------------------------------------------------------------------------------------------------

#Scan for 2 bulbs
bulbs = lazylights.find_bulbs(expected_bulbs=2, timeout=5)
#now bulbs can be called by their names
bulbs_by_name = {state.label.strip(" \x00"): state.bulb
                 for state in lazylights.get_state(bulbs)}
#set([
# Bulb(gateway_mac='LIFXV2', mac='\xd0s\xd51\xeaN', addr=('192.168.0.12', 56700)),
# Bulb(gateway_mac='LIFXV2', mac='\xd0s\xd5$mE'   , addr=('192.168.0.14', 56700))
# ])

if (len(bulbs)==0):
    print ("No LIFX bulbs found. Make sure you're on the same WiFi network and try again")
    sys.exit(1)

#turn on
lazylights.set_power(bulbs, True)
#do nothing during a tenth of a second
time.sleep(0.1)

#init counters/accumulators
red   = 0
green = 0
blue  = 0

#this is a thread to aquire BPMs from Itunes(given that you already calculated it on MIXXX)
def changeBPM():
	global beatLenght
	global DURATION
	threading.Timer(10.0, changeBPM).start()
	bpmTrack = iTunes.currentTrack().bpm()
	notPlaying=(iTunes.playerState() == 1800426352)
	# 1800426352#not playing
	# 1800426320#playing

	#if Itunes is not playing music
	if notPlaying:
		beatLenght = DURATION*SLOW_DOWN
		print("not playing")

	#if it's playing and there is an associated BPM
	elif bpmTrack != 0:
		msBPM = 60000.0 / (bpmTrack)  # type: Union[float, int]
		beatLenght = msBPM*SLOW_DOWN #avoid stroboscopic effect
		print "bpmTrack"
		print beatLenght

	#if it is playing but no BPMs
	else:
		beatLenght=DURATION
		print "bpm = 0"
		print beatLenght

changeBPM()
begin1=time.time()
#bpm1=beatLenght
bpm1=beatLenght+1 #to force it to a state bpm1 not equal to beatLenght
beginBPM=time.time()
countBeat=1
cReg = Color(rgb=(1, 1, 0))

while True:

	if bpm1!=beatLenght:
	 	#this is a different music
		beginBPM = time.time()
		countBeat=0
		bpm1 = beatLenght
		print "music changed"
	else:
	 	#this is the same music
		a=(beatLenght / 1000)-(time.time() - beginBPM)%(beatLenght/1000.0)
		a=max(0,a)
		time.sleep( a  )#should not sleep if 0
		countBeat += 1
	 	# %reminder //int division

	#if (time.time() - begin1) < DURATION/1000.0:
	#	time.sleep(DURATION/1000.0 - (time.time() - begin1) -0.665/1000)#0.665 there is a lag of less than a milisecond
		#lag is reduce to 0.1ms/beat, thus 50ms over a music
		#print time.time() - begin1
		#print"DURATION/1000.0"
		#print DURATION/1000.0

	# take a screenairshot
	#print(time.time()-begin1)


	##############################@
	# begin1=(time.time())
	# image = ImageGrab.grab(bbox=box)
	# c = Color(rgb=(1, 0, 0))
	# lazylights.set_state(bulbs,c.hue*360,(c.saturation),c.luminance,KELVIN,(DURATION),False)
	# #image.show()
	#
	#
	# #This is the screenshot processing
	#
	# for y in range(0, height, DECIMATE):  #loop over the height
	# 	for x in range(0, width, DECIMATE):  #loop over the width (half the width in this case)
	# 		#print "\n coordinates   x:%d y:%d \n" % (x,y)
	# 		color = image.getpixel((x, y))  #grab a pixel
	# 		# calculate sum of each component (RGB)
	# 		red = red + color[0]
	# 		green = green + color[1]
	# 		blue = blue + color[2]
	# 		#print red + " " +  green + " " + blue
	# 		#print "\n totals   red:%s green:%s blue:%s\n" % (red,green,blue)
	# 		#print color
	#
	#
	# # calculate the averages
	# red = (( red / ( (height/DECIMATE) * (width/DECIMATE) ) ) )/255.0
	# green = ((green / ( (height/DECIMATE) * (width/DECIMATE) ) ) )/255.0
	# blue = ((blue / ( (height/DECIMATE) * (width/DECIMATE) ) ) )/255.0
	#
	#
	# #be sure to be in range 0..1
	# if red>1:
	# 	red=1
	# if green>1:
	# 	green=1
	# if blue>1:
	# 	blue=1
	# # generate a composite colour from these averages
	# #c = Color(rgb=(red, green, blue))
	#
	#
	#
	####################################
	c = Color(rgb=(random.uniform(0.1, 1),random.uniform(0.1, 1),random.uniform(0, 0.5)))
	##middle1=(time.clock())
	##print(middle1-begin1)
	##print (c)

	#print "\naverage1  red:%s green:%s blue:%s" % (red,green,blue)
	#print "average1   hue:%f saturation:%f luminance:%f" % (c.hue,c.saturation,c.luminance)
	#print "average1  (hex) "+  (c.hex)

	#//////////////////////////////////////////////////////////////////////////////////////////////////////////
	# PROGRAM LIFX BULBS
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#	if (c.red < BLACK_THRESHOLD)  and (c.green < BLACK_THRESHOLD) and (c.blue < BLACK_THRESHOLD):
		#print "black1 detected"
#		lazylights.set_state(bulbs,0,0,BLACK_BRIGHTNESS,BLACK_KELVIN,(DURATION),False)
#	else:
#set_light_state_raw

	if countBeat%2==0:
		lazylights.set_state([bulbs_by_name['LIFX 246D45']], cReg.hue * 360, cReg.saturation, 0.3, KELVIN, 0, False)

	else:
		cReg = c
		lazylights.set_state([bulbs_by_name['LIFX 31ea4e']],c.hue*360,c.saturation,0.3,KELVIN,0,False)
		#bulbs_by_name 'LIFX 31ea4e' 'LIFX 246D45'
		##print (c)
		#lazylights.set_state(bulbs,c.hue*360,(2+c.saturation)/3,1,KELVIN,(DURATION),False)#c.luminance

	#//////////////////////////////////////////////////////////////////////////////////////////////////////////





	# Clear colour accumulators
	red   = 0
	green = 0
	blue  = 0







