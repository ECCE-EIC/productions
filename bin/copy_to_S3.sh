#!/bin/bash

RBASE="S3/eictest/ECCE/MC"   # make sure to use 'S3' as the config alias below
LBASE=`pwd`

# Check that we have both command line arguments
if [ $# -lt 2 ]
then
  echo ""
  echo " Usage:  copy_to_S3.sh  <outputPath>  <outputDest>"
  echo ""
  echo "  <outputPath>      local relative directory prefixed with $LBASE"
  echo "  <outputDest>      remote directory prefixed with $RBASE"
  echo ""
  exit 1
fi

outputPath=$1
outputDest=$2

echo " Instruction for copy_to_T2.sh: $LBASE/$outputPath --> $RBASE/$outputDest"
echo ""

# load the proper software environment
export PATH="${PATH}:/cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/utils/bin"
echo " MINIO: "`which mcs3`

# make sure we are authenticated
mcs3 config host add S3 https://dtn01.sdcc.bnl.gov:9000/ username secret 

PWD=`pwd`
for f in `find $outputPath -type f | sed "s#$PWD##"`
do

  rdir=`dirname $RBASE/$f`

  echo " Make directory (bucket): $rdir"
  echo " -->\
  mcs3 mb -p $rdir"
  mcs3 mb -p $rdir

  echo " Copy file: $f"
  echo " -->\
  mcs3 cp $LBASE/$f $RBASE/$f"
  mcs3 cp $LBASE/$f $RBASE/$f

done
