#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------
# Python setup to submit production request using the production libraries.
#
# Author: C.Paus                                                                      (Jul 07, 2021)
#---------------------------------------------------------------------------------------------------
import os,sys
from datetime import datetime
from optparse import OptionParser
import penv as penv

# define and get all command line arguments
parser = OptionParser()
# production tags/hash
parser.add_option("-t","--tag",dest="tag",default='ana.14',help="production tag")
parser.add_option("-a","--hash",dest="hash",default='5f210c7',help="production hash")
# samples
parser.add_option("-p","--physics_group",dest="physics_group",  default='SIDIS', help="name of plot")
parser.add_option("-g","--generator",dest="generator",default='pythia6',help="name of the generator")
parser.add_option("-c","--collisions",dest="collisions",default='ep_18x100lowq2',help="name of the generator")
# read them all
(options, args) = parser.parse_args()

# Setting up the production
sample = penv.Sample(options.physics_group,options.generator,options.collisions)
req = penv.Request('ana.14','5f210c7',sample)
req.sample.show()

# Create a submit engine
# - first make an id for the submitter
id = datetime.now().strftime("%Y%m%d_%H%M%S")
# - now instantiate the submitter
sub = penv.Submitter(id)

# Generate the submission script
sub.submit(req)
