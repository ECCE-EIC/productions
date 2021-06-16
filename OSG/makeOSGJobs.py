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
import sys, os, subprocess
from os import environ
from ROOT import TFile, TObjString

# productionSite    : used for recording metadata. This is always OSG@JLab for this script
# release           : nightly build version to use. default is "new" (don't ask)
# macrosDir         : full path to macros directory, ending with ".../macros"
# generatedDir      : should be top level corresponding to generated events location e.g. /gpfs/mnt/gpfs02/eic/ on SDCC gpfs
# simulationsTopDir : top of output directory tree for DST and eval files
productionSite    = 'OSG@JLab'
release           = 'new'
macrosDir         = '/work/eic/users/davidl/2021.06.15.ecce_test_campaign/macros'
productionsDir    = '/work/eic/users/davidl/2021.06.15.ecce_test_campaign/productions'
generatedTopDir   = 'root://sci-xrootd.jlab.org//osgpool/eic'
outputDest        = '/u/scratch/davidl/2021.06.15.ecce_test_campaign'
simulationsTopDir = 'DST_files'

nArgs = len(sys.argv)
if nArgs != 11:
    print("Usage: python makeOSGJob.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite>")
    sys.exit()

myShell='/bin/bash'

class pars:
  simulationsTopDir = '/sphenix/user/cdean/ECCE/MC'
  nEventsPerJob = int(sys.argv[1])
  thisWorkingGroup = sys.argv[2]
  thisGenerator = sys.argv[3]
  thisCollision = sys.argv[4]
  build = sys.argv[5]
  submitPath = sys.argv[6]
  macrosPath = sys.argv[7]
  prodTopDir = sys.argv[8]
  macrosHash = sys.argv[9]
  prodSite = sys.argv[10]

# Automatically extract macros branch name and hash from the specified directory
#macrosBranch = subprocess.Popen(['git', '-C', macrosDir, 'branch', '--points-at', 'HEAD'], stdout=subprocess.PIPE).communicate()[0].split()[-1].decode().strip()
#pars.macrosHash = subprocess.Popen(['git', '-C', macrosDir, 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE).communicate()[0].decode().strip()

def getNumEvtsInFile(theFile):
    # For some reason pyroot is failing when using xrootd so if 
	 # that is being used, try accessing the file through the filesystem
    if '.jlab.org//osgpool' in theFile:
        theFile = '/work/osgpool' + theFile.split('.jlab.org//osgpool')[1]
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeOSGJob():
    print("Creating OSG condor submission files for {} production".format(pars.thisWorkingGroup))
    #Find and open the pars.thisWorkingGroup list of input event files
    inputFileList = "{}/inputFileLists/eic-smear_{}_{}_{}.list".format(pars.prodTopDir,
                                                                       pars.thisWorkingGroup,
                                                                       pars.thisGenerator,
                                                                       pars.thisCollision)
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
    outputPath = "{}/{}/{}/{}/{}+{}".format(pars.simulationsTopDir,
                                            pars.build,
                                            pars.macrosHash,
                                            pars.thisWorkingGroup,
                                            pars.thisGenerator,
                                            pars.thisCollision)
    outputEvalPath = outputPath + "/eval"
    os.makedirs(outputPath, exist_ok=True)
    os.makedirs(outputEvalPath, exist_ok=True)
    #Print input/output info
    print("Input file list: {}".format(inputFileList))
    print("Output directory: {}".format(outputPath))
    #Now loop over all input trees and make a submission script that fits the request
    nJobs = 0
    fileNumber = 0
    while line:
       inputFile = line.replace("\n", "")
       nEventsInFile = getNumEvtsInFile(inputFile)
       nJobsFromFile = math.ceil(nEventsInFile/pars.nEventsPerJob)
       for i in range(nJobsFromFile):

            jobNumber = nJobs
            skip = i*pars.nEventsPerJob

            fileTag = "{0}_{1}_{2}_{3:03d}_{4:07d}_{5:04d}".format(pars.thisWorkingGroup,
                                                                   pars.thisGenerator,
                                                                   pars.thisCollision,
                                                                   fileNumber,
                                                                   skip,
                                                                   pars.nEventsPerJob)

            osgOutputInfo = "{0}/log/osg-{1}".format(osgDir, fileTag)

            outputFile = "DST_{}.root".format(fileTag)
            argument = "{} {} {} {} {} {} {} {} {} {} {}".format(pars.nEventsPerJob,
                                                                 inputFile,
                                                                 outputFile,
                                                                 skip,
                                                                 outputPath,
                                                                 pars.build,
                                                                 pars.thisWorkingGroup,
                                                                 pars.macrosHash,
                                                                 pars.prodSite,
                                                                 pars.thisGenerator,
                                                                 pars.thisCollision)

            osgFileName = "osgJob_{}.job".format(fileTag)

            osgFile = open("{0}/{1}".format(osgDir, osgFileName), "w")

            #osgFile.write("JOB_NAME       = ecce-osg-{0}_{1}_{2}-{3:05d}\n".format(PWG, thisGenerator, thisCollision, jobNumber))
            osgFile.write("\n")
            osgFile.write("executable     = " + productionsDir + "/OSG/ecce_osg.sh\n")
            osgFile.write("arguments      = run_EIC_production.sh " + outputDest + " " + argument + "\n")
            osgFile.write("request_cpus   = 1\n")
            osgFile.write("request_memory = 2 GB\n")
            osgFile.write("request_disk   = 3 GB\n")
            osgFile.write("\n")
            osgFile.write("should_transfer_files  = YES\n")
            osgFile.write("transfer_input_files   = copy_to_S3.sh," + macrosDir + "," + productionsDir + "\n")
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
       fileNumber += 1
       line = infile.readline()

    print("OSG submission files have been written to:\n{}/osgJobs".format(myOutputPath))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeOSGJob()
