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
import sys, os
from os import environ
from ROOT import TFile, TObjString

# macrosDir         : full path to macros directory, ending with ".../macros"
# generatedDir      : should be top level corresponding to generated events location e.g. /gpfs/mnt/gpfs02/eic/ on SDCC gpfs
# simulationsTopDir : top of output directory tree for DST and eval files
macrosDir         = '/work/eic/users/davidl/2021.06.11.ecce_jlab_test_campaign/macros'
generatedTopDir   = 'root://sci-xrootd.jlab.org//osgpool/eic'
outputDest        = '/u/scratch/davidl/2021.06.11.ecce_jlab_test_campaign'
simulationsTopDir = 'DST_files'

nArgs = len(sys.argv)
if nArgs != 5:
    print("Usage: python makeOSGJob <nEventsPerJob> <physics WG> <generator> <collision>")
    sys.exit()

myShell='/bin/bash'
#myShell = str(environ['SHELL'])
#goodShells = ['/bin/bash', '/bin/tcsh']
#if myShell not in goodShells:
#    print("Your shell {} was not recognised".format(myShell))
#    sys.exit()


nEventsPerJob = int(sys.argv[1])

thisWorkingGroup = sys.argv[2]
ecceWorkingGroup = ['SIDIS', 'HFandJets', 'ExclusiveReactions']
if thisWorkingGroup not in ecceWorkingGroup:
    print("Physics WG: {} was not recognised".format(thisWorkingGroup))
    sys.exit()
else:
    print("Physics WG: {}".format(thisWorkingGroup))


thisGenerator = sys.argv[3]
ecceGenerator = ['pythia6', 'pythia8']
if thisGenerator not in ecceGenerator:
    print("Generator: {} was not recognised".format(thisGenerator))
    sys.exit()
else:
    print("Generator: {}".format(thisGenerator))


thisCollision = sys.argv[4]
ecceCollision = ['ep_10x100', 'ep_18x100', 'ep_18x275']
if thisCollision not in ecceCollision:
    print("Collision: {} was not recognised".format(thisCollision))
    sys.exit()
else:
    print("Collision: {}".format(thisCollision))


def getNumEvtsInFile(theFile):
    # For some reason pyroot is failing when using xrootd so if 
	 # that is being used, try accessing the file through the filesystem
    if '.jlab.org//osgpool' in theFile:
        theFile = '/work/osgpool' + theFile.split('.jlab.org//osgpool')[1]
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeOSGJob(PWG):
    print("Creating OSG condor submission files for {} production".format(PWG))
    #Find and open the PWG list of input event files
    inputFileList = "eic-smear_{}_{}_{}.list".format(PWG, thisGenerator, thisCollision)
    infile = open(inputFileList, "r")
    line = infile.readline()
    if not line.startswith('/') : line = generatedTopDir + '/' + line
    #Get the current working directory to write submissions and logs to
    myOutputPath = os.getcwd().replace('/w/eic-sciwork18', '/work/eic')
    osgDir = "{}/osgJobs".format(myOutputPath)
    os.makedirs("{}/log".format(osgDir), exist_ok=True)
    submitScriptName = "{}/submitJobs.sh".format(osgDir)
    submitScript = open("{}".format(submitScriptName), "w")
    os.chmod(submitScriptName, 0o744)
    submitScript.write("#!{}\n".format(myShell))
    #Now make output directory (plus eval folder)
    outputPath = "{}/{}/{}/{}".format(simulationsTopDir, thisWorkingGroup, thisGenerator, thisCollision)
    outputEvalPath = outputPath + "/eval"
    os.makedirs(outputPath, exist_ok=True)
    os.makedirs(outputEvalPath, exist_ok=True)
    #Print input/output info
    print("Input file list: {}".format(inputFileList))
    print("Output directory: {}".format(outputPath))
    #Now loop over all input trees and make a submission script that fits the request
    nJobs = 0
    while line:
       inputFile = line.replace("\n", "")
       nEventsInFile = getNumEvtsInFile(inputFile)
       nJobsFromFile = math.ceil(nEventsInFile/nEventsPerJob)
       for i in range(nJobsFromFile):

            jobNumber = nJobs
            skip = i*nEventsPerJob

            osgOutputInfo = "{0}/log/osg-{1}_{2}_{3}-{4:05d}".format(osgDir, PWG, thisGenerator, thisCollision, jobNumber)

            outputFile = "DST_{}_{}_{}-{:05d}.root".format(PWG, thisGenerator, thisCollision, jobNumber)
            argument = "{} {} {} {} {}".format(nEventsPerJob, inputFile, outputFile, skip, outputPath)

            osgFileName = "osgJob_{0}_{1}_{2}-{3:05d}.job".format(PWG, thisGenerator, thisCollision, jobNumber)
            osgFile = open("{0}/{1}".format(osgDir, osgFileName), "w")

            #osgFile.write("JOB_NAME       = ecce-osg-{0}_{1}_{2}-{3:05d}\n".format(PWG, thisGenerator, thisCollision, jobNumber))
            osgFile.write("\n")
            osgFile.write("executable     = ecce_osg.sh\n")
            osgFile.write("arguments      = run_EIC_production.sh " + outputDest + " " + argument + "\n")
            osgFile.write("request_cpus   = 1\n")
            osgFile.write("request_memory = 2 GB\n")
            osgFile.write("request_disk   = 3 GB\n")
            osgFile.write("\n")
            osgFile.write("should_transfer_files  = YES\n")
            osgFile.write("transfer_input_files   = " + macrosDir + ",copy_to_S3.sh\n")
            if outputDest.startswith('/'):
                osgFile.write("transfer_output_files  = " + simulationsTopDir + "\n")
                osgFile.write("transfer_output_remaps = \"%s=%s\"\n" % (simulationsTopDir, os.path.join(outputDest, simulationsTopDir)))
            osgFile.write("error  = {}.err\n".format(osgOutputInfo))
            osgFile.write("output = {}.out\n".format(osgOutputInfo))
            osgFile.write("log    = {}.log\n".format(osgOutputInfo))
            osgFile.write("\n")
            osgFile.write("#------------------------------------------------------------------\n")
            osgFile.write("\n")
            osgFile.write("Requirements = (HAS_SINGULARITY == TRUE) && (HAS_CVMFS_oasis_opensciencegrid_org == True) && (SINGULARITY_MODE == \"privileged\") &&  (HAS_CVMFS_sphenix_opensciencegrid_org == True) && (Arch == \"X86_64\")\n")
            osgFile.write("\n")
            osgFile.write("+ProjectName = \"EIC\"\n")
            osgFile.write("+SingularityImage = \"/cvmfs/oasis.opensciencegrid.org/jlab/epsci/singularity/images/rhic_sl7_ext_S3.simg\"\n")
            osgFile.write("+SingularityBindCVMFS = True\n")
            osgFile.write("+SingularityAutoLoad  = True\n")
            osgFile.write("#+DESIRED_Sites=\"JLab-FARM-CE\"\n")
            osgFile.write("\n")
            osgFile.write("queue 1\n")

            submitScript.write("condor_submit {}\n".format(osgFileName))

            nJobs += 1
       line = infile.readline()

    print("OSG submission files have been written to:\n{}/osgJobs".format(myOutputPath))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeOSGJob(thisWorkingGroup)
