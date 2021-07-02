#
# This requires root with python support.
# To do this on the JLab ifarm once could
#  e.g.
#
#   source /apps/root/6.18.04/setroot_CUE.bash
#
#
# This script should be modified so values in the class "pars"
# contain the parameters for the job. Then run it like this:
#
#  python3 ./macros/detectors/EICDetector/makeSLURMJobsUser.py
#

import math
import sys, os, getpass, shutil
from os import environ
from ROOT import TFile, TObjString

# MYDIR          : Directory where campaign is being run from (DST and log directories will be created here)
# inputFileList  : File containing list of EICsmear formatted generated events files
# macrosTopDir   : Directory "macros". (This is should contain "detectors/EICDetector/Fun4All_G4_EICDetector.C")
# nEventsPerJob  : Jobs will be broken up into this many events per job
# nTotalEvents   : Maximum number of events to process when summing all jobs.

class pars:
    MYDIR='/work/eic2/ECCE/users/davidl/2021.07.02.incl_highq2_xiaochao'
    inputFileList='generated_events_files.list'
    macrosTopDir='macros'
    nEventsPerJob=1000
    nTotalEvents=2
    


# This is used to map the full path file names in the list of
# generated files that are on the BNL system to paths on the
# JLab system.
#generatedDirNameMap = {'/gpfs/mnt/gpfs02/eic':'/work/osgpool/eic'}

nArgs = len(sys.argv)
if nArgs != 1:
    print("Usage: python3 makeSLURMJob.py")
    sys.exit()

#myShell='/bin/bash'

# Path variable descriptions
#
# simulationsTopDir : Directory where output DST files should go
# submitPath        : Directory where the SLURM batch scripts are written
# macrosPath        : Directory where the Fun4All_G4_EICDetector.C lives (e.g. .../macros/detector/EICDetector)
# macrosTopDir      : Directory "macros". (This is just <macrosPath>/../..)
# prodTopDir        : Directory where setProduction.py is being run from (typically "productions")

#class pars:
#  simulationsTopDir = '/work/eic2/ECCE/MC'
#  nEventsPerJob = int(sys.argv[1])
#  thisWorkingGroup = sys.argv[2]
#  thisGenerator = sys.argv[3]
#  thisCollision = sys.argv[4]
#  build = sys.argv[5]
#  submitPath = sys.argv[6]
#  macrosPath = sys.argv[7]
#  macrosTopDir = os.path.abspath( macrosPath + '/../..')
#  prodTopDir = sys.argv[8]
#  macrosHash = sys.argv[9]
#  prodSite = sys.argv[10]
#  macrosBranch = sys.argv[11]
#  nTotalEvents = int(sys.argv[12])


def getNumEvtsInFile(theFile):
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeSLURMJob():

    print("Creating SLURM submission files for custom user campaign")

    # Open top-level submit file to write command to
    infile = open(pars.inputFileList, "r")
    line = infile.readline()
    slurmDir = os.path.join(pars.MYDIR, 'slurmJobs')
    os.makedirs(slurmDir, exist_ok=True)
    submitScriptName = os.path.join(slurmDir, 'submitJobs.sh')
    submitScript = open( submitScriptName, "w")
    os.chmod(submitScriptName, 0o744)
    submitScript.write("#!/bin/bash\n")

    # Make output directories
    outputPath     = os.path.join( pars.MYDIR, 'DST' )
    outputLogPath  = os.path.join( pars.MYDIR, 'log')
    os.makedirs(outputPath, exist_ok=True)
    os.makedirs(outputLogPath, exist_ok=True)
    
    # If pars.macrosTopDir is a relative path, then prepend the cwd to it.
    if not pars.macrosTopDir.startswith('/'):
        pars.macrosTopDir = os.path.join(os.getcwd(), pars.macrosTopDir)

    # Make sure script file exists where we think it should relative to cwd
    scriptFile=os.path.join(os.getcwd(),'productions/extras/run_EIC_user.sh')
    if not os.path.exists(scriptFile):
        print('ERROR: Script file not found: ' + scriptFile)
        print('Make sure to run this from the directory containing the "productions" directory!')
        sys.exit()

    # Copy Fun4All_runEvaluators.C to the macros driectory if needed
    # n.b. this is currently kept in the productions repository but I
    # think Cameron may move it to the macros repository at some point.
    scriptFileEvaluators = 'macros/detectors/EICDetector/Fun4All_runEvaluators.C'
    if not os.path.exists( scriptFileEvaluators ):
        tmpFile = os.path.join(os.getcwd(),'productions/extras/Fun4All_runEvaluators.C')
        if os.path.exists( tmpFile ):
            print('Copying ' + tmpFile + ' to ' + scriptFileEvaluators)
            shutil.copy( tmpFile, scriptFileEvaluators )
        else:
            print('ERROR: Script file not found: ' + scriptFileEvaluators)
            print('       and also couldn\'t find: ' + tmpFile)
            print('Make sure to run this from the directory containing the "productions" directory!')
            sys.exit()
            

    # Print input/output info
    print()
    print("Macros directory: {}".format(pars.macrosTopDir))
    print(" Input file list: {}".format(pars.inputFileList))
    print("Output directory: {}".format(outputPath))
    print("   Log directory: {}".format(outputLogPath))
    print()

    # Loop over all input trees and make a submission script that fits the request
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
            if (pars.nTotalEvents>0) and (nEvents >= pars.nTotalEvents): break

            fileBase = inputFile.split('/')[-1].replace('.root', '')
            fileTag = "{0}_{1:03d}_{2:07d}_{3:05d}".format( fileBase,
                                                            fileNumber,
                                                            skip,
                                                            pars.nEventsPerJob)

            slurmOutputInfo = "{0}/slurm-{1}".format(outputLogPath, fileTag)

            outputFile = "DST_{}.root".format(fileTag)
            argument = "{} {} {} {} {}".format(pars.nEventsPerJob,
                                               inputFile,
                                               outputFile,
                                               skip,
                                               outputPath)

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
            slurmFile.write("SCRIPT={}\n".format(scriptFile))
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

            submitScript.write("sbatch {}\n".format(os.path.join(slurmDir, slurmFileName)))

            nJobs += 1
       if (pars.nTotalEvents>0) and (nEvents >= pars.nTotalEvents):
           submitScript.close()
           break
       fileNumber += 1
       line = infile.readline()

    print("\nSLURM submission files have been written to:\n{}".format(slurmDir))
    print("\nThis setup will submit {} jobs".format(nJobs))
    print("\nYou can submit your jobs with the script:\n{}".format(submitScriptName))


makeSLURMJob()
