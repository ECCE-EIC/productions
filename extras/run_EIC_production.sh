#!/bin/bash

source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n $6

export ROOT_INCLUDE_PATH=$(pwd)/../../common:$ROOT_INCLUDE_PATH

metaDataFile=${5}/${3}.txt
tmpLogFile=${3}.out

d=`date +%Y/%m/%d`
t=`date +%H:%M`

# Print production details to screen and to metadata file simultaneously
cat << EOF | tee ${metaDataFile}
====== Your production details ======
Production started: ${d} ${t}
Production site: $9
Production Host: ${HOSTNAME}
ECCE build: $6
ECCE macros branch: ${12}
ECCE macros hash: $8
PWG: $7
Generator: ${10} 
Collision type: ${11}
Input file: $2
Output file: $3
Output dir: $5
Number of events: $1
Skip: $4
=====================================
EOF

echo "Disabling evaluators and enabling DST readout"
./changeFun4All_G4_EICDetector.sh

# Run Fun4all. Send output to stdout but also capture to temporary local file
echo running root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\)
root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\) | tee ${tmpLogFile}

# Scan stdout of Fun4all for random number seeds and add to metadata file
echo production script finished, writing metadata
echo "" >> ${metaDataFile}
echo Seeds: >> ${metaDataFile}
grep 'PHRandomSeed::GetSeed()' ${tmpLogFile} | awk '{print $3}' >> ${metaDataFile}
rm ${tmpLogFile}

echo "" >> ${metaDataFile}
echo md5sum: >> ${metaDataFile}
md5sum ${5}/${3} | awk '{print $1}' >> ${metaDataFile}

echo "DST has been created"
echo "Now producing evaluators"

root.exe -q -b Fun4All_runEvaluators.C\(0,\"$3\",\"$5\",0,\"$5\"\)

echo "script done"
