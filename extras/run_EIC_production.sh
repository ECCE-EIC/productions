#!/bin/bash

source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n $6

d=`date +%Y/%m/%d`
t=`date +%H:%M`

# Print production details to screen and to metadata file simultaneously
cat << EOF | tee ${5}/${3}.txt
====== Your production details ======
Production started: ${d} ${t}
Production site: $9
Production Host: ${HOST}
ECCE build: $6
ECCE macros branch: production_$7
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

# Run Fun4all. Send output to stdout but also capture to temporary local file
echo running root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\)
root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\) | tee tmp.out

# Scan stdout of Fun4all for random number seeds and add to metadata file
echo production script finished, writing metadata
grep -i seed tmp.out >> ${5}/${3}.txt
rm tmp.out

echo "script done"
