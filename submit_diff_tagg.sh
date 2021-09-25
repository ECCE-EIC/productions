#/usr/bin/bash
rm slurm_submission.out
touch slurm_submission.out

<<<<<<< HEAD
#for f in productionSetups/run_DiffractiveAndTagging_*; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre_ePb-18x108-*; do
#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_e[PZ]* ; do
=======
<<<<<<< HEAD
for f in productionSetups/run_DiffractiveAndTagging_*; do
=======
<<<<<<< HEAD
#for f in productionSetups/run_DiffractiveAndTagging_*; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre_ePb-18x108-*; do
for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_e[PZ]* ; do
>>>>>>> master

#for f in productionSetups/run_ExclusiveReactions_topeg_eA-* ; do
#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-* ; do

#for f in productionSetups/run_ExclusiveReactions_MILOU3D_ep-* ; do
<<<<<<< HEAD
for f in productionSetups/run_ExclusiveReactions_topeg_eA-*DVCS.txt ; do 
=======
=======
for f in productionSetups/run_DiffractiveAndTagging_*; do
>>>>>>> master
>>>>>>> e6e022181ed5f51de18589494be0b10948f03339
>>>>>>> master
  python3 setupProduction.py JLAB $f | grep submitJobs.sh >> slurm_submission.out
done

