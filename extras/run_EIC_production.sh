#!/bin/bash

export HOME=/sphenix/u/${LOGNAME}
source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n $6

logFile="${12}.out"
d=`date +%Y/%m/%d`
t=`date +%H:%M`

echo ====== Your production details ======
echo Production started: ${d} ${t}
echo Production site: $9
echo ECCE build: $6
echo ECCE macros branch: production_$7
echo ECCE macros hash: $8
echo PWG: $7
echo Generator: ${10} 
echo Collision type: ${11}
echo Input file: $2
echo Output file: $3
echo Output dir: $5 
echo Number of events: $1
echo Skip: $4
echo =====================================

echo running root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\)
root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\)
echo production script finished, writing metadata
root.exe -q -b writeMetaData.C\(\"$3\",\"$5\",\"${logFile}\"\)
echo "script done"
