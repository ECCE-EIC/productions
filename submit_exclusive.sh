#/usr/bin/bash

bash_file="slurm_exclusive_submission.out"

rm $bash_file 
touch $bash_file

touch sim_exe_path.out

#for f in productionSetups/run_DiffractiveAndTagging_*; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre_ePb-18x108-*; do
#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_e[PZ]* ; do
#for f in productionSetups/run_DiffractiveAndTagging_*; do
#for f in productionSetups/run_DiffractiveAndTagging_*; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre_ePb-18x108-*; do
#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_e[PZ]* ; do

#for f in productionSetups/run_ExclusiveReactions_topeg_eA-* ; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-* ; do

#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-* ; do
#for f in productionSetups/run_ExclusiveReactions_topeg_eA-*DVCS.txt ; do 
#for f in productionSetups/run_DiffractiveAndTagging_*; do
for f in productionSetups/run_ExclusiveReactions_*IP6.txt; do
  python3 setupProduction.py JLAB $f | grep submitJobs.sh >> $bash_file
  python3 setupProduction.py JLAB $f | grep "Output directory" >> sim_exe_path.out
#  python3 setupProduction.py JLAB $f | grep "Output directory"
	echo $f
done





