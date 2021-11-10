#!/bin/bash
#
# This is a modified version of run_EIC_production.sh that skips
# DST production and only runs the evaluator files.
#
# This also takes a 13th argument to specify the exact revision
# number to use for the evaluator output instead of using the 
# automatic mechanism in Fun4All_runEvaluators.C.
#
# NOTE: This is done in a VERY HACKY way. We basically tell
# Fun4All_runEvaluators.C to use a temporary output directory
# and then move the files it creates into the real directory.
# The alternative is to modify Fun4All_runEvaluators.C and
# re-tag it with a different hash. This would affect everyone
# else's campaigns unecessarily since nothing substantive in
# the macros was changed.
#
# NOTE: If a value of "-1" is passed for the evaluator output revision
# then the automatic mechanism IS used to determine the evaluators
# output directory and no temporary directory is used.
#

unset LD_PRELOAD

source /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh -n $6

export ROOT_INCLUDE_PATH=$(pwd)/../../common:$ROOT_INCLUDE_PATH

metaDataFile=${5}/${3}.txt
tmpLogFile=${3}.out

d=`date +%Y/%m/%d`
t=`date +%H:%M`

# Print production details to screen and to metadata file simultaneously
cat << EOF | tee ${tmpLogFile}
====== Evaluator only pass ======
Production started: ${d} ${t}
Production site: $9
Production Host: ${HOSTNAME}
ECCE build: $6
ECCE macros branch: ${12}
ECCE macros hash: $8
PWG: $7
Generator: ${10} 
Collision type: ${11}
Evaluator output revision: ${13}
Input file: $2
Output file: $3
Output dir: $5
Number of events: $1
Skip: $4
=====================================
EOF

cat ${tmpLogFile} >> ${metaDataFile}

# Run Fun4all. Send output to stdout but also capture to temporary local file
#echo running root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\)
#root.exe -q -b Fun4All_G4_EICDetector.C\($1,\"$2\",\"$3\",\"\",$4,\"$5\"\) | tee ${tmpLogFile}
#
#rc_dst=$?
#echo " rc for dst: $rc_dst"

# Do some basic error handling here: is this failed we need to abort! Continuing might cause broken files on all levels.
#if [ ".$rc_dst" != ".0" ] || ! [ -e "$outputPath/$outputFile" ] 
#then
#  echo " DST production failed. EXIT here, no file copy will be initiated!"
#  ls -lhrt $outputPath
#  exit $rc_dst
#fi

# Scan stdout of Fun4all for random number seeds and add to metadata file
#echo production script finished, writing metadata
#echo "" >> ${metaDataFile}
#echo Seeds: >> ${metaDataFile}
#grep 'PHRandomSeed::GetSeed()' ${tmpLogFile} | awk '{print $3}' >> ${metaDataFile}
#rm ${tmpLogFile}

#echo "" >> ${metaDataFile}
#echo md5sum: >> ${metaDataFile}
#md5sum ${5}/${3} | awk '{print $1}' >> ${metaDataFile}

#echo "DST has been created"

echo "Skipped DST production"
echo "Now producing evaluators"

if [ ".${13}" == ".-1" ]; then
  # Use default (i.e. allow Fun4All_runEvaluators.C to choose)
  outdir=${5}
else
  # Use temporary directory for output so values can be moved to user-specified directory
  tmp_outdir=${5}/eval_tmp/skip_${4}
  outdir=${tmp_outdir}
fi

root.exe -q -b Fun4All_runEvaluators.C\(0,\"$3\",\"$5\",0,\"${outdir}\"\)

rc_eval=$?
echo " rc for eval: $rc_eval"
# Do some more error handling here.
if [ ".$rc_eval" != ".0" ]
then
  echo " EVAL production failed. Delete the potentially broken or incomplete EVAL files."
else
  echo " EVAL production succeeded."
fi

if [ ".${tmp_outdir}" != "." ]; then
  # Outputs were written to temporary directory. Move them to user-specified one
  user_specified_evaldir=$(printf "${5}/eval_%05d" ${13})
  echo "mkdir -p ${user_specified_evaldir}"
  mkdir -p ${user_specified_evaldir}
  base=`basename ${3} .root`
  echo "mv ${outdir}/eval_00000/${base}\*.root ${user_specified_evaldir}"
  mv ${outdir}/eval_00000/${base}*.root ${user_specified_evaldir}
  echo "rm -rf ${tmp_outdir}"
  rm -rf ${tmp_outdir}
fi



echo "script done"
