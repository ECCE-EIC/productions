#!/usr/bin/env python3
#
# This will generate a report on the status of a campaign.
# It will scan the directory with the submit scripts and
# then look for DST files and log files corresponding to
# them.
#
# Successful DST jobs will have a DST file that can be 
# opened and a "T" tree that has the expected number of 
# entries.
#
# For this to work it needs to know the locations of the
# submit scripts, DST files, logfiles, and the number of
# events per job. The JLAB/makeSLURMJobs.py and
# OSG/makeOSGJobs.py automaticaly create a file named
# submitParameters.dat in the directory where they place
# the submissions scripts. This file has a format of e.g.:
#
#  SUBMITDIR=/work/eic2/ECCE/PRODUCTION/2021.07.21.Electroweak_Djangoh_ep-10x100nc-q2-10/productions/submissionFiles/Electroweak/Djangoh/ep-10x100nc-q2-10/osgJobs
#  LOGDIR=/work/eic2/ECCE/PRODUCTION/2021.07.21.Electroweak_Djangoh_ep-10x100nc-q2-10/productions/submissionFiles/Electroweak/Djangoh/ep-10x100nc-q2-10/osgJobs/log
#  DSTDIR=/work/eic2/ECCE/MC/prop.2/c131177/Electroweak/Djangoh/ep-10x100nc-q2-10
#  EVENTS_PER_JOB=1000
#
# Run this with no arguments or by passing the name of the
# submitParameters.dat file:
#
#  ./campaignStatus.py
#
#         or
#
#  ./campaignStatus.py ../submissionFiles/*/*/*/*/submitParameters.dat
#

import os, sys, glob
import uproot

SUBMITDIR      = ''
LOGDIR         = ''
DSTDIR         = ''
EVENTS_PER_JOB = 1

# Read submit parameters from file
submitParametersFile = '/path/to/submitParameters.dat'
if len(sys.argv) > 1:
	submitParametersFile = sys.argv[1]
else:
	tmp = glob.glob('../submissionFiles/*/*/*/*/submitParameters.dat')
	if len(tmp) > 1:
		submitParametersFile = tmp[0]

if not os.path.exists( submitParametersFile ):
	print( 'No file: ' + submitParametersFile )
	sys.exit()
f = open( submitParametersFile )
for line in f.readlines():
	if line.startswith('SUBMITDIR'     ): SUBMITDIR      = line.split('=')[1].strip()
	if line.startswith('LOGDIR'        ): LOGDIR         = line.split('=')[1].strip()
	if line.startswith('DSTDIR'        ): DSTDIR         = line.split('=')[1].strip()
	if line.startswith('EVENTS_PER_JOB'): EVENTS_PER_JOB = line.split('=')[1].strip()

#----------------------------------------------------------

N_SUBMIT         = 0  # Total number of submit scripts found
N_DST_TOTAL      = 0  # Total number of DST file found in DSTDIR (possibly includes some that don't correspond to a submit script)
N_DST_SUBMITTED  = 0  # Total number of DST files with names corresponding to submit scripts
N_DST_GOOD       = 0  # Total number of DST files corresponding to submit script that could be opened and have the expected number of entries in "T"
N_TIMEOUT        = 0  # Total number of log files indicating timeout
N_DST_BAD_EVENTS = 0  # Total number of DST files that have the wrong number of events

GOOD_DST = []           # Good DST files
MISSING_DST = []        # missing root file names
MISSING_DST_SUBMIT = [] # submit scripts with missing DST files
BAD_DST = []            # DST files that exist but are not whole
BAD_DST_SUBMIT = []     # submit scripts for BAD_DST files
BAD_DST_NEVENTS = []    # DST files that have a "T" tree but wrong number of events
TIMEOUT_SUBMIT =[]      # submit scripts for jobs without good DST that timed out according to error log

# Get list of submit scripts
submit_fnames = [os.path.basename(x) for x in glob.glob( os.path.join(SUBMITDIR, '*Job_*.job') )]
N_SUBMIT = len(submit_fnames)

# Get list of DST files
dst_fnames = glob.glob( os.path.join(DSTDIR, 'DST_*.root') )
N_DST_TOTAL = len(dst_fnames)

# Loop over submit files and check corresponding DST file
print('Checking DST files ...')
for i,fsubmit in enumerate(submit_fnames):

    # Update ticker
    if i%1 == 0:
        print(' %d/%d complete ...' % (i, N_SUBMIT), end='\r')

    froot = 'DST_' + fsubmit.split('_', maxsplit=1)[1].replace('.job', '.root')
    froot_fullpath = os.path.join(DSTDIR, froot)
    if os.path.exists( froot_fullpath ):
        N_DST_SUBMITTED += 1
        try:
            f = uproot.open( froot_fullpath )
            if f['T'].fEntries == int(EVENTS_PER_JOB):
                N_DST_GOOD += 1
                GOOD_DST += [froot_fullpath]
            else:
                N_DST_BAD_EVENTS += 1  # we only get here if the "T" tree exists but has wrong entries
                BAD_DST_NEVENTS += [froot_fullpath]
                raise ValueError
        except:
            BAD_DST += [froot_fullpath]
            BAD_DST_SUBMIT += [os.path.join(SUBMITDIR, fsubmit)]
    else:
        MISSING_DST += [froot_fullpath]
        MISSING_DST_SUBMIT += [os.path.join(SUBMITDIR, fsubmit)]

    #if i>=10: break
    
print(' %d/%d complete     ' % (N_SUBMIT, N_SUBMIT) )

# Check log files for either bad or missing DST files to check for timeout
# n.b. we just check the last line of the stderr file here
print('Checking log files for jobs without good DST files ...')
logs_to_check = set( BAD_DST_SUBMIT + MISSING_DST_SUBMIT)
for i,fsubmit_fullpath in enumerate(logs_to_check):

    # Update ticker
    if i%1 == 0:
        print(' %d/%d complete ...' % (i, len(logs_to_check)), end='\r')

    fsubmit = os.path.basename(fsubmit_fullpath)
    ferr = fsubmit.replace('slurmJob_','slurm-').replace('.job', '.err')
    ferr_fullpath = os.path.join(LOGDIR, ferr)
    if os.path.exists(ferr_fullpath):
        with open(ferr_fullpath, 'rb') as fil:
            fil.seek(-200, 2)
            last_line = fil.readlines()[-1].decode("utf-8")
            if 'DUE TO TIME LIMIT' in last_line:
                N_TIMEOUT += 1
                TIMEOUT_SUBMIT += [fsubmit_fullpath]

    #if i>=30: break
print(' %d/%d complete     ' % (len(logs_to_check), len(logs_to_check)) )

#==========================================================

# Print summary
status_mess  = []
status_mess += ['\n--- SUMMARY ------------------\n']

status_mess += ['     SUBMITDIR : ' + SUBMITDIR ]
status_mess += ['        LOGDIR : ' + LOGDIR ]
status_mess += ['        DSTDIR : ' + DSTDIR ]
status_mess += ['EVENTS_PER_JOB : ' + EVENTS_PER_JOB ]
status_mess += ['\n']
status_mess += ['        N_SUBMIT: %4d  - Num. submit scripts found' % N_SUBMIT ]
status_mess += ['     N_DST_TOTAL: %4d  - Num. DST files found (good or not)' % N_DST_TOTAL ]
status_mess += [' N_DST_SUBMITTED: %4d  - Num. DST files found  (good or not) that have submit script' % N_DST_SUBMITTED ]
status_mess += ['      N_DST_GOOD: %4d  - Num. DST files that are good and have submit file' % N_DST_GOOD ]
status_mess += ['N_DST_BAD_EVENTS: %4d  - Num. DST files that have the wrong number of events' % N_TIMEOUT ]
status_mess += ['   N_DST_MISSING: %4d  - Num. DST files that are missing' % len(MISSING_DST_SUBMIT) ]
status_mess += ['       N_TIMEOUT: %4d  - Num. log files showing timeout (bad or missing DST files only)' % N_TIMEOUT ]

N_DST_BAD_EVENTS

status_mess += ['\n------------------------------\n']

print( '\n'.join(status_mess) )


# Make ouput directory to hold status reports
print( 'Writing status reports to "Status_Reports" directory ...' )
os.makedirs('Status_Reports', exist_ok=True)

# Write general summary to file
with open('Status_Reports/status_report.txt', 'w') as fil:
    fil.write( '\n'.join(status_mess) )

# Write GOOD_DST to file
with open('Status_Reports/good_DST_files.txt', 'w') as fil:
    fil.write( '# Good DST files\n')
    for f in GOOD_DST: fil.write( f + '\n')

# Write BAD_DST to file
with open('Status_Reports/bad_DST_files.txt', 'w') as fil:
    fil.write( '# DST files that are either corrupted or don\'t have correct number of entries\n')
    for f in BAD_DST: fil.write( f + '\n')

# Write BAD_DST_NEVENTS to file
with open('Status_Reports/bad_DST_nevents_files.txt', 'w') as fil:
    fil.write( '# DST files that don\'t have correct number of entries\n')
    for f in BAD_DST_NEVENTS: fil.write( f + '\n')

# Write BAD_DST_SUBMIT to file
with open('Status_Reports/bad_DST_submit_files.txt', 'w') as fil:
    fil.write( '# Submit scripts that have DST files that are either corrupted or don\'t have correct number of entries\n')
    for f in BAD_DST_SUBMIT: fil.write( f + '\n')

# Write MISSING_DST to file
with open('Status_Reports/missing_DST_files.txt', 'w') as fil:
    fil.write( '# Missing DST files\n')
    for f in MISSING_DST: fil.write( f + '\n')

# Write MISSING_DST_SUBMIT to file
with open('Status_Reports/missing_DST_submit_files.txt', 'w') as fil:
    fil.write( '# Submit scripts for which the DST files are missing\n')
    for f in MISSING_DST_SUBMIT: fil.write( f + '\n')

# Write TIMEOUT_SUBMIT to file
with open('Status_Reports/timeout_submit_files.txt', 'w') as fil:
    fil.write( '# Submit scripts that don\'t have a good DST file and whose log indicates the job timed out\n')
    for f in TIMEOUT_SUBMIT: fil.write( f + '\n')

print('Done.')

