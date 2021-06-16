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

# macrosDir         : full path to macros directory, ending with ".../macros"
# generatedDir      : should be top level corresponding to generated events location e.g. /gpfs/mnt/gpfs02/eic/ on SDCC gpfs
# simulationsTopDir : top of output directory tree for DST and eval files
macrosDir         = '/work/eic/users/davidl/2021.06.11.ecce_jlab_test_campaign/macros'
generatedTopDir   = '/work/osgpool/eic'
simulationsTopDir = '/volatile/eic/davidl/2021.06.11.ecce_jlab_test_campaign/DST_files'

nArgs = len(sys.argv)
if nArgs != 11:
    print("Usage: python makeSLURMJob.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite>")
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
    if not line.startswith('/') : line = generatedTopDir + '/' + line
    #Get the current working directory to write submissions and logs to
    myOutputPath = os.getcwd().replace('/w/eic-sciwork18', '/work/eic')
    slurmDir = "{}/slurmJobs".format(myOutputPath)
    os.makedirs("{}/log".format(slurmDir), exist_ok=True)
    submitScriptName = "{}/submitJobs.sh".format(slurmDir)
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

            slurmOutputInfo = "{0}/log/slurm-{1}".format(slurmDir, fileTag)

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
            slurmFile.write("cp -rp " + macrosDir + " .\n")
            slurmFile.write("cd macros/detectors/EICDetector\n")
            slurmFile.write("\n")
            slurmFile.write("singularity exec --no-home -B /cvmfs:/cvmfs ${SIMG} ${SCRIPT} " + argument + "\n")
            slurmFile.write("echo \n")
            slurmFile.write("echo \"----------------------------------------------\"\n")
            slurmFile.write("cd ..\n")
            slurmFile.write("rm -rf workdir_${SLURM_JOBID}\n")
            slurmFile.write("printf \"End time: \"; /bin/date\n")

            submitScript.write("sbatch {}\n".format(slurmFileName))

            nJobs += 1
       fileNumber += 1
       line = infile.readline()

    print("SLURM submission files have been written to:\n{}/slurmJobs".format(myOutputPath))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeSLURMJob()
