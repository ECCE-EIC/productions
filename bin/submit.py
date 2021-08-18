#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------
# Python setup to submit production request using the production libraries (penv).
#
# Author: C.Paus                                                                      (Jul 07, 2021)
#---------------------------------------------------------------------------------------------------
import os,sys
from datetime import datetime
from optparse import OptionParser
import penv as penv

# define and get all command line arguments
parser = OptionParser()
# define what we want to do
parser.add_option("-i","--inputDir",dest="inputDir",default='inputFileListsMit',help="input list dir")
parser.add_option("-p","--physicsGroup",dest="physicsGroup",default='SIDIS',help="physics group")
parser.add_option("-g","--generator",dest="generator",default='pythia6',help="generator used")
parser.add_option("-c","--collisions",dest="collisions",default='ep_18x100lowq2',help="collision setup")
parser.add_option("-n","--nEvtsPerJob",dest="nEvtsPerJob",default=2000,help="# of Events per simulation job")
# technical parameters
parser.add_option("-e","--execute",dest="execute",default=False,action="store_true",help="Execute condor_submit.")
parser.add_option("-v","--verbosity",dest="verbosity",default=0,help="verbosity of actions")
parser.add_option("-t","--timing",dest="timing",default=False,action="store_true",help="Find timing for completed.")
# read them all
(options, args) = parser.parse_args()

def findConfig():
    # Find out which tag and release we are dealing with (looking for file ../penv_<tag>_<hash>.tgz)
    try:
        for f in os.listdir("../"):
            if f.endswith(".tgz"):
                name = f.split("_")[0]
                tag = f.split("_")[1]
                hash = f.split("_")[2]
                hash = hash.replace(".tgz","")
    except:
        print(" ERROR - missing tar ball for the production (../penv_<tag>_<hash>.tgz).")
        sys.exit(1)

    return (tag,hash)

def timingAnalysis(req):

    logA = penv.LogAnalyzer(req)
    logA.findLogs()
    logA.show()

    import matplotlib.pyplot as plt
    import matplotlib as mlp

    ts = []
    dstTs = []
    evalTs = []
    for key in logA.timings:
        ts.append(logA.timings[key])
        dstTs.append(logA.dstTimings[key])
        evalTs.append(logA.evalTimings[key])

    # love helvetica
    hfont = {'fontname':'Helvetica'}

    # define the figure
    plt.figure('Job timing')
    n, bins, patches = plt.hist(ts, 20, label="Total", histtype='step', linewidth=2.0)
    n, bins, patches = plt.hist(dstTs, 20, label="DST only", histtype='step', linewidth=2.0)
    n, bins, patches = plt.hist(evalTs, 20, label="EVAL only", histtype='step', linewidth=2.0)

    # make a legend
    plt.legend(loc='upper right',frameon=False)

    # make plot nicer
    plt.xlabel('Wall Clock Time for completion [s]', fontsize=22, **hfont)
    plt.ylabel('Number of Jobs', fontsize=22, **hfont)

    # make axis tick numbers larger
    plt.xticks(fontsize=18, **hfont)
    plt.yticks(fontsize=18, **hfont)

    # make sure to noe have too much white space around the plot
    plt.subplots_adjust(top=0.97, right=0.97, bottom=0.13, left=0.12)

    # save plot for later viewing
    plt.savefig("timing.png")     # sends spurios message to the screen 'Unable to parse the pattern', fonts?

    # show the plot for interactive use
    plt.show()

    return

#===================================================================================================
# M A I N
#===================================================================================================

# Depending on what was installed - could be overwritten by hand but not recommended
(tag,hash) = findConfig()

# Setting up the sample and related request
sample = penv.Sample(options.inputDir,options.physicsGroup,options.generator,options.collisions,int(options.nEvtsPerJob))
req = penv.Request(tag,hash,sample)
req.sample.show()

# Create a submit engine (can be used for many submissions)

# - make an id for the submitter
id = datetime.now().strftime("%Y%m%d_%H%M%S")
# - instantiate the submitter
sub = penv.Submitter(id)

# Generate the submission script and submit
##sub.submit(req,options.execute,options.verbosity)
sub.submitSlurm(req,options.execute,options.verbosity)

# Logfile analysis
if options.timing:
    timingAnalysis(req)
