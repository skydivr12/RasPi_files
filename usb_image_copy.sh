#!/bin/bash

# Script to move over image files from a USB key
# when it is inserted into the system.

# Should be called from a udev rule like:
# ACTION=="add",KERNEL=="sd*", SUBSYSTEMS=="usb", ATTRS{product}=="Mass Storage", RUN+="/root/bin/usbhook %k"

# Copyright 2009 Jason Antman.  
# 

# CONFIGURATION
DEBUG=1 # Set to 1 for debugging output
DEST="/home/foo/" # Destination for files


DEVICE="$1" # The device name
LOGFACILITY="kernel.info" # For debugging output


if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook called with arguments: "$DEVICE"; fi

sleep 5 # Delay 5 seconds to wait for mount

mount | grep "$DEVICE"
FOO="$?"

if [ $FOO == 0 ]; then
    if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook device mounted: "$DEVICE"; fi
else
    if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook device NOT mounted: "$DEVICE" - exiting; fi
    exit 0
fi

BAR=$(mount | grep "$DEVICE" | awk '{ print $3 }')

if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook checking for image files in: "$BAR"; fi

# Copy only image files from all subdirectories (case-insensitive)
find "$BAR" -type f -iregex '.*\.\(jpg\|jpeg\|png\|gif\|bmp\)' -exec cp -R {} "$DEST" \;

if [ $? == 0 ]; then
    if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook image files copied successfully from: "$BAR"; fi
else
    if [ ${DEBUG:=0} == 1 ]; then logger "$LOGFACILITY" usbhook no image files found in: "$BAR"; fi
fi
