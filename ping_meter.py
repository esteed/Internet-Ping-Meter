#!/usr/bin/python

##
## Internet Ping Meter v1.0 - Eric Steed
##
## 01/03/17 - first version - EPS
##
import serial
import sys
import subprocess
import time
latency = 0
ping_targets="8.8.8.8 4.2.2.2 208.67.220.220"
#ping_targets="8.8.8.0 4.2.2.0 208.67.220.0"
retVal = 0
failLevel = 0
lastLEDStatus = ""

##
## Define array variable alertLevel[] and assign color codes to be sent to the NeoPixel.
## Based on the number of total ping failures, iterate the failLevel by one and
## send the appropriate color code.
##
clearLED = "ic"
alertLevel = []
alertLevel = ["h","g","f","e","d"]


##
## Open the serial port to talk to the NeoPixel.  Have to wait for it to initialize
## before we start sending signals
##
port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
time.sleep(3)

##
## Green = h
## Greenish Yellow = g
## Yellow = f
## Orange = e
## Red = d
## Black = i
##
## LED #'s
##
## 1-9 = 1-9
## 10 = a
## 11 = b
## 12 = c
##
## I'm using a NeoPixel ring with 12 LED Segments to indicate the average latency of
## multiple established servers on the internet.  This way I can tell visually if
## my internet connection is slow, or even down.
##
## To control the NeoPixel, I've assigned specific characters to indicate how many
## LED's to illuminate and what color.  When we tell the NeoPixel to illuminate a
## given number of LED's, we have to account for the fact that the last command
## string that was sent is persistent in that the LED stays lit even when the next
## command string comes in.  For example, if reading 1 determines that 4 LED's
## should be lit, then reading 2 calls for 3 LED's, you wouldn't be able to see that
## because all 4 LED's were still illuminated from the previous cycle.
##
## To account for this, we send an instruction to "illuminate" all 12 LED's with
## the color Black before sending the actual value desired.  This is done by
## assigning a value of 'ic' to the variable clearLED.  I've also added some logic
## at the end of the infinite while loop that says don't send any instructions
## unless there's been a change since the last one.  This gets rid of the blinking 
## effect that I was seeing on every update- rather annoying!
##

##
## I'm using the subprocess library for now unless I can get the native Python ping library
## to do it for me.  If stdout is null for a given target, return 0.
##
def doPing(host):
        import os,platform
        pingOutput = subprocess.Popen(["ping -c 1 -w 1 " + host + " | grep rtt | awk -F/ '{print $5}' | awk -F. '{print $1}'"], stdout=subprocess.PIPE, shell=True)
        (out, err) = pingOutput.communicate()
        if (out.rstrip('\n') == ''):
            return 0
        else:
            return out.rstrip('\n')

##
## Get average latency from all of the ping targets.  Had to cast the output of
## doPing() into an integer to be able to do math against it
##
while True:
        count=0
        for x in ping_targets.split():
            retVal = int(doPing(x))
            #print "latency = [{0}]".format(retVal)
            # print "type = [{0}]".format(type(retVal))
            if (retVal > 0):
                latency += retVal
                count+=1


        ##
        ## If count is zero, that means we were not able to successfully ping
        ## any of the targets and we should start incrementing the failure count.
        ## Furthermore, if we have been incrementing failLevel and we are now
        ## able to ping, reset the failLevel back to 0 at that time.
        ##
        if (count == 0):
            # Increase failure level
            #print "Failed to ping any host"
            failLevel += 1
            if (failLevel > 4):
                failLevel = 4

        else:
            latency=(latency/count)
            failLevel = 0

        ##
        ## Set LEDStatus to the appropriate value based on latency and failure count
        ##

        #print "Average Latency = [{0}]".format(latency)

        if (latency > 1) and (latency <= 10):
                #print "1-10"
                LEDStatus = clearLED + alertLevel[failLevel] + "1"

        elif (latency >= 11) and (latency <= 20):
                #print "11-20"
                LEDStatus = clearLED + alertLevel[failLevel] + "2"

        elif (latency >= 21) and (latency <= 30):
                #print "21-30"
                LEDStatus = clearLED + alertLevel[failLevel] + "3"

        elif (latency >= 31) and (latency <= 40):
                #print "31-40"
                LEDStatus = clearLED + alertLevel[failLevel] + "4"

        elif (latency >= 41) and (latency <= 50):
                #print "41-50"
                LEDStatus = clearLED + alertLevel[failLevel] + "5"

        elif (latency >= 51) and (latency <= 60):
                #print "51-60"
                LEDStatus = clearLED + alertLevel[failLevel] + "6"

        elif (latency >= 61) and (latency <= 70):
                #print "61-70"
                LEDStatus = clearLED + alertLevel[failLevel] + "7"

        elif (latency >= 71) and (latency <= 80):
                #print "71-80"
                LEDStatus = clearLED + alertLevel[failLevel] + "8"

        elif (latency >= 81) and (latency <= 90):
                #print "81-90"
                LEDStatus = clearLED + alertLevel[failLevel] + "9"

        elif (latency >= 91) and (latency <= 100):
                #print "91-100"
                LEDStatus = clearLED + alertLevel[failLevel] + "a"

        else:
                #print "latency greater than 101"
                LEDStatus = clearLED + alertLevel[failLevel] + "c"

		##		
		## If the latency is within a different range than the last iteration, send
		## the command to update the LED count on the NeoPixel.  Otherwise you get
		## a rather annoying blinking effect as the LED's are updated even if it's the
		## same measurement as the last time.
		##
        if (LEDStatus != lastLEDStatus):
            port.write(LEDStatus)
            lastLEDStatus = LEDStatus

        #time.sleep(5)
        #print LEDStatus
        latency = 0
