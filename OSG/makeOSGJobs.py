#
#  6/9/2021  David Lawrence  davidl@jlab.org
#
# This requires root with python support.
# To do this on the JLab ifarm once could
#  e.g.
#
#   source /apps/root/6.18.04/setroot_CUE.bash
#
#
# Run this with something like:
#
#  python3 ./macros/detectors/EICDetector/makeOSGJobs.py 1000000 SIDIS pythia6 ep_18x100
#
# n.b. The generated submitJobs.sh script should be
# run on either scosg16.jlab.org or scosg20.jlab.org
#

import math
import sys, os, subprocess, glob
from os import environ
from ROOT import TFile, TObjString

# This is used to map the full path file names in the list of
# generated files that are on the BNL system to paths on the
# JLab system.
generatedDirNameMap = {	'/gpfs/mnt/gpfs02/eic':'root://sci-xrootd.jlab.org//osgpool/eic',
								'/work/osgpool/eic'   :'root://sci-xrootd.jlab.org//osgpool/eic'}

nArgs = len(sys.argv)
if nArgs != 13:
    print("Usage: python makeOSGJobs.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite> <macrosBranch> <nTotalEvents>")
    sys.exit()

myShell='/bin/bash'

# Path variable descriptions
#
# simulationsTopDir : Directory where output DST files should go
# submitPath        : Directory where the SLURM batch scripts are written
# macrosPath        : Directory where the Fun4All_G4_EICDetector.C lives (e.g. .../macros/detector/EICDetector)
# macrosTopDir      : Directory "macros". (This is just <macrosPath>/../..)
# prodTopDir        : Directory where setProduction.py is being run from (typically "productions")

class pars:
  #simulationsTopDir = '/sphenix/user/cdean/ECCE/MC'
  #simulationsTopDir = 'S3://eictest/ECCE/MC'
  simulationsTopDir = '/work/eic2/ECCE/MC'
  nEventsPerJob = int(sys.argv[1])
  thisWorkingGroup = sys.argv[2]
  thisGenerator = sys.argv[3]
  thisCollision = sys.argv[4]
  build = sys.argv[5]
  submitPath = sys.argv[6]
  macrosPath = sys.argv[7]
  macrosTopDir = os.path.abspath( macrosPath + '/../..')
  macrosTarball = glob.glob(macrosTopDir + '*.tgz')[0]  # assume setupProduction.py made one (and only one) tarball
  prodTopDir = sys.argv[8]
  macrosHash = sys.argv[9]
  prodSite = sys.argv[10]
  macrosBranch = sys.argv[11]
  nTotalEvents = int(sys.argv[12])

def getNumEvtsInFile(theFile):
    # For some reason pyroot is failing when using xrootd so if 
	 # that is being used, try accessing the file through the filesystem
    if '.jlab.org//osgpool' in theFile:
        theFile = '/work/osgpool' + theFile.split('.jlab.org//osgpool')[1]
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeOSGJob():
    print("Creating OSG condor submission files for {} production".format(pars.thisWorkingGroup))

    # If writing to S3 then make sure the copy_to_s3.py script exists
    if pars.simulationsTopDir.startswith('S3://'):
        if not os.path.exists('copy_to_S3.py'):
            print('\nERROR: ==========================================================')
            print('pars.simulationsTopDir specifies writing to S3 but the')
            print('copy_to_S3.py script does not exist in the current directory!')
            print('Make sure the file exists here and has been modified to')
            print('include an accessKey and secretKey with write privileges.')
            print('==================================================================\n')
            sys.exit()

    #Find and open the pars.thisWorkingGroup list of input event files
    inputFileList = "{}/{}/inputFileLists/{}_{}_{}.list".format(pars.prodTopDir, 
                                                                pars.prodSite,
                                                                pars.thisWorkingGroup, 
                                                                pars.thisGenerator, 
                                                                pars.thisCollision)
    infile = open(inputFileList, "r")
    line = infile.readline()
    for key,val in generatedDirNameMap.items(): line = line.replace(key, val)

    # Set directory to write submission scripts and logs to
    osgDir = "{}/osgJobs".format(pars.submitPath) 
    os.makedirs("{}/log".format(osgDir), exist_ok=True)
    submitScriptName = "{}/submitJobs.sh".format(osgDir)
    submitScript = open("{}".format(submitScriptName), "w")
    os.chmod(submitScriptName, 0o744)
    submitScript.write("#!{}\n".format(myShell))

    # Portion of output directory path relative to top-level simulations output dir
    outputRelPath = "{}/{}/{}/{}/{}".format(pars.build,
                                            pars.macrosHash,
                                            pars.thisWorkingGroup,
                                            pars.thisGenerator,
                                            pars.thisCollision)

    # Copy the topmost directory of the outputRelPath to its own variable.
    outputRelPathTopDirName = outputRelPath.split('/')[0]

    # Full path to directory where DST files will be written. (n.b. this may start with "S3://")
    outputPath = "{}/{}".format(pars.simulationsTopDir, outputRelPath)

    # Log files must always be local
    outputLogPath  = outputPath + "/log"
    os.makedirs(outputLogPath, exist_ok=True)
	 
	 # Write key campaign parameters to submitParameters.dat file
	 parmsFile = os.path.join( osgDir, 'submitParameters.dat' )
	 with open( parmsFile, 'w' ) as fparms:
	 	fparms.write( 'SUBMITDIR=%s\n' % osgDir )
	 	fparms.write( 'LOGDIR=%s\n' % outputLogPath)
	 	fparms.write( 'DSTDIR=%s\n' % outputPath)
	 	fparms.write( 'EVENTS_PER_JOB=%d\n' % pars.nEventsPerJob )
		fparms.close()

    # Print input/output info
    print("Input file list: {}".format(inputFileList))
    print("Output directory: {}".format(outputPath))

    # Now loop over all input trees and make a submission script that fits the request
    nJobs = 0
    fileNumber = 0
    while line:
       for key,val in generatedDirNameMap.items(): line = line.replace(key, val)
       inputFile = line.replace("\n", "")
       nEventsInFile = getNumEvtsInFile(inputFile)
       nJobsFromFile = math.ceil(nEventsInFile/pars.nEventsPerJob)
       for i in range(nJobsFromFile):

            jobNumber = nJobs
            skip = i*pars.nEventsPerJob
       
            nEvents = nJobs*pars.nEventsPerJob
            if nEvents >= pars.nTotalEvents: break

            fileTag = "{0}_{1}_{2}_{3:03d}_{4:07d}_{5:05d}".format(pars.thisWorkingGroup,
                                                                   pars.thisGenerator,
                                                                   pars.thisCollision,
                                                                   fileNumber,
                                                                   skip,
                                                                   pars.nEventsPerJob)

            osgOutputInfo = "{0}/osg-{1}".format(outputLogPath, fileTag)

            outputFile = "DST_{}.root".format(fileTag)
            argument = "{} {} {} {} {} {} {} {} {} {} {} {}".format(pars.nEventsPerJob,
                                                                    inputFile,
                                                                    outputFile,
                                                                    skip,
                                                                    outputRelPath, #outputPath,
                                                                    pars.build,
                                                                    pars.thisWorkingGroup,
                                                                    pars.macrosHash,
                                                                    pars.prodSite,
                                                                    pars.thisGenerator,
                                                                    pars.thisCollision,
                                                                    pars.macrosBranch)

            osgFileName = "osgJob_{}.job".format(fileTag)

            osgFile = open("{0}/{1}".format(osgDir, osgFileName), "w")
            
            transfer_input_files = pars.macrosTarball + "," + pars.prodTopDir
            if pars.simulationsTopDir.startswith('S3://'):
                transfer_input_files += ',copy_to_S3.py'

            osgFile.write("\n")
            osgFile.write("executable     = " + pars.prodTopDir + "/OSG/ecce_osg.sh\n")
            osgFile.write("arguments      = run_EIC_production.sh " + pars.simulationsTopDir + " " + argument + "\n")
            osgFile.write("request_cpus   = 1\n")
            osgFile.write("request_memory = 2 GB\n")
            osgFile.write("request_disk   = 3 GB\n")
            osgFile.write("\n")
            osgFile.write("should_transfer_files  = YES\n")
            osgFile.write("transfer_input_files   = " + transfer_input_files + "\n")
            if outputPath.startswith('/'):
                osgFile.write("transfer_output_files  = %s\n" % outputRelPathTopDirName)
                osgFile.write("transfer_output_remaps = \"%s=%s\"\n" % (outputRelPathTopDirName, os.path.join(pars.simulationsTopDir,outputRelPathTopDirName)))
            osgFile.write("error  = {}.err\n".format(osgOutputInfo))
            osgFile.write("output = {}.out\n".format(osgOutputInfo))
            osgFile.write("log    = {}.log\n".format(osgOutputInfo))
            osgFile.write("\n")
            osgFile.write("#------------------------------------------------------------------\n")
            osgFile.write("\n")
            osgFile.write("Requirements = (HAS_SINGULARITY == TRUE) && (HAS_CVMFS_oasis_opensciencegrid_org == True) && (SINGULARITY_MODE == \"privileged\") &&  (HAS_CVMFS_sphenix_opensciencegrid_org == True) && (Arch == \"X86_64\")\n")
            osgFile.write("\n")
            osgFile.write("+ProjectName = \"EIC\"\n")
            osgFile.write("+SingularityImage = \"/cvmfs/eic.opensciencegrid.org/singularity/rhic_sl7_ext\"\n")
            osgFile.write("+SingularityBindCVMFS = True\n")
            osgFile.write("+SingularityAutoLoad  = True\n")
            osgFile.write("#+DESIRED_Sites=\"JLab-FARM-CE\"\n")
            osgFile.write("\n")
            osgFile.write("queue 1\n")
            osgFile.close()

            submitScript.write("condor_submit {}/{}\n".format(osgDir, osgFileName))

            nJobs += 1
       if nEvents >= pars.nTotalEvents: 
           submitScript.close()
           break
       fileNumber += 1
       line = infile.readline()

    print("OSG submission files have been written to:\n{}".format(osgDir))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeOSGJob()
