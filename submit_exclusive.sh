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

#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-* ; do
#for f in productionSetups/run_ExclusiveReactions_topeg_eA-*DVCS.txt ; do 
#for f in productionSetups/run_DiffractiveAndTagging_*; do
#for f in productionSetups/run_ExclusiveReactions_*IP6.txt; do
#for f in productionSetups/run_ExclusiveReactions_LAger_ep-*; do
#for f in productionSetups/run_ExclusiveReactions_*IP8*; do
#for f in productionSetups/run_ExclusiveReactions_*; do
#for f in productionSetups/run_ExclusiveReactions_*lumi10*; do
#for f in productionSetups/run_ExclusiveReactions_LAger_ep-*lumi10-3T-IP6*; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-*[0-9]-DVCS-IP6.txt; do
#for f in productionSetups/run_ExclusiveReactions_*0p7*; do
#for f in productionSetups/run_ExclusiveReactions_Sartre_ePb-18x108-phi-KK-b*; do
#for f in productionSetups/ExclusiveReactions-r7-prop.5.1/run_ExclusiveReactions_Sartre_ePb-18x108-phi-*; do
#for f in productionSetups/run_ExclusiveReactions_EpIC_ep-[15][^0]*; do
#for f in productionSetups/run_ExclusiveReactions_EpIC_*Pi0*; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-*Full*; do
#for f in productionSetups/run_ExclusiveReactions_*; do
#for f in productionSetups/run_ExclusiveReactions_KM20*; do
#for f in productionSetups/run_LoQ2Tagger_*TCS*; do
#for f in productionSetups/run_ExclusiveReactions_LAger_ep*; do
#for f in productionSetups/run_ExclusiveReactions_*; do
#for f in productionSetups/run_ExclusiveReactions_topeg*; do
#for f in productionSetups/run_ExclusiveReactions_EpIC_ep-*TCS*; do
#for f in productionSetups/run_ExclusiveReactions_LAger_ep-*; do

#for f in productionSetups/run_ExclusiveReactions_topeg*; do

#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-5x41-DVCS-*; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-5x41-DVCS-*IP8*; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-10x100-DVCS-*; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-10x100-DVCS-BH*; do

#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-18x275-DVCS-*IP8.txt; do
#for f in productionSetups/run_ExclusiveReactions_*_ePb-18x108-phi*; do


for f in productionSetups/run_ExclusiveReactions_MILOU3D_*; do
  python3 setupProduction.py JLAB $f | grep submitJobs.sh >> $bash_file
#  python3 setupProduction.py JLAB $f | grep "Output directory" >> sim_exe_path.out
  python3 setupProduction.py JLAB $f | grep "Output directory" | sed 's/Output directory: //' >> sim_exe_path.out

#  python3 setupProduction.py JLAB $f | grep "Output directory"
	echo $f
done

