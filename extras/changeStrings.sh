#!/bin/bash

if [ $# -ne 3 ]
then
  echo "Usage: ./changeStrings.sh <inputFile> <oldString> <newString>"
  exit 0
else
  echo "Changing strings"
fi
 
fileName=$1
inputString=$2
outputStrring=$3

echo "running: sed -i -e \"s@${2}@${3}@g\" ${1}"
sed -i -e "s@${2}@${3}@g" ${1}
