#!/usr/bin/env python
#
# CAUTION:
#
# This script is used to copy files back to the BNL S3 storage
# from a remote site. To do this, it contains secret information
# used for authentication. This file should be kept securely on
# the OSG submit host. OSG condor will transfer it securely to 
# the remote site to run. 
#
# DO NOT PUBLISH THIS SCRIPT WITH KEYS HAVING WRITE ACCESS!
# (this includes committing it to GitHub!)
#
#
# This should take two arguments: 
#
#  outputPath   - The top level directory holding the output files (should be "DST_files")
#  outputDest   - The destination directory of the remote site prefixed with "S3://"
#
#  
#  Example:
#
#  If you have these two files in this directory structure:
#
#      testdir/level1/level2/test.root
#      testdir/level1/level2/level3/junk.log
#
# Running:
#
#  ./copy_to_S3.py testdir/ S3://eictest/ECCE
#
#
# will copy the files to the S3 storage as:
#
#      eictest/ECCE/testdir/level1/level2/test.root
#      eictest/ECCE/testdir/level1/level2/level3/junk.log
#
# n.b. all necessary directories on the S3 site will be created
# 

import os, sys
import subprocess

# Authentication info (edit to use your write-privileged username/access key)
user      = 'eicS3read'
accesskey = 'eicS3read'

# Full path to minio "mc" executable to use
mc = '/cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/utils/bin/mcs3'

# Check that we have both command line arguments
if len(sys.argv) < 3:
    print()
    print('Usage:  copy_to_S3.py outputPath outputDest')
    print()
    print('  where outputPath is local directory and outputDest is remote directory prefixed with "S3://"')
    print()
    sys.exit()
    
outputPath = sys.argv[1]
outputDest = sys.argv[2]
print("copy_to_S3.py: '" + outputPath + "' -> '" + outputDest + "'")

# Remove "S3://" prefix from outputDest
outputDest = outputDest.replace('S3://', '')

# Check that "mc" executable exists
if not os.path.exists(mc):
    print('The executable "%s" does not exist!' % mc)
    sys.exit()


# Use local working directory as home since that is where mcs3 will
# store its config (including secrets). Configure BNL host
os.environ['HOME'] = os.getcwd()
os.system(mc + " config host add S3 https://dtn01.sdcc.bnl.gov:9000/ %s %s" % (user, accesskey) )

# Walk the specified directory tree and copy all files to remote site
for dirname,subdirname,filelist in os.walk(outputPath):

    #print(" OutputDest: %s"%(outputDest))

    # Don't bother making empty directories
    if len(filelist) == 0:
        continue

    remoteDir = os.path.join('S3', outputDest, dirname)
    cmd = [mc, 'mb', '-p', remoteDir]
    print(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()
    print( output[0].decode() )
    print( output[1].decode() )

    #sys.exit(0)
	
    for f in filelist:
        localFile  = os.path.join(dirname, f)
        remoteFile = os.path.join(remoteDir, f)
        cmd = [mc, 'cp', '--quiet', '--no-color', localFile, remoteFile]
        print(' '.join(cmd))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.communicate()
        print( output[0].decode() )
        print( output[1].decode() )

# Clean up so we don't leave the authentication info on the filesystem
os.system(mc + " config host rm S3")
