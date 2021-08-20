#/usr/bin/bash
rm slurm_submission.out
touch slurm_submission.out

for f in productionSetups/run_DiffractiveAndTagging_*; do
  python3 setupProduction.py JLAB $f | grep submitJobs.sh >> slurm_submission.out
done

