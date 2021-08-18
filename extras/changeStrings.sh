#!/bin/bash

if [ $# -ne 3 ]
then
  echo "Usage:  changeStrings.sh <inputFile> <oldString> <newString>"
  exit 0
else
  echo "Changing strings using sed with global option ('g') in a given file."
fi
 
fileName=$1
inputString=$2
outputString=$3

echo "running: \
sed -i -e \"s@${inputString}@${outputString}@g\" ${fileName}"
sed -i -e  "s@${inputString}@${outputString}@g" ${fileName}
