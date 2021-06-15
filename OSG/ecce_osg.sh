#!/bin/bash
#
# This is run from inside the sinugularity container on
# the remote node.
#
# The submit script needs to pass in 5 arguments:
#
#  arg 1: name of ROOT script (do not include path. Should be in macros/detector/EICDetector) 
#  arg 2: number of events to simulate
#  arg 3: job name (set in submit script)
#  arg 4: cluster  (assigned by condor)
#  arg 5: process  (assigned by condor)
#
# All of the above except for the first 2 arguments are
# used to uniquely identify each job and name directories
# and files.
#

printf "Start time: "; /bin/date
printf "host: "; /bin/hostname -A
printf "user: "; /usr/bin/id
printf "cwd: "; /bin/pwd
printf "os: "; /bin/lsb_release -a
echo 
echo "----------------------------------------------"
echo "df -h"
df -h
echo "----------------------------------------------"
echo "ls -ltr"
ls -ltr
echo "----------------------------------------------"
echo

# First arguments are meant for this script while the rest
# are meant for the run_EIC_production.sh script.
#
# script_name should be run_EIC_production.sh
export script_name=${1}
shift

# outputDest is where to copy output to. There are a few
# options:
#
# 1. A simple directory signifies that condor/OSG will take
# care of copying all of the files back to the submit node.
#
# 2. If it starts with s3:// then it will call the copy_to_s3.sh
# script to copy the files to BNL's S3 storage
#  
export outputDest=${1}
shift

# Remaining arguments are passed to script
export nEventsPerJob=${1}
export inputFile=${2}
export outputFile=${3}
export skip=${4}
export outputPath=${5}

# Setup ECCE environment
#source /cvmfs/eic.opensciencegrid.org/ecce/default/opt/fun4all/core/bin/ecce_setup.sh -n new.2
source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n new.3

# Run the specified script (e.g. run_EIC_production.sh)
cd macros/detectors/EICDetector
mkdir -p ${outputPath}/eval
./${script_name} "$@"

# Output files will be written into $outputPath which should be
# just "DST_files" in the local directory. Move the outputs to 
# the directory we woke up in here so they can be copied to the 
# final destination using the correct protocol. 
mv `echo ${outputPath} | cut -d/ -f1 ` ../../../
pwd
cd ../../../
pwd

# Copy files to final storage destination.

# Test S3
if [[ ${outputdest} == s3://* ]] ; then
	./copy_to_S3.sh
fi

echo "----------------------------------------------"
echo "files:"
ls -ltr 
echo "----------------------------------------------"

printf "End time: "; /bin/date
