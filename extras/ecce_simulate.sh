#!/bin/bash
#
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:"
echo " PATH: $PATH"

echo " START -- "; date +%s
echo "args: $@"
echo "host: $HOSTNAME"; hostname
echo "user: "`id`
echo "cwd:  "`pwd`
echo "os:   "`lsb_release -a`
echo 
echo "----------------------------------------------"
echo "df -h"
df -h
echo "----------------------------------------------"
echo "ls -ltr"
ls -ltr
echo "----------------------------------------------"
echo "env"
env | sort -u
echo "----------------------------------------------"
echo " ----> PATH: $PATH"
echo

# this is where we start our work
export BASEDIR=`pwd`
echo "\
tar fzx penv.tgz"
tar fzx penv.tgz
ls -lhrt

export tag="$1"
export hash="$2"
export inputFile="$3"
export nskip="$4"
export nevts="$5"
export fid="$6"
export pwg="$7"
export gen="$8"
export coll="$9"

# derived variables
export outputFile=DST_${pwg}_${gen}_${coll}_${fid}_${nskip}_${nevts}.root # DST_SIDIS_pythia6_ep_18x100lowq2_009_1998000_02000.root
export outputPath=${tag}/${hash}/${pwg}/${gen}/${coll}                    # ana.14/5f210c7/SIDIS/pythia6/ep_18x100lowq2

# download input file
./productions/extras/download.sh $inputFile

# Run the simulation
mv productions/extras/* macros/detectors/EICDetector
cd macros/detectors/EICDetector
mkdir -p ${outputPath}/eval
source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n $tag
export ROOT_INCLUDE_PATH=$(pwd)/../../common:$ROOT_INCLUDE_PATH
metaDataFile=${outputPath}/${outputFile}.txt
tmpLogFile=${outputFile}.out
d=`date +%Y/%m/%d`
t=`date +%H:%M`

# Print production details to screen and to metadata file simultaneously
cat << EOF | tee ${metaDataFile}
====== Your production details ======
Production started: ${d} ${t}
Production site: MIT
Production Host: ${HOSTNAME}
ECCE build: $tag
ECCE macros branch: master
ECCE macros hash: $hash
PWG: $pwg
Generator: $gen 
Collision type: $coll
Input file: $inputFile
Output file: $outputFile
Output dir: $outputPath
Number of events: $nevts
Skip: $nskip
=====================================
EOF

echo "Disabling evaluators and enabling DST readout"
./setupFun4All_G4_EICDetector.sh
./setupFun4All_G4_EICDetector.sh

if [ "${coll}" = "singlePion" ]
then
  echo "Setting up pion gun"
  ./setupPionGun.sh
  ./setupPionGun.sh
fi
if [ "${coll}" = "singleElectron" ]
then
  echo "Setting up electron gun"
  ./setupElectronGun.sh
  ./setupElectronGun.sh
fi

# Run Fun4all: send output to stdout but also capture to temporary local file
echo " START DST -- "`date +%s`
echo " #### running \
root.exe -q -b Fun4All_G4_EICDetector.C\($((10#$nevts)),\"$inputFile\",\"$outputFile\",\"\",$((10#$nskip)),\"$outputPath\"\)"
root.exe -q -b Fun4All_G4_EICDetector.C\($((10#$nevts)),\"$inputFile\",\"$outputFile\",\"\",$((10#$nskip)),\"$outputPath\"\) | tee ${tmpLogFile}
$((10#$machinenumber))
rc_dst=$?
echo " rc for dst: $rc_dst"
echo " END DST -- "`date +%s`

# Do some basic error handling here: is this failed we need to abort! Continuing might cause broken files on all levels.
if [ ".$rc_dst" != ".0" ]
then
  echo " DST production failed. EXIT here, no file copy will be initiated!"
  exit $rc_dst
fi

# Scan stdout of Fun4all for random number seeds and add to metadata file
echo production script finished, writing metadata
echo "" >> ${metaDataFile}
echo Seeds: >> ${metaDataFile}
grep 'PHRandomSeed::GetSeed()' ${tmpLogFile} | awk '{print $3}' >> ${metaDataFile}
rm ${tmpLogFile}

echo "" >> ${metaDataFile}
echo md5sum: >> ${metaDataFile}
md5sum ${outputPath}/${outputFile} | awk '{print $1}' >> ${metaDataFile}

echo " START EVAL -- "`date +%s`
echo " #### running \
root.exe -q -b Fun4All_runEvaluators.C\(0,\"$outputFile\",\"$outputPath\",0,\"$outputPath\"\)"
root.exe -q -b Fun4All_runEvaluators.C\(0,\"$outputFile\",\"$outputPath\",0,\"$outputPath\"\)
rc_eval=$?
echo " rc for eval: $rc_eval"
echo" END EVAL -- "`date +%s`

# Do some more error handling here.
if [ ".$rc_eval" != ".0" ]
then
  echo " EVAL production failed. Delete the potentially broken or incomplete EVAL files."
  echo " --> but keeping the DST and continue to copy."
  rm -rf ${outputPath}/eval*
fi

# Show the complete output we have produced
echo ":::::::::::::::::::::::::::::::::::::::::::::"
echo " output directory contents"
find ${outputPath}
echo ":::::::::::::::::::::::::::::::::::::::::::::"

# Moving the output to the base directory
mv `echo ${outputPath} | cut -d/ -f1` ../../../
pwd
chmod 750 copy_to_T2.sh
cp copy_to_T2.sh ../../../
cd ../../../
pwd


# Copy files to final storage destination.

# Write outputs to MIT T2
echo "----------------------------------------------"
echo "files:"
ls -ltr 

outputRelPathTopDirName=$(echo "${outputPath}" | cut -d "/" -f1)
./copy_to_T2.sh ${outputRelPathTopDirName} ""

echo "----------------------------------------------"
echo "removing all files created"
echo "\
rm -rf ${outputRelPathTopDirName}"
rm -rf ${outputRelPathTopDirName}

echo " END -- "`date +%s`
