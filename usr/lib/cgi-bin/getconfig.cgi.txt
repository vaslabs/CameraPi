#!/bin/bash

lsusb | grep "Canon" | sed 's/://g' | awk '{print "usbreset /dev/bus/usb/" $2 "/" $4}'
echo `gphoto2 --list-config`
