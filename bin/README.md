# Installation of the software [ independent of the submission or production requests, values are examples ]

    INSTALL_DIR=$HOME/ecce
    BRANCH=production_SIDIS
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
    git branch --set-upstream-to=origin/$BRANCH $BRANCH
    git config --local advice.detachedHead false
    git checkout $TAG
  
    cd $INSTALL_DIR
  
    tar fzc penv_${TAG}_${HASH}.tgz macros productions


# Production process

Make sure input and output are properly taken care of.

    --> extras/download.sh
    --> extras/copy_to_*

Check that you update the methods how to extract the completed jobs and the queued jobs. It is in the class Request the two methods loadCompletedJobs() and loadQueuedJobs().

    --> python/penv.py

Submit a specific request using condor

    cd $INSTALL_DIR/productions
    source ./setup.sh
    ./bin/submit.py -h
    ./bin/submit.py -p SIDIS -g pythia6 -c ep_18x100lowq2   [ -n 2000 ]

The input list is automatically constructed from the input parameters. It probably means you have to rename that file according to the conventions:

    ./inputFiles/${PWG}_${GENERATOR}_${COLLISIONS}.list


# Production basic numbers from tests (ana.14,  (DST_SIDIS_pythia6_ep_18x100lowq2)

    1000 events --> 172M --> (2:16hr)
    1616 events --> 278M --> (3:40hr)
                    369M --> (4:50hr)
    3000 events --> 516M --> (6:48hr)
