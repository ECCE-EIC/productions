echo " ---- Rebuilt ----"
cd ~/ecce/eccesw/002/ECCESW_ana.14/productions
python setupProduction.py MIT productionSetups/SIDISSetup_ep_18x100_lowq2.txt
cd ~/ecce/eccesw/002/ECCESW_ana.14/productions/submissionFiles/SIDIS/pythia6/ep_18x100lowq2/mitJobs
condor_submit mitJob_SIDIS_pythia6_ep_18x100lowq2_000_0001000_01000.job
