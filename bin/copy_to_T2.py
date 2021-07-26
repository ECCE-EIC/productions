#!/usr/bin/env python
import os, sys, time
import subprocess

rbase = "gsiftp://se01.cmsaf.mit.edu:2811//cms/store/user/paus"
lbase = "file://%s"%os.getcwd()

# Check that we have both command line arguments
if len(sys.argv) < 3:
    print()
    print(' Usage:  copy_to_T2.py  <outputPath>  <outputDest>')
    print()
    print('  <outputPath>      local relative directory prefixed with %s'%lbase)
    print('  <outputDest>      remote directory prefixed with %s'%rbase)
    print()
    sys.exit()
    
outputPath = sys.argv[1]
outputDest = sys.argv[2]
print(" copy_to_T2.py: %s/%s  ->  %s/%s"%(lbase,outputPath,rbase,outputDest))

# Walk the specified directory tree and copy all files to remote site
rc = 0 # register the sum of the return codes (0 - means no error occured)
for dirname,subdirname,filelist in os.walk(outputPath):

    print(" D,S: %s %s"%(dirname,subdirname))

    # No empty directories
    if len(filelist) == 0:
        continue

    remoteDir = os.path.join(rbase,dirname)
    for f in filelist:
        localFile  = "%s/%s"%(lbase,os.path.join(dirname,f))
        remoteFile = os.path.join(remoteDir,f)
        cmd = ["gfal-copy", "-f", localFile, remoteFile]
        print(' '.join(cmd))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while proc.poll() is None: # Process hasn't exited yet, let's wait some
            time.sleep(0.5)
        rc += int(proc.returncode)
        output = proc.communicate()
        print(output[0].decode())
        print(output[1].decode())

print(" copy_to_T2.py: Completed - sum of return codes: %d"%(rc))
