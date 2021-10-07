#/usr/bin/bash
rm slurm_submission.out
touch slurm_submission.out

touch sim_path.out

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
#for f in productionSetups/run_DiffractiveAndTagging*-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_e*-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_DEMP_ep-5x41-K*; do
#for f in productionSetups/run_DiffractiveAndTagging_*-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_DEMP_ep-*-pionFF-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-*IP6*; do
for f in productionSetups/run_DiffractiveAndTagging_*-IP8*; do
#for f in productionSetups/run_DiffractiveAndTagging_EIC_mesonMC_ep-*; do
  python3 setupProduction.py JLAB $f | grep submitJobs.sh >> slurm_submission.out
  python3 setupProduction.py JLAB $f | grep "Output directory" >> sim_path.out
#  python3 setupProduction.py JLAB $f | grep "Output directory"
#	echo $f
done


