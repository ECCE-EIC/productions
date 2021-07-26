# Installation of the software [ independent of the submission or production requests ]

  INSTALL_DIR=$HOME/ecce
  BRANCH=production_SIDIS
  ?? RELEASE=ana.14  seems not to be needed
  TAG=5f210c7

  # go here
  cd $INSTALLDIR

  # make sure to remove old stuff, if there was an install already
  rm -rf macros productions

  git clone https://github.com/ECCE-EIC/macros.git
  git clone https://github.com/ECCE-EIC/productions.git

  # get the right version
  cd macros
  git checkout -b $BRANCH
  git branch --set-upstream-to=origin/$BRANCH $BRANCH
  git config --local advice.detachedHead false
  git checkout $TAG

  cd $INSTALL_DIR

  tar fzc penv.tgz macros productions

# Production process

Make sure input and output are properly taken care of.

  --> extras/download.sh
  --> extras/copy_to_*

Submit a specific request using condor

  cd productions
  ./bin/submit.py -h

  ./bin/submit.py -t ana.14 -a 5f210c7 -p SIDIS -g pythia6 -c ep_18x100lowq2 





# setup

  productionsSetup.py:                             nevents/job = 10
  productionSetups/SIDISSetup_ep_18x100_lowq2.txt: nTotalEvents 500

# Production basic numbers from tests (ana.14,  (DST_SIDIS_pythia6_ep_18x100lowq2)

 1000 events --> 172M --> (2:16hr)
 1616 events --> 278M --> (3:40hr)
                 369M --> (4:50hr)
 3000 events --> 516M --> (6:48hr)

These scripts are used to submit and run ecce simulation production jobs on
the OSG. They were developed at JLab using the scosg16 submit node. 

The simulation output can be directed to go either to JLab storage or BNL S3. This is specified by editing the makeOSGJobs.py script and modifying the line in class pars to be something like one of these:

    simulationsTopDir = 'S3://eictest/ECCE/MC'
    simulationsTopDir = '/work/eic2/ECCE/MC'

If set to the first value, the output files will be pushed to BNL S3 storage straight from the remote OSG node. The files be placed in a directory tree starting with ''eictest/ECCE/MC''. All subdirectories will be automatically created.

If the second form in the above examples is used then the files will be sent back to JLab where they will be stored in the specified directory.

## S3 Write access
The BNL S3 storage can be accessed from anywhere, but requires a username/accesskey pair with write priviliges if one wishes to write to it. These are currently limited to only a few people. The way this works is the copy_to_S3.py file must be copied to the directory where the condor_submit command is being executed from and modified to include the secret information. For example

    cp OSG/copy_to_S3.py .
    chmod 700 copy_to_S3.py
    <edit copy_to_S3.py to include write-authorized username/accesskey>
    condor_submit path/to/file.job

Condor will take care of securely transferring the ''copy_to_S3.py'' file to the remote site. At the end of the job, the script is run where it will copy all of the files back. The ''copy_to_S3.py'' script will set the HOME directory to the local working directory so the minio client will only write the secret infomation locally. It will also remove the configuration just before the script exits to ensure the secret information is not left on the remote job node.
