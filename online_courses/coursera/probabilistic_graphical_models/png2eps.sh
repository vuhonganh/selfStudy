#!/bin/sh

# File: png2eps.sh: convert every .png file to .eps if the latter does not exist

for FILE in ./images/*.png
do
    FILENAME=`basename $FILE .png`;
    [ ! -e ./images/${FILENAME}.eps ] && convert ./images/${FILENAME}.png eps3:./images/${FILENAME}.eps
done

# remove all png files in ./images folder
rm -rf ./images/*.png