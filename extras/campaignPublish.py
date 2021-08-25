#!/usr/bin/env python3
#
# This script is used for publishing the eval files for campaigns
# run at JLAB or on the OSG (with files brought back to JLab).
#
# Here publishing means copying from the standard directory on
# the /work/eic2 disk to the xrootd directory AND to the BNL
# S3 storage. This makes the files available to everyone without
# an account at either JLab or BNL.
#
# NOTE: This relies on the extras/campaignStatus.py script to have
# already been run so that the Status_reports/good_DST_files.txt
# file exists. ONLY files in the MOST RECENT eval_xxx folder that
# correspond to DST files in the "good" list will be published.
#
# Currently, no check is made that the eval files themselves are
# good.
#
# This uses the DST directory location to find the most recent
# eval directory and to know where to copy the files to. This
# read from the submitParameters.dat file. This file has a
# format of e.g.:
#
#  SUBMITDIR=/work/eic2/ECCE/PRODUCTION/2021.07.21.Electroweak_Djangoh_ep-10x100nc-q2-10/productions/submissionFiles/Electroweak/Djangoh/ep-10x100nc-q2-10/osgJobs
#  LOGDIR=/work/eic2/ECCE/PRODUCTION/2021.07.21.Electroweak_Djangoh_ep-10x100nc-q2-10/productions/submissionFiles/Electroweak/Djangoh/ep-10x100nc-q2-10/osgJobs/log
#  DSTDIR=/work/eic2/ECCE/MC/prop.2/c131177/Electroweak/Djangoh/ep-10x100nc-q2-10
#  EVENTS_PER_JOB=1000
#
# Run this with no arguments or by passing the name of the
# submitParameters.dat file:
#
#  ./campaignPublish.py
#
#         or
#
#  ./campaignPublish.py ../submissionFiles/*/*/*/*/submitParameters.dat
#

import os, sys, glob, shutil
import uproot
import subprocess

# The following flag will cause a "mcs3 mirror" command to be executed
# that will copy all of the evaluator files from the xrootd directory
# for this campaign to the BNL S3 storage.
# NOTE: For this to work, the command "mcs3" must exist and proper access
# and secret keys registered for it in your ~/.mcs3/config.json file
# for the "S3" alias. 
COPY_TO_S3 = True
mcs3 = '/cvmfs/eic.opensciencegrid.org/gcc-8.3/opt/fun4all/utils/bin/mcs3'


SUBMITDIR      = ''
LOGDIR         = ''
DSTDIR         = ''
EVENTS_PER_JOB = 1

# Read submit parameters from file
submitParametersFile = '/path/to/submitParameters.dat'
if len(sys.argv) > 1:
	submitParametersFile = sys.argv[1]
else:
	if os.path.exists('./submissionFiles'):
		tmp = glob.glob('./submissionFiles/*/*/*/*/submitParameters.dat')
	else:
		tmp = glob.glob('../submissionFiles/*/*/*/*/submitParameters.dat')
	if len(tmp) > 0:
		submitParametersFile = tmp[0]

if not os.path.exists( submitParametersFile ):
	print( 'No file: ' + submitParametersFile )
	sys.exit()

print('Reading campaign parameters from:' + submitParametersFile)
f = open( submitParametersFile )
for line in f.readlines():
	if line.startswith('SUBMITDIR'     ): SUBMITDIR      = line.split('=')[1].strip()
	if line.startswith('LOGDIR'        ): LOGDIR         = line.split('=')[1].strip()
	if line.startswith('DSTDIR'        ): DSTDIR         = line.split('=')[1].strip()
	if line.startswith('EVENTS_PER_JOB'): EVENTS_PER_JOB = line.split('=')[1].strip()

#----------------------------------------------------------

# Get name of most recent evaluator directory
tmp = sorted( glob.glob( DSTDIR + '/eval_*' ) )
if not tmp :
    print('NO eval_* directory in ' + DSTDIR + '/eval_*' )
    sys.exit()
EVALDIR = tmp[-1]  # should be ordered by name. take last one
if not EVALDIR.startswith('/work/eic2/ECCE/MC'):
    print('ERROR: Expecting the evaluator directory to start with "/work/eic2/ECCE/MC"')
    print('       EVALDIR = ' + EVALDIR)

# Open good_DST_files.txt file and read in list of good DSTs
good_fname = 'Status_Reports/good_DST_files.txt'
if not os.path.exists( good_fname ):
    print( 'No file: ' + good_fname + ' ! Please make sure extras/campaignStatus.py has been run!' )
    sys.exit()

# Look for eval files with names corresponding to a good DST file.
# Use the DST file name as the key and the list of corresponding
# eval files as the value.
eval_files = {}

# Loop over good DST files
print('Scanning good DST files for evaluators ...')
f = open( good_fname )
for line in f.readlines():
    if line.startswith('#'): continue
    if not line.startswith( DSTDIR ):
        print( 'ERROR: A DST file in ' + good_fname + ' does not start with the DSTDIR (i.e. ' + DSTDIR + ')')
        print( '\noffending file:\n       ' + line.strip() )
        print( '(nothing copied)' )
        sys.exit()
    fname = os.path.basename( line.strip() )
    fname_base = fname.replace('.root', '')
    eval_files[fname] = glob.glob( os.path.join( EVALDIR, fname_base+'*.root' ) )
    
# Report what we found
Nevalfiles = sum([len(v) for k,v in eval_files.items()] )
ratio = float(Nevalfiles)/float(len(eval_files))

print( '\nFOUND')
print( '--------------------------------------')
print( '              DSTDIR: %s' % DSTDIR )
print( '             EVALDIR: %s' % EVALDIR )
print( ' Num. good DST files: %d' % len(eval_files) )
print( 'Num. evaluator files: %d' % Nevalfiles )
print( '   ratio Neval/N_DST: %f' % ratio )
print( '')

# Determine directory on xrootd server
XROOTD_DIR = EVALDIR.replace('/work/eic2/ECCE/MC', '/work/osgpool/eic/ECCE/MC')
if not os.path.exists( XROOTD_DIR ):
    print('Making directory: ' + XROOTD_DIR )
    os.makedirs(XROOTD_DIR, exist_ok=True)

# Copy all evaluator files to destination
print( 'Copying evaluator files to ' + XROOTD_DIR )
Ncopied   = 0
Nexisting = 0
for dst,evals in eval_files.items():
    for feval in evals:
        if not os.path.exists( os.path.join(XROOTD_DIR, os.path.basename(feval) ) ):
            shutil.copy2( feval, XROOTD_DIR )
            Ncopied += 1
        else:
            Nexisting += 1

print('Copied %d files to xrootd server (%d already were there)' % (Ncopied, Nexisting))

# Mirror all files in xrootd directory on S3
if COPY_TO_S3:
    print( '\nMirroring evaluator files from xrootd to S3 ...' )
    S3DIR = XROOTD_DIR.replace('/work/osgpool/eic/ECCE/MC', 'S3/eictest/ECCE/MC')
    cmd = [mcs3, 'mirror', '--preserve', XROOTD_DIR, S3DIR]
    print( ' '.join(cmd) )
    subprocess.call( cmd )  # must use call() instead of run() since were using python 3.4.3 sometimes

print('\nDone.')

