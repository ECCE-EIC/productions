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
#for f in productionSetups/run_DiffractiveAndTagging_*-IP8*; do
#for f in productionSetups/run_DiffractiveAndTagging_EIC_mesonMC_ep-*; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-*; do
#for f in productionSetups/run_DiffractiveAndTagging_*.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre*.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre*3T*.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-10x100-NeutronSS-q2-*; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-18x166-NeutronSS-q2-*; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-18x166-NeutronSS-q2-*; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-5x41-NeutronSS-q2-*; do
#for f in productionSetups/run_DiffractiveAndTagging_DEMP_ep-*-IP8.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_DEMP_ep-*3T-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_elSpectro_ep-*3T-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_EIC_mesonMC_ep-*noB0-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_EIC_mesonMC_ep-*-IP6.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_ePb-18x108-*Diff*.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_EIC_mesonMC*PiStruc-IP8.txt; do

#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_e*nobeampipe.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_*v2.2*.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_Sartre_ePb-18x108-*; do
#for f in productionSetups/run_DiffractiveAndTagging_BeAGLE_ePb-18x108-*; do
#for f in productionSetups/run_LoQ2Tagger_pythia6_ep-*XYZ*.txt ; do
#for f in productionSetups/run_DiffractiveAndTagging*.txt ; do
#for f in productionSetups/run_DiffractiveAndTagging_Djangoh_eHe3-*.txt ; do
#for f in productionSetups/run_DiffractiveAndTagging_elSpectro_ep-*.txt; do
#for f in productionSetups/run_DiffractiveAndTagging_*Xinbai*.txt; do
for f in productionSetups/run_DiffractiveAndTagging_*Xinbai*.txt; do
  python3 setupProduction.py JLAB $f | grep submitJobs.sh >> slurm_submission.out
#  python3 setupProduction.py JLAB $f | grep "Output directory" >> sim_path.out
  python3 setupProduction.py JLAB $f | grep "Output directory" | sed 's/Output directory: //' >> sim_path.out
#  python3 setupProduction.py JLAB $f | grep "Output directory"
#	echo $f
done


