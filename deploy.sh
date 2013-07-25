#!/bin/bash
#Deploy Script
#7/23/2013
#Andy Boutte

#Copies new or modified files into place on CameraPi

BRANCH=`git branch | awk {'print $2'}`
FILES=`git ls-tree -r --name-only $BRANCH`

for f in $FILES
do
	if [ "$f" = "deploy.sh" ]
	then
		echo "Skipping deploy script..."
	elif [ "$f" = "README.md" ]
	then
		echo "Skipping readme..."
	else		
		cp -uv $f /$f	
	fi
done

echo "Finished processing all files..."
