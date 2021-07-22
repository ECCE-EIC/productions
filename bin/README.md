# Introduction

Production is setup in fundamentally two independent steps. The installation of the software for a
given release (defined by tag and hash) and the management of the various processing requests.

The below given example is designed to install a defined release (ana.14, 5f210c7) and submit a test
production where a test sample is submitted for processing. There will be 10 jobs each producing 10
events. It should finish from beginning to start in about 10 minutes and is testing the entire
setup, including the retrieval of files from S3, processing the DST and the eval files and finally
copying all received output back to S3. It can also perform a rudimentary timing analysis based on
tags placed in the log file. Ideally a summary file with those numbers would be produced but having
a hook for logfile analysis is very useful and can be easily extended to cover a variety of tests.
Plotting could also be included :-)

# Installation of the software

    INSTALL_DIR=$HOME/ecce/000   # option: increment the 000 counter for each new production release
    TAG=ana.14
    HASH=5f210c7
  
    # go here
    cd $INSTALLDIR
  
    # make sure to remove old stuff, if there was an install already
    rm -rf macros productions
  
    git clone https://github.com/ECCE-EIC/macros.git
    git clone https://github.com/ECCE-EIC/productions.git
  
    # get the right version
    cd macros
    git checkout -b $BRANCH
    git branch --set-upstream-to=origin/production_SIDIS production_SIDIS
    git config --local advice.detachedHead false
    git checkout $HASH
  
    # make the tarball that is used for all productions in this instance
    cd $INSTALL_DIR
    tar fzc penv_${TAG}_${HASH}.tgz macros productions


# Production process

It is important to run production from the 'productions' directory, where the current release is
installed. This would be $INSTALLDIR/productions. Please, make sure to edit the setup.sh files to
reflect your site. The PENV_LOG directory is used to store all log files and the corresponding files
used in the production, which are the tar ball and the executable (ecce_simulate.sh). Make sure
there is enough space, and the path is not too long so you can get there quick.

    # get setup
    cd $INSTALLDIR/productions
    source setup.sh

The work horses for input and output are captured in the shell scripts:

    ./bin/download.sh
    ./bin/copy_to_S3.sh

For now the download will download the generator input file to the /tmp directory of the worker
which could potentially overflow. It might be better to download to the work directory. For tests at
MIT this scheme worked well. The first job arriving on a given node will perform the download, while
first locking the node to ensure other jobs arriving do not try the download of the same file and
wait for the completion. This has worked well for me but can lead to problems like stuck locks or
broken files remaining in the /tmp directory.

Job status is during submission checked in the general condor job status logic. It should be easy to
adjust to slurm. Completion is checked by explicitly checking for the presence of the DST output
file. Again, potential pitfalls are missing metadata files or missing 'eval' files. For now this can
be checked semi automatically by hand. Deleting a corresponding problematic DST file would simple lead
to a re-submission of the missing file (including .txt and evals).

To get your job going use the following command, where the parameters should be self explanatory:

     ./bin/submit.py -i inputFileListsMit -p TEST -g pythia6 -c ep_18x100lowq2 -n 10

This will do a test run. That means create the submission script and tell you the job status. It can
be executed at any point safely. To really 'e'xecute we add the -e option

    ./bin/submit.py -i inputFileListsMit -p TEST -g pythia6 -c ep_18x100lowq2 -n 10 -e

Also this command can be executed later safely, only it will find jobs that are missing and
re-submit them. The will overwrite the .out and .err files from the previous jobs so be sure you do
not need them anymore.

Finally doing a 't'iming analysis you can just add the -t option and per job times and averages are
extracted from the log files.

    ./bin/submit.py -i inputFileListsMit -p TEST -g pythia6 -c ep_18x100lowq2 -n 10 -t


# Some production basic numbers from tests (ana.14,  (DST_SIDIS_pythia6_ep_18x100lowq2)

    1000 events --> 172M --> (2:16hr)
    1616 events --> 278M --> (3:40hr)
                    369M --> (4:50hr)
    3000 events --> 516M --> (6:48hr)
