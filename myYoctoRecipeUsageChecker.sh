#!/bin/bash
#Script that parses the dependency logs of the image to see 
# what all recipes in the provided parent folder are getting used in 
# the generated image
#Param 1: Parent folder containing the recipes eg: recipe-core
#Step 1: Generate the dependencies for your image bitbake -g <image name>
#Step 2: Run this script from the same folder containing the generated dependency files
path=$1
folders=()

for f in "$path"/*; do
	if [ -d "$f" ]; then
	   folder_name=$(basename "$f")
	   folders+=("$folder_name")
	fi
done

for f in "${folders[@]}"; do
	echo "Searching for $f recipe"
	count=$(grep -rn --include={pn-buildlist,task-depends.dot} "$f" /home/dravikumar/Repos/yocto_catapult/myRepo/riscv-yocto-catapult-11/build/ | wc -l )
	if [ $count -ne 0 ]; then
	   echo "$f -> $count"
	fi
done