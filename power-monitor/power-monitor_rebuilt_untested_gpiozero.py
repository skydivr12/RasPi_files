#!/usr/bin/python3 -u

import subprocess
import time
from gpiozero import Button, LED

DEBUG = 0

# GPIO / BCM 17 - physical pin 11
PORT = 17

# Shutdown delay in seconds
# 14.5 minutes
SHUTDOWN_DELAY = 870 

# No. of seconds after ignition returns to cancel shutdown 
CANCEL_SHUTDOWN = 5

IGN_STATUS = 1
SHUTDOWN = 0
IGN_OFF_TIME = 0
IGN_OFF_LAST_SEEN = 0
NOW = 0

# set up button and LED objects
button = Button(PORT, pull_up=True)
led = LED(4)

while True:
	
	NOW = time.time()

	# Get the status of the ignition
	IGN_UP = button.is_pressed
 
	# Ignition switched off? then set shutdown flag and igntion off time  
	if not IGN_UP and not SHUTDOWN:
		SHUTDOWN = 1
		IGN_OFF_TIME = NOW 
		print("Ignition switched off, shutdown flag set!")
		led.on()

	# Increment this counter while ignition is off 
	if not IGN_UP and SHUTDOWN:
		IGN_OFF_LAST_SEEN = NOW 

	# if igntion is off check if shutdown delay time reached
	if (SHUTDOWN and not IGN_UP and ((NOW - IGN_OFF_TIME) > SHUTDOWN_DELAY)):
		print("Shutdown delay of", SHUTDOWN_DELAY, "seconds reached, shutting down!")
		try:
			STATUS = subprocess.check_output(["shutdown", "-h", "now", "--no-wall"])
		except subprocess.CalledProcessError as shutdowncmd:
			print("Shutdown failed with error code: ", shutdowncmd.returncode)
			break	

	# Cancel shutdown if power has been back for CANCEL_SHUTDOWN seconds
	if ((NOW - IGN_OFF_LAST_SEEN) >= CANCEL_SHUTDOWN ) and SHUTDOWN:
		print("Ignition has been back for : ", CANCEL_SHUTDOWN, " seconds - shutdown flag reset")
		SHUTDOWN = 0
		IGN_OFF_TIME = 0
		IGN_OFF_LAST_SEEN = 0
		led.off()

	if DEBUG:
		STATUS = button.is_pressed
		print("Pin status is: ", STATUS)
		print("IGN_UP is set to: ", IGN_UP)
		print("SHUTDOWN is set to: ", SHUTDOWN)
		if SHUTDOWN:
			print("Igntion off time is: ", IGN_OFF_TIME)
			print("Igntion off last seen time is: ", IGN_OFF_LAST_SEEN)
			print("Current time is : ", NOW)
			print("Elapsed time is : ", (NOW - IGN_OFF_TIME))

	time.sleep(1)

if DEBUG:
	print("Exiting")
led.off()
GPIO.cleanup()
