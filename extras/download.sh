#!/bin/bash
#
# Download the input file to local /tmp with locking
#
# FULL_FILE="root://xrootd.cmsaf.mit.edu//store/user/paus/ecce/ep_noradcor.18x100lowq_run001.root"
#
XR="root://xrootd.cmsaf.mit.edu//store/user/paus/ecce"
FULL_FILE="$1"
FILE=`basename $FULL_FILE`
TARGET="/tmp/$FILE"

echo ""
echo " Downloading: $@"
echo " on host: "`hostname`
echo " from: $XR/$FILE"
echo ""
source /cvmfs/grid.cern.ch/centos7-ui-test/etc/profile.d/setup-c7-ui-example.sh
echo "XRDCP: "`which xrdcp`
export X509_USER_PROXY="$BASEDIR/x509up_u5407"
echo " Proxy: $X509_USER_PROXY"
voms-proxy-info -all

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
  echo " xrdcp: "`which xrdcp`
  echo "\
  xrdcp  $XR/$FILE /tmp/$FILE\
  "
  xrdcp  $XR/$FILE /tmp/$FILE
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
