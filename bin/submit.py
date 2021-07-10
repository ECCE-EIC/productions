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
### production tags/hash - should be deduced from the installation
##parser.add_option("-t","--tag",dest="tag",default='ana.14',help="production tag")
##parser.add_option("-a","--hash",dest="hash",default='5f210c7',help="production hash")
# samples
parser.add_option("-p","--physics_group",dest="physics_group",default='SIDIS',help="physics group")
parser.add_option("-g","--generator",dest="generator",default='pythia6',help="generator used")
parser.add_option("-c","--collisions",dest="collisions",default='ep_18x100lowq2',help="collision setup")
parser.add_option("-n","--nEvtsPerJob",dest="nEvtsPerJob",default='2000',help="# of Events per simulation job")
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

# Depending on what was installed - could be overwritten by hand but not recommended
(tag,hash) = findConfig()

# Setting up the sample and related request
sample = penv.Sample(options.physics_group,options.generator,options.collisions,int(options.nEvtsPerJob))
req = penv.Request(tag,hash,sample)
req.sample.show()

# Create a submit engine
# - make an id for the submitter
id = datetime.now().strftime("%Y%m%d_%H%M%S")
# - instantiate the submitter
sub = penv.Submitter(id)

# Generate the submission script and submit
sub.submit(req)
