#!/usr/bin/env python3
#
# Generate root macro for plotting job times.
#
# Run from the production directory with:
#
#  python3 extras/plot_Njobs_vs_time.py submissionFiles/*/*/*/*/submitParmaeters.dat
#

import os, sys, math, glob
import subprocess
import pytz
from dateutil import parser
from datetime import datetime

# Get list of submitParameters.dat files from command
# line. If not given, search for them.
if len(sys.argv) > 1:
    submitParametersFiles = sys.argv[1:]
else:
	if os.path.exists('./submissionFiles'):
		submitParametersFiles = glob.glob('./submissionFiles/*/*/*/*/submitParameters.dat')
	else:
		submitParametersFiles = glob.glob('../submissionFiles/*/*/*/*/submitParameters.dat')
   
if len(submitParametersFiles) == 0:
    print('No submitParameters.dat files specified or found!')
    sys.exit(-1)

print('='*100)
print('Generating reports for the following configurations:')
for f in submitParametersFiles: print('\t'+f)
print('='*100)


# Loop over submitParameters.dat files
for submitParametersFile in submitParametersFiles:

    SUBMITDIR      = ''
    LOGDIR         = ''
    DSTDIR         = ''
    EVENTS_PER_JOB = 1

    print('- '*45)
    print(submitParametersFile + '\n')

    if not os.path.exists( submitParametersFile ):
	    print( 'No file: ' + submitParametersFile )
	    continue

    print('Reading campaign parameters from:' + submitParametersFile)
    f = open( submitParametersFile )
    for line in f.readlines():
	    if line.startswith('SUBMITDIR'     ): SUBMITDIR      = line.split('=')[1].strip()
	    if line.startswith('LOGDIR'        ): LOGDIR         = line.split('=')[1].strip()
	    if line.startswith('DSTDIR'        ): DSTDIR         = line.split('=')[1].strip()
	    if line.startswith('EVENTS_PER_JOB'): EVENTS_PER_JOB = line.split('=')[1].strip()

    reaction = '_'.join(DSTDIR.split('/')[-3:])
    print( 'Using log files found in: ' + LOGDIR )

    # Determine site where campaign was run from SUBMITDIR
    SITE = ''
    if SUBMITDIR.endswith('osgJobs'  ): SITE = 'OSG'
    if SUBMITDIR.endswith('slurmJobs'): SITE = 'JLAB'
    
    # Get count of submission files
    Njobs_total = len(glob.glob(SUBMITDIR+'/*.job'))

    # Find all files ending in ".out" in the specified directory 
    # tree. Find the "Start time:" and "End time:" strings for each
    # and convert them into a datetime in the local timezone.

    job_starts = []
    job_ends = []
    job_files = []
    for dirname,subdirname,filelist in os.walk(LOGDIR):
	    for fname in filelist:
		    if not fname.endswith('.out'): continue
		    #if not fname.endswith('-eval_only.out'): continue

		    with open( os.path.join( dirname, fname) ) as f:
			    dt_start = None
			    dt_end   = None
			    #local = pytz.timezone('US/Eastern')
			    tzinfos={"CDT":"UTC-5", "PDT":"UTC-7"}  # python parser does not know CDT timezone
			    try:
				    for line in f.readlines():
					    if line.startswith('Start time:'):
						    dt_start = parser.parse( line.split('Start time:')[1], tzinfos=tzinfos).astimezone()
					    if line.startswith('End time:'):
						    dt_end = parser.parse( line.split('End time:')[1], tzinfos=tzinfos).astimezone()
			    except:
				    print('PROBLEM reading ' + os.path.join( dirname, fname))
			    if dt_start and dt_end :
				    job_starts += [dt_start]
				    job_ends   += [ dt_end ]
				    job_files  += [os.path.join( dirname, fname)]

    # Find earliest job start and latest job end
    dt_earliest = min(job_starts)
    dt_latest = max(job_ends)

    # Create array to hold histogram of job times
    xmin = 0.0;
    xmax = math.ceil((dt_latest - dt_earliest).total_seconds()/3600.0)
    Nbins = 100
    bin_width = (xmax-xmin)/(Nbins-1);
    Njobs_vs_t = [0]*Nbins


    xmin_tdiff = 0
    xmax_tdiff = 12.0
    #xmax_tdiff = 0.5
    Nbins_tdiff = 100
    bin_width_tdiff = (xmax_tdiff-xmin_tdiff)/(Nbins_tdiff-1);
    Njobs_vs_tdiff = [0]*Nbins_tdiff


    # Loop over all jobs and calculate times relative to campaign start
    for i in range( len(job_starts) ):
	    dt_start = job_starts[i]
	    dt_end   = job_ends[i]
	    tstart   = (dt_start - dt_earliest).total_seconds()/3600.0
	    tend     = (dt_end   - dt_earliest).total_seconds()/3600.0
	    tdiff    = tend - tstart

	    ibin_start = min(Nbins-1, max(0,int((tstart - xmin)/bin_width)))
	    ibin_end   = min(Nbins-1, max(0,int((tend - xmin)/bin_width)))
	    for j in range( ibin_start, ibin_end ): Njobs_vs_t[j] += 1

	    ibin = min(Nbins-1, max(0,int(tdiff/bin_width_tdiff)))
	    Njobs_vs_tdiff[ibin] += 1
        
	    # if tdiff>9 or tdiff<0.5 : print('tdiff=%3.2f : %s' % (tdiff, job_files[i]))

	    # print('Start: %3.2f  End: %3.2f  diff: %3.2f hours' % (tstart, tend, tdiff) )


    # Print full ROOT macro

    macro = []
    macro += ['\n// Generated from data scraped from log files in:']
    macro += ['// ' + LOGDIR ]

    macro += ['\nvoid Njobs_vs_time(void){']

    vals = ','.join([str(x) for x in Njobs_vs_t])
    macro += ['	double Njobs_vs_t[] = {0,' + vals + ',0};']      # include underflow and overflow bins
    macro += ['	auto hNjobs_vs_t = new TH1D("hNjobs_vs_t", ";time since campaign start (hours)", %d, %f, %f);' % (Nbins, xmin, xmax) ]
    macro += ['	hNjobs_vs_t->Set(%d, Njobs_vs_t);' % (Nbins+2)]

    vals = ','.join([str(x) for x in Njobs_vs_tdiff])
    macro += ['	double Njobs_vs_tdiff[] = {0,' + vals + ',0};']  # include underflow and overflow bins
    macro += ['	auto hNjobs_vs_tdiff = new TH1D("hNjobs_vs_tdiff", ";total job time (hours)", %d, %f, %f);' % (Nbins_tdiff, xmin_tdiff, xmax_tdiff) ]
    macro += ['	hNjobs_vs_tdiff->Set(%d, Njobs_vs_tdiff);' % (Nbins_tdiff+2)]

    macro += ['	hNjobs_vs_t->SetStats(0);']
    macro += ['	hNjobs_vs_tdiff->SetStats(0);']
    macro += ['	hNjobs_vs_t->SetLineColor(kBlue);']
    macro += ['	hNjobs_vs_tdiff->SetLineColor(kMagenta);\n']

    macro += ['	auto c1 = new TCanvas("c1","",1000, 1000);']
    macro += ['	c1->Divide(1,2);\n']

    macro += ['	c1->cd(1);']
    macro += ['	gPad->SetGrid();']
    macro += ['	hNjobs_vs_t->Draw();']
    macro += ['	c1->cd(2);']
    macro += ['	gPad->SetGrid();']
    macro += ['	hNjobs_vs_tdiff->Draw();\n']

    macro += ['	// Draw job parameters on plot']
    macro += ['	c1->Draw(); // needed for xmid to be correct (why I don\'t know ??)']
    macro += ['	c1->cd(1);']
    macro += ['	auto xmid = (gPad->GetX1()+gPad->GetX2())/2.0;']
    macro += ['	auto ymax = gPad->GetY2();']
    macro += ['	auto latex = new TLatex();']
    macro += ['	latex->SetTextSize(0.040);']
    macro += ['	latex->SetTextAlign(11);']
    macro += ['	latex->DrawLatex(0.0, ymax*0.95, "' + LOGDIR + '");']

    macro += ['	latex->SetTextSize(0.060);']
    macro += ['\n	latex->DrawLatex( 1.5*xmid, 0.75*ymax, "' + SITE + '");']
    macro += ['\n	c1->cd(2);']
    macro += ['	auto xmid2 = (gPad->GetX1()+gPad->GetX2())/2.0;']
    macro += ['	auto ymax2 = gPad->GetY2();']
    macro += ['\n	latex->DrawLatex( 1.5*xmid2, 0.75*ymax2, "' + SITE + '");']
    macro += ['\n	char str[256];']
    macro += ['	sprintf(str, "%d/%d = %3.1f%%%% of jobs");' % (len(job_starts), Njobs_total, 100.0*float(len(job_starts))/float(Njobs_total) )]
    macro += ['	latex->SetTextSize(0.040);']
    macro += ['	latex->DrawLatex( 1.25*xmid2, 0.70*ymax2, str);']

    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    macro += ['\n	c1->cd(1);']
    macro += ['	auto xmax = gPad->GetX2();']
    macro += ['	latex->SetTextSize(0.030);']
    macro += ['	latex->SetTextAlign(33);']
    macro += ['	latex->DrawLatex( xmax, ymax, "' + date_time + '");']

    macro += ['\n	// Save to files']
    macro += ['	c1->SaveAs("Njobs_vs_time_%s.png");' % reaction]
    macro += ['	c1->SaveAs("Njobs_vs_time_%s.pdf");' % reaction]
    macro += ['}']

    # Make ouput directory to hold status reports if it doesn't already exist
    statusReportsDir = 'Status_Reports/'+reaction
    if not os.path.exists(statusReportsDir): os.makedirs(statusReportsDir, exist_ok=True)
    print( 'Writing macro to "%s" directory ...' % statusReportsDir )

    with open(statusReportsDir+'/Njobs_vs_time.C', 'w') as fil:
        fil.write( '\n'.join(macro) )
    print('\nWrote macro to file: '+statusReportsDir+'/Njobs_vs_time.C')
    savedir = os.getcwd()
    print('cd '+statusReportsDir)
    os.chdir(statusReportsDir)
    print('Running macro ...')
    cmd = ['root', '-q', '-b', '-l', 'Njobs_vs_time.C']
    print(' '.join(cmd))
    subprocess.call(cmd)
    print('cd '+savedir)
    os.chdir(savedir)

