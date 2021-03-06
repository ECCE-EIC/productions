#!/bin/bash
#
# This is run from inside the singularity container on
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
# 2. If it starts with S3:// then it will call the copy_to_s3.py
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
# n.b. This is not really needed since the script_name should be
# run_EIC_production.sh which will source the ecce_setup.sh
# script with the correct build as the argument.
#source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n new.3

# Unpack the macros tarball.
# This will be named something like macros_tag_prop.2.1-production.tgz 
# but will unpack to just "macros".
tar xzf macros*.tgz

# Change to the working directory for the job
cd macros/detectors/EICDetector

# Create the directories needed for the output
mkdir -p ${outputPath}

# Run the specified script (e.g. run_EIC_production.sh)
echo "----------------------------------------------"
printf "cwd: "; /bin/pwd
echo "ls -ltr"
ls -ltr
echo "----------------------------------------------"
echo
echo ./${script_name} "$@"
./${script_name} "$@"

echo ":::::::::::::::::::::::::::::::::::::::::::::"
echo " output directory contents"
find ${outputPath}
echo ":::::::::::::::::::::::::::::::::::::::::::::"

# Output files will be written into $outputPath which should be
# just "DST_files" in the local directory. Move the outputs to 
# the directory we woke up in here so they can be copied to the 
# final destination using the correct protocol. 
mv `echo ${outputPath} | cut -d/ -f1 ` ../../../
pwd
cd ../../../
pwd

# Copy files to final storage destination.

# Write outputs BNL S3 (if appropriate)
if [[ ${outputDest} == S3://* ]] ; then
	outputRelPathTopDirName=$(echo "${outputPath}" | cut -d "/" -f1)
	./copy_to_S3.py ${outputRelPathTopDirName} ${outputDest}
fi

echo "----------------------------------------------"
echo "files:"
ls -ltr 
echo "----------------------------------------------"

printf "End time: "; /bin/date
