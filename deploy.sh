#!/bin/bash
#Deploy Script
#7/23/2013
#Andy Boutte

#Copies new or modified files into place on CameraPi

BRANCH=`git branch | awk {'print $2'}`
FILES=`git ls-tree -r --name-only $BRANCH`

for f in $FILES
do
	#echo "Processing $f file..."
	cp -uv $f /$f
done

echo "Finished processing all files..."
