#!/bin/sh
# ghoto_web.cgi
# Shell script for remote control of digital cameras
#
# Copyright (C) 2005 Helmut Dersch  der@fh-furtwangen.de
# Portions of this script are derived from work copyright 
# Frank Pilhofer fp@informatik.uni-frankfurt.de
#
# This program is free software; the author(s) 
# give unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.
#

# This script is used for remote control of
# digital cameras. It interfaces to gphoto2
# (http://www.gphoto.org) on the server side
# and via HTML pages and WWW to the client.
# It uses plain Shell and Unix commands and
# should run on minimal installations like
# embedded Linux. It has been testet on
# the Linksys NSLU2 server running unslung-standard 3-16
# (http://www.nslu2-linux.org).


# The following lines may need to be edited
# for other systems
export PATH=$PATH:/usr/bin:/opt/bin:/opt/gphoto/bin/
#export LD_LIBRARY_PATH=/opt/gphoto/lib


# Read, process and evaluate CGI parameters
# derived from "proccgi.sh" by 
# Frank Pilhofer fp@informatik.uni-frankfurt.de

_F_QUERY_STRING=`dd count=$CONTENT_LENGTH bs=1 2> /dev/null`"&"
_F_QUERY_STRING="`echo $_F_QUERY_STRING | sed 'sa%2Fa/ag'`"
while [ "$_F_QUERY_STRING" != "" -a "$_F_QUERY_STRING" != "&" ] ; do
        _F_VARDEF=`echo $_F_QUERY_STRING | cut -d \& -f 1`
        _F_QUERY_STRING=`echo $_F_QUERY_STRING | cut -d \& -f 2-`
        _F_VAR=`echo $_F_VARDEF | cut -d = -f 1`
        _F_VAL=`echo "$_F_VARDEF""=" | cut -d = -f 2`

        eval `echo "FORM_$_F_VAR"="'"$_F_VAL"'"`
done

# Now execute command in $FORM_sub

if   test $FORM_sub = "Preview"; then
     rm -f preview.jpg
     gphoto2 --capture-preview --filename preview.jpg 2> /dev/null    
     sleep 5 
     echo "Content-type: text/html"
     echo ""
     echo "<meta http-equiv=\"refresh\" content=\"0; URL=../index.html#panel\">"

elif test $FORM_sub = "Capture"; then
     gphoto2 --capture-image 2> /dev/null
     echo "Content-type: text/html"
     echo ""
     echo "<meta http-equiv=\"refresh\" content=\"0; URL=index.html#panel\">"

elif test $FORM_sub = "HDR"; then
     echo "Content-type: text/html"
     echo ""
     echo "<HTML><BODY>"
     echo "The command being sent to your camera is <p>"
     echo "sudo takehdr --aperture 8 --outtype jpeg --cr2path /home/andyboutte/images/cr2 --tiffpath /home/andyboutte/images/tiff --hdrpath /home/andyboutte/images/hdr --jpgpath /home/andyboutte/images/jpg"
     echo "<p>"
     echo "Response:<p>"
     echo "<pre>"
     sudo takehdr --aperture 8 --outtype jpeg --cr2path /home/andyboutte/images/cr2 --tiffpath /home/andyboutte/images/tiff --hdrpath /home/andyboutte/images/hdr --jpgpath /home/andyboutte/images/jpg
     echo "</pre>"
     echo "<p>"
     echo "To return to Remote Control press Back in your Browser"
     echo "</BODY></HTML>"
     echo ""

elif test $FORM_sub = "TimeLapse"; then
     echo "Content-type: text/html"
     echo ""
     echo "<HTML><BODY>"
     echo "The command being sent to your camera is <p>"
     echo "sudo takehdr --aperture 8 --outtype jpeg --cr2path /home/andyboutte/images/cr2 --tiffpath /home/andyboutte/images/tiff --hdrpath /home/andyboutte/images/hdr --jpgpath /home/andyboutte/images/jpg"
     echo "<p>"
     echo "Response:<p>"
     echo "<pre>"
sudo taketimelapse --aperture 8 --startshutterspeed $FORM_start --endshutterspeed $FORM_end --videoduration $FORM_videoduration --timelapseduration $FORM_timelapseduration --jpgpath /home/andyboutte/images/timelapse 
     echo "</pre>"
     echo "<p>"
     echo "To return to Remote Control press Back in your Browser"
     echo "</BODY></HTML>"
     echo ""

elif test $FORM_sub = "Execute"; then
     echo "Content-type: text/html"
     echo ""
     echo "<HTML><BODY>"
     echo "The command being sent to your camera is <p>"
     echo "gphoto2 " $FORM_cmd
     echo "<p>"
     echo "Response:<p>"
     echo "<pre>"
     gphoto2 $FORM_cmd
     echo "</pre>"
     echo "<p>"
     echo "To return to Remote Control press Back in your Browser"
     echo "</BODY></HTML>"
     echo ""

elif test $FORM_sub = "getconfig"; then
     echo "Content-type: text/html"
     echo ""
     echo "<HTML><BODY>"
     echo "<p>"
	 lsusb | grep "Canon" | sed 's/://g' | awk '{print "usbreset /dev/bus/usb/" $2 "/" $4}'
	 echo `gphoto2 --list-config`
     echo "</BODY></HTML>"
     echo ""

elif test $FORM_sub = "Load"; then
     echo "Content-type: application/gzip"
     echo ""
     gphoto2 --quiet --get-file $FORM_num --folder $FORM_dir --stdout  2> /dev/null
fi
