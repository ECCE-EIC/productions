#!/usr/bin/env python3

import os, sys, math
import pytz
from dateutil import parser

#logdir = '/w/eic-sciwork18/users/davidl/2021.06.17.test_campaign/productions/submissionFiles/SIDIS/pythia6/ep_18x100/osgJobs/log'
#logdir = '/work/eic2/ECCE/MC/new/9daf451/SIDIS/pythia6+ep_18x100/log'
logdir = '/work/eic2/ECCE/MC/ana.14/5f210c7/SIDIS/pythia6/ep_18x100highq2/log'
#logdir = '/w/eic-sciwork18/users/davidl/2021.06.29.ecce_SIDIS_sample_campaign/productions/submissionFiles/SIDIS/pythia6/ep_18x100highq2/osgJobs/log'

# Find all files ending in ".out" in the specified directory 
# tree. Find the "Start time:" and "End time:" strings for each
# and convert them into a datetime in the local timezone.

job_times = []
job_starts = []
job_ends = []
for dirname,subdirname,filelist in os.walk(logdir):
	for fname in filelist:
		if not fname.endswith('.out'): continue
		
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
xmax_tdiff = 8.0
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
	for i in range( ibin_start, ibin_end ): Njobs_vs_t[i] += 1
	
	ibin = min(Nbins-1, max(0,int(tdiff/bin_width_tdiff)))
	Njobs_vs_tdiff[ibin] += 1
	
	# print('Start: %3.2f  End: %3.2f  diff: %3.2f hours' % (tstart, tend, tdiff) )


# Print full ROOT macro

print('\nvoid Njobs_vs_time(void){')

print('	double Njobs_vs_t[] = {', end='')
for v in Njobs_vs_t: print(v, end=',')
print('0};')
print('	auto hNjobs_vs_t = new TH1D("hNjobs_vs_t", ";time since campaign start (hours)", %d, %f, %f);' % (Nbins, xmin, xmax) )
print('	hNjobs_vs_t->Set(%d, Njobs_vs_t);' % Nbins)

print('	double Njobs_vs_tdiff[] = {', end='')
for v in Njobs_vs_tdiff: print(v, end=',')
print('0};')
print('	auto hNjobs_vs_tdiff = new TH1D("hNjobs_vs_tdiff", ";total job time (hours)", %d, %f, %f);' % (Nbins_tdiff, xmin_tdiff, xmax_tdiff) )
print('	hNjobs_vs_tdiff->Set(%d, Njobs_vs_tdiff);' % Nbins_tdiff)

print('	hNjobs_vs_t->SetStats(0);')
print('	hNjobs_vs_tdiff->SetStats(0);')
print('	hNjobs_vs_t->SetLineColor(kBlue);')
print('	hNjobs_vs_tdiff->SetLineColor(kMagenta);\n')

print('	auto c1 = new TCanvas("c1","");')
print('	c1->Divide(1,2);\n')

print('	c1->cd(1);')
print('	gPad->SetGrid();')
print('	hNjobs_vs_t->Draw();')
print('	c1->cd(2);')
print('	gPad->SetGrid();')
print('	hNjobs_vs_tdiff->Draw();\n')

print('	c1->SaveAs("Njobs_vs_time.png");')
print('	c1->SaveAs("Njobs_vs_time.pdf");')
print('}')




