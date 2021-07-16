#!/usr/bin/env python
#===================================================================================================
# Test whether all expected output files have really been produced. This is not very clean or
# elegant but I used it by hand and it found all missing files and suggested deletions that I
# execute by hand.
#===================================================================================================
import subprocess
import time
import os,sys
from optparse import OptionParser

# define and get all command line arguments
parser = OptionParser()
parser.add_option("-p","--physicsGroup",dest="physicsGroup",default='SIDIS',help="physics group")
parser.add_option("-g","--generator",dest="generator",default='pythia6',help="generator used")
parser.add_option("-c","--collisions",dest="collisions",default='ep_18x100lowq2',help="collision setup")
# technical parameters
parser.add_option("-e","--execute",dest="execute",default=False,action="store_true",help="Execute condor_submit.")
# read them all
(opts, args) = parser.parse_args()

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

(tag,hash) = findConfig()

dstFiles = []
evalFiles = []

fileIds = []
allFiles = {}

#sample = 

tags = ['g4cemc', 'g4eemc', 'g4event', 'g4femc', 'g4fhcal', 'g4hcalin', 'g4hcalout', 'g4tracking']

common_r = '.root'
common_e = '_eval'
common = 'DST_%s_%s_%s_'%(opts.physicsGroup,opts.generator,opts.collisions)
remoteFile = "S3/eictest/ECCE/MC/%s/%s/%s/%s/%s"%(tag,hash,opts.physicsGroup,opts.generator,opts.collisions)
cmd = ["mc", "ls", remoteFile, "| grep root"]
#print(' '.join(cmd))
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out,err) = proc.communicate()

for line in out.decode().split('\n'):
    f = line.split(' ')[-1]
    if '.root' in f:
        id = f.replace(common,"")
        id = id.replace(common_r,"")
        dstFiles.append(id)
        if '.txt' not in f:
            #print(" append -> %s"%(id))
            fileIds.append(id)
            #sys.exit(0)

remoteFile = "%s/eval_00000"%(remoteFile)
cmd = ["mc", "ls", remoteFile, "| grep root"]
#print(' '.join(cmd))
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out,err) = proc.communicate()

for line in out.decode().split('\n'):
    f = line.split(' ')[-1]
    if '.root' in f:
        id = f.replace(common,"")
        id = id.replace(common_r,"")
        id = id.replace(common_e,"")
        evalFiles.append(id)
        tag = id.split('_')[-1]
        if tag in tags:
            pass
        else:
            print(" Adding a tag: %s"%(f))
            tags.append(tag)

print(" Tags found in list:")
for tag in tags:
    print(" -> %s"%tag)


files = {}

# make a list of all possible files
for fileId in fileIds:
    files["%s"%(fileId)] = 0
    files["%s.txt"%(fileId)] = 0
    for tag in tags:
        files["%s_%s"%(fileId,tag)] = 0

# now go through the files we found and mark them
for f in dstFiles:
    if files.has_key(f):
        files[f] += 1
    else:
        print(" ERROR found file not in all list!: %s"%(f))
        if '.txt' not in f:
            files[f] = 0

for f in evalFiles:
    if files.has_key(f):
        files[f] += 1
    else:
        print(" ERROR found file not in all list!: %s"%(f))
        files[f] = 0

# collect inconsistent Ids (badIds)
badIds = {}
for key in sorted(files.keys()):
    if files[key] == 0:
        print(" Missing file: %s"%(key))
        fileId = "_".join(key.split("_")[0:3])
        if badIds.has_key(fileId):
            badIds[fileId] += 1
        else:
            badIds[fileId] = 1

# what to do about the badIds
if len(badIds) > 0:
    if opts.execute:
        print(" Executing:")
    else:
        print("# NOT Executing:")
    
    for key in badIds:
        #cmd = "mc rm S3/eictest/ECCE/MC/ana.14/5f210c7/SIDIS/pythia6/ep_18x100lowq2/%s%s.root"%(common,key)
        cmd = "mc rm S3/eictest/ECCE/MC/%s/%s/%s/%s/%s/%s%s.root"\
              %(tag,hash,opts.physicsGroup,opts.generator,opts.collisions,common,key)
        if opts.execute:
            print(" %s"%(cmd))
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out,err) = proc.communicate()
            print("OUT:\n"%(out.decode()))
            print("ERR:\n"%(err.decode()))
        else:
            print(" %s"%(cmd))
