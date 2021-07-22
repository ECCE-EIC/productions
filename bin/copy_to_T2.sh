#!/bin/bash
# Setup for MIT but can be changed
RBASE="gsiftp://se01.cmsaf.mit.edu:2811//cms/store/user/paus"
LBASE="file://"`pwd`

# Check that we have both command line arguments
if [ $# -lt 2 ]
then
    echo ""
    echo " Usage:  copy_to_T2.py  <outputPath>  <outputDest>"
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
source /cvmfs/grid.cern.ch/centos7-ui-test/etc/profile.d/setup-c7-ui-example.sh
# make sure we are authenticated
export X509_USER_PROXY="./x509up_u5407"
echo " Proxy: $X509_USER_PROXY"
voms-proxy-info -all
# double check the software is really there
echo "GFAL: "`which gfal-copy`

PWD=`pwd`
for f in `find $outputPath -type f | sed "s#$PWD##"`
do
  echo " Copy file: $f"
  echo " --> gfal-copy -f $LBASE/$f $RBASE/$f"
  gfal-copy -f $LBASE/$f $RBASE/$f
  rc=$?
done
