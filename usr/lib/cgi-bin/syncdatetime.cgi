#!/bin/bash

lsusb | grep "Canon" | sed 's/://g' | awk '{print "usbreset /dev/bus/usb/" $2 "/" $4}'
sudo /usr/local/bin/syncdatetime
