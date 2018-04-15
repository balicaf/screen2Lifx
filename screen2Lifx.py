# Author: Frak Al-Nuaimy
# email: frakman@hotmail.com
#https://github.com/frakman1/lifxscreen2/issues/1

#my goal is to use that with Itunes visualizer
#toDo: change c.saturation and c.luminance to 1
#toDo: use music bpm to change lights accordingly (predict lag/having a lag time multiple of the beats?)
#toDo: change the decimate+mean to another system (edge detection filter+mediane of pixels grabbed?)
#toDo: In case of more than 85 ms transition(DURATION), add to the 2D pixels accumulator a time one (i.e. do an average in time too)


import lazylights
import time
from PIL import ImageGrab
#from PIL import Image
import os
from colour import Color
import sys
import math
import binascii

#//////////////////////////////////////////////////////////////////////////////////////////////////////////
# GLOBAL DEFINES
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
KELVIN           = 0    # 2000 to 8000, where 2000 is the warmest and 8000 is the coolest
DECIMATE         = 10   # skip every DECIMATE number of pixels to speed up calculation
DURATION         = 2000  # The time over which to change the colour of the lights in ms. Use 100 for faster transitions
BLACK_THRESHOLD  = 0.08 # Black Screen Detection Threshold
BLACK_BRIGHTNESS = 0.03 # Black Screen case's brightness setting
BLACK_KELVIN     = 5000 # Black Screen case's Kelvin setting
#//////////////////////////////////////////////////////////////////////////////////////////////////////////

#------------------------------------------------------------------------------------------------------------
# I use this to manually create a bulb using IP and MAC address.
def createBulb(ip, macString, port = 56700):
    return lazylights.Bulb(b'LIFXV2', binascii.unhexlify(macString.replace(':', '')), (ip,port))
#------------------------------------------------------------------------------------------------------------
#print("hi")

#Scan for bulbs
bulbs = lazylights.find_bulbs(expected_bulbs=1, timeout=5)
print (bulbs)
print (len(bulbs))

if (len(bulbs)==0):
    print ("No LIFX bulbs found. Make sure you're on the same WiFi network and try again")
    sys.exit(1)


#here is one bulb. I get this value from my router info page.
#myBulb1 = createBulb('10.10.10.2','D0:73:D5:31:EA:4E')  
#lazylights requires a 'set' of bulbs as input 
#bulbs1=[myBulb1]

#turn on
lazylights.set_power(bulbs, True)
time.sleep(1)

#turn off
#lazylights.set_power(bulbs, False)


#init counters/accumulators
red   = 0
green = 0
blue  = 0

# Crop a chunk of the screen out
# This is hacky and is currently screen and movie-size specific.

# TODO: clean this up and make it dynamically detect size and crop the black bits out automagically
#values form mbpr 13", 21:9 movie
left   = 0      # The x-offset of where your crop box starts
top    = 220    # The y-offset of where your crop box starts
width  = 2560   # The width  of crop box
height = 1000#1440    # The height of crop box
box    = (left, top, left+width, top+height)
# This is the Main loop
while True:

	# take a screenairshot
	image = ImageGrab.grab(bbox=box)
	c = Color(rgb=(1, 0, 0))
	lazylights.set_state(bulbs,c.hue*360,(c.saturation),c.luminance,KELVIN,(DURATION),False)
	#image.show()


        #This is the screenshot processing
	##begin1=  (time.clock())
	for y in range(0, height, DECIMATE):  #loop over the height
		for x in range(0, width, DECIMATE):  #loop over the width (half the width in this case)
			#print "\n coordinates   x:%d y:%d \n" % (x,y)
			color = image.getpixel((x, y))  #grab a pixel
			# calculate sum of each component (RGB)
			red = red + color[0]
			green = green + color[1]
			blue = blue + color[2]
			#print red + " " +  green + " " + blue
			#print "\n totals   red:%s green:%s blue:%s\n" % (red,green,blue)
			#print color
	

	# calculate the averages
	red = (( red / ( (height/DECIMATE) * (width/DECIMATE) ) ) )/255.0
	green = ((green / ( (height/DECIMATE) * (width/DECIMATE) ) ) )/255.0
	blue = ((blue / ( (height/DECIMATE) * (width/DECIMATE) ) ) )/255.0

	# generate a composite colour from these averages
	c = Color(rgb=(red, green, blue))
	##middle1=(time.clock())
	##print(middle1-begin1)
	##print (c)

	#print "\naverage1  red:%s green:%s blue:%s" % (red,green,blue)
	#print "average1   hue:%f saturation:%f luminance:%f" % (c.hue,c.saturation,c.luminance)
	#print "average1  (hex) "+  (c.hex)

	#//////////////////////////////////////////////////////////////////////////////////////////////////////////
	# PROGRAM LIFX BULBS 
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////
	if (c.red < BLACK_THRESHOLD)  and (c.green < BLACK_THRESHOLD) and (c.blue < BLACK_THRESHOLD):
		#print "black1 detected"
		lazylights.set_state(bulbs,0,0,BLACK_BRIGHTNESS,BLACK_KELVIN,(DURATION),False)
	else:
            
		lazylights.set_state(bulbs,c.hue*360,c.saturation,c.luminance,KELVIN,(DURATION),False)
		##print (c)
		#lazylights.set_state(bulbs,c.hue*360,(2+c.saturation)/3,1,KELVIN,(DURATION),False)#c.luminance
                
	#//////////////////////////////////////////////////////////////////////////////////////////////////////////
		


	##end1=time.clock()
	##print(end1-begin1)

	# Clear colour accumulators 	
	red   = 0
	green = 0
	blue  = 0





