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
#  python3 ./macros/detectors/EICDetector/makeSLURMJobs.py 1000000 SIDIS pythia6 ep_18x100
#

import math
import sys, os, getpass
from os import environ
from ROOT import TFile, TObjString

# This is used to map the full path file names in the list of
# generated files that are on the BNL system to paths on the
# JLab system.
generatedDirNameMap = {'/gpfs/mnt/gpfs02/eic':'/work/osgpool/eic'}

nArgs = len(sys.argv)
if nArgs != 13:
    print("Usage: python makeSLURMJob.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite> <macrosBranch> <nTotalEvents>")
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
  simulationsTopDir = '/work/eic2/ECCE/MC'
  nEventsPerJob = int(sys.argv[1])
  thisWorkingGroup = sys.argv[2]
  thisGenerator = sys.argv[3]
  thisCollision = sys.argv[4]
  build = sys.argv[5]
  submitPath = sys.argv[6]
  macrosPath = sys.argv[7]
  macrosTopDir = os.path.abspath( macrosPath + '/../..')
  prodTopDir = sys.argv[8]
  macrosHash = sys.argv[9]
  prodSite = sys.argv[10]
  macrosBranch = sys.argv[11]
  nTotalEvents = int(sys.argv[12])


def getNumEvtsInFile(theFile):
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeSLURMJob():
    print("Creating SLURM submission files for {} production".format(pars.thisWorkingGroup))
    #Find and open the PWG list of input event files
    inputFileList = "{}/inputFileLists/eic-smear_{}_{}_{}.list".format(pars.prodTopDir,
                                                                       pars.thisWorkingGroup,
                                                                       pars.thisGenerator,
                                                                       pars.thisCollision)
    infile = open(inputFileList, "r")
    line = infile.readline()
    for key,val in generatedDirNameMap.items(): line = line.replace(key, val)
    #Get the current working directory to write submissions and logs to
    #myOutputPath = os.getcwd().replace('/w/eic-sciwork18', '/work/eic')
    slurmDir = "{}/slurmJobs".format(pars.submitPath)
    submitScriptName = "{}/submitJobs.sh".format(slurmDir)
    submitScript = open("{}".format(submitScriptName), "w")
    os.chmod(submitScriptName, 0o744)
    submitScript.write("#!{}\n".format(myShell))
    #Now make output directory
    outputPath = "{}/{}/{}/{}/{}/{}".format(pars.simulationsTopDir,
                                            pars.build,
                                            pars.macrosHash,
                                            pars.thisWorkingGroup,
                                            pars.thisGenerator,
                                            pars.thisCollision)
    outputLogPath  = outputPath + "/log"
    os.makedirs(outputPath, exist_ok=True)
    os.makedirs(outputLogPath, exist_ok=True)
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
       
            nEvents = nJobs*pars.nEventsPerJob
            if nEvents >= pars.nTotalEvents: break

            fileTag = "{0}_{1}_{2}_{3:03d}_{4:07d}_{5:05d}".format(pars.thisWorkingGroup,
                                                                   pars.thisGenerator,
                                                                   pars.thisCollision,
                                                                   fileNumber,
                                                                   skip,
                                                                   pars.nEventsPerJob)

            slurmOutputInfo = "{0}/slurm-{1}".format(outputLogPath, fileTag)

            outputFile = "DST_{}.root".format(fileTag)
            argument = "{} {} {} {} {} {} {} {} {} {} {} {}".format(pars.nEventsPerJob,
                                                                    inputFile,
                                                                    outputFile,
                                                                    skip,
                                                                    outputPath,
                                                                    pars.build,
                                                                    pars.thisWorkingGroup,
                                                                    pars.macrosHash,
                                                                    pars.prodSite,
                                                                    pars.thisGenerator,
                                                                    pars.thisCollision,
                                                                    pars.macrosBranch)

            slurmFileName = "slurmJob_{}.job".format(fileTag)
            slurmFile = open("{0}/{1}".format(slurmDir, slurmFileName), "w")				
            slurmFile.write("#!/bin/bash\n")
            slurmFile.write("#\n")
            slurmFile.write("#SBATCH --account=eic\n")
            slurmFile.write("#SBATCH --nodes=1\n")
            slurmFile.write("#SBATCH --ntasks=1\n")
            slurmFile.write("#SBATCH --mem-per-cpu=2000\n")
            slurmFile.write("#SBATCH --job-name=slurm-{0}\n".format(fileTag))
            slurmFile.write("#SBATCH --time=05:30:00\n")
            slurmFile.write("#SBATCH --gres=disk:10000\n")
            slurmFile.write("#SBATCH --output=" + slurmOutputInfo + ".out\n")
            slurmFile.write("#SBATCH --error=" + slurmOutputInfo + ".err\n")
            slurmFile.write("#SBATCH --chdir=/u/scratch/" + getpass.getuser() + "\n")
            slurmFile.write("#\n")
            slurmFile.write("\n")
            slurmFile.write("printf \"Start time: \"; /bin/date\n")
            slurmFile.write("printf \"host: \"; /bin/hostname -A\n")
            slurmFile.write("printf \"user: \"; /usr/bin/id\n")
            slurmFile.write("printf \"cwd: \"; /bin/pwd\n")
            slurmFile.write("printf \"os: \"; /bin/lsb_release -a\n")
            slurmFile.write("echo \n")
            slurmFile.write("echo \"----------------------------------------------\"\n")
            slurmFile.write("echo \n")
            slurmFile.write("SIMG=/cvmfs/eic.opensciencegrid.org/singularity/rhic_sl7_ext\n")
            slurmFile.write("SCRIPT=./run_EIC_production.sh\n")
            slurmFile.write("\n")
            slurmFile.write("# JLab creates a strange alias for \"module\" in login scripts\n")
            slurmFile.write("# The following should be equivalent to:\n")
            slurmFile.write("#  module load /apps/modulefiles/singularity/3.4.0\n")
            slurmFile.write("eval `/usr/bin/modulecmd bash load /apps/modulefiles/singularity/3.4.0`\n")
            slurmFile.write("\n")
            slurmFile.write("# Create and cd to dedicated working directory\n")
            slurmFile.write("mkdir -p workdir_${SLURM_JOBID}\n")
            slurmFile.write("cd workdir_${SLURM_JOBID}\n")
            slurmFile.write("printf \"cwd: \"; /bin/pwd\n")
            slurmFile.write("\n")
            slurmFile.write("# Copy entire macros directory to local disk\n")
            slurmFile.write("cp -rp " + pars.macrosTopDir + " .\n")
            slurmFile.write("cd macros/detectors/EICDetector\n")
            slurmFile.write("\n")
            slurmFile.write("singularity exec --no-home -B /cvmfs:/cvmfs ${SIMG} ${SCRIPT} " + argument + "\n")
            slurmFile.write("echo \n")
            slurmFile.write("echo \"----------------------------------------------\"\n")
            slurmFile.write("cd ..\n")
            slurmFile.write("rm -rf workdir_${SLURM_JOBID}\n")
            slurmFile.write("printf \"End time: \"; /bin/date\n")
            slurmFile.close()

            submitScript.write("sbatch {}\n".format(slurmFileName))

            nJobs += 1
       if nEvents >= pars.nTotalEvents: 
           submitScript.close()
           break
       fileNumber += 1
       line = infile.readline()

    print("SLURM submission files have been written to:\n{}".format(slurmDir))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeSLURMJob()
