#!/bin/bash
#
# Download the input file to local /tmp with locking of the worker node to avoid jobs stepping on
# each other. Default using S3 should always work, but if a root:// file is given it should also
# work, as long as your ticket is valid and has permission.
#
# Example for S3:
#   FULL_FILE="S3://eictest/ECCE/ProductionInputFiles/SIDIS/pythia6/ep_18x100/ep_noradcor.18x100lowq_run001.root"
#
# Example for xrootd:
#   FULL_FILE="root://xrootd.cmsaf.mit.edu//store/user/paus/ecce/ep_noradcor.18x100lowq_run001.root"
#
echo "==========================="
echo ""
echo " Downloading: $@"
echo " on host: "`hostname`
echo ""
env | sort -u
echo ""
echo "==========================="

FULL_FILE="$1"
FILE=`basename $FULL_FILE`
TARGET="/tmp/$FILE"
if [[ $FULL_FILE == "root://"* ]]
then
  printf " Found an xrootd file: $FULL_FILE\n Use xrdcp.\n"
  TOOL="xrdcp"
  SOURCE=$FULL_FILE
  source /cvmfs/grid.cern.ch/centos7-ui-test/etc/profile.d/setup-c7-ui-example.sh
  echo " XRDCP: "`which xrdcp`
  export X509_USER_PROXY="$BASEDIR/x509up_u5407"
  echo " Proxy: $X509_USER_PROXY"
  voms-proxy-info -all
elif [[ $FULL_FILE == "S3://"* ]]
then
  printf " Found a S3 file: $FULL_FILE\n Use MinIo.\n"
  TOOL="mcs3 cp"
  SOURCE=`echo $FULL_FILE | sed 's#S3://#S3R/#'`
  export PATH="${PATH}:/cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/utils/bin"
  echo " MINIO: "`which mcs3`
  mcs3 config host add S3R https://dtn01.sdcc.bnl.gov:9000/ eicS3read eicS3read
else
  printf " File: $FULL_FILE is neither xrootd nor MinIo. Exit with rc=1\n"
  exit 1
fi

# check lock
while [ -e "$TARGET.lock" ]
do
  echo " Show target: $TARGET"
  ls -lhrt /tmp |grep $TARGET
  echo " .. sleeping for 10s"
  sleep 10
done

# machine is not locked, grab it and download
if ! [ -e "$TARGET" ]
then
  touch $TARGET.lock
  echo " Locking machine "
  echo "\
  $TOOL  $SOURCE $TARGET"
  $TOOL  $SOURCE $TARGET
  ls -lhrt /tmp
  echo " Release lock."
  rm -f $TARGET.lock
else
  echo ""
  echo " ====================================="
  echo ""
  echo " File is already available."
  ls -lhrt $TARGET*
  echo ""
  echo " ====================================="
  echo ""
fi
