import math
import sys, os
from os import environ
from ROOT import TFile, TObjString


nArgs = len(sys.argv)
if nArgs != 13:
    print("Usage: python makeCondorJob.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite> <macrosBranch> <nTotalEvents>")
    sys.exit()


myShell = str(environ['SHELL'])
goodShells = ['/bin/bash', '/bin/tcsh']
if myShell not in goodShells:
    print("Your shell {} was not recognised".format(myShell))
    sys.exit()


class pars:
  simulationsTopDir = '/gpfs/mnt/gpfs02/eic/DATA/ECCE_Productions/MC'
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
  macrosBranch = sys.argv[11]
  nTotalEvents = int(sys.argv[12])


def getNumEvtsInFile(theFile):
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeCondorJob():
    print("Creating condor submission files for {} production".format(pars.thisWorkingGroup))
    #Find and open the pars.thisWorkingGroup list of input event files
    inputFileList = "{}/inputFileLists/eic-smear_{}_{}_{}.list".format(pars.prodTopDir, 
                                                                       pars.thisWorkingGroup, 
                                                                       pars.thisGenerator, 
                                                                       pars.thisCollision)
    infile = open(inputFileList, "r")
    line = infile.readline()
    #Get the current working directory to write submissions and logs to
    myOutputPath = pars.submitPath #os.getcwd()
    #Now make output directory
    outputPath = "{}/{}/{}/{}/{}/{}".format(pars.simulationsTopDir, 
                                            pars.build,
                                            pars.macrosHash,
                                            pars.thisWorkingGroup, 
                                            pars.thisGenerator, 
                                            pars.thisCollision)
    os.makedirs(outputPath, exist_ok=True)
    #condorDir = "{}/condorJobs".format(myOutputPath)
    condorDir = "{}/condorJobs".format(outputPath)
    os.makedirs("{}/log".format(condorDir), exist_ok=True)
    submitScriptName = "{}/submitJobs.sh".format(condorDir)
    submitScript = open("{}".format(submitScriptName), "w")
    os.chmod(submitScriptName, 0o744)
    submitScript.write("#!{}\n".format(myShell))
    #Print input/output info
    print("Input file list: {}".format(inputFileList))
    print("Output directory: {}".format(outputPath))
    #Now loop over all input trees and make a submission script that fits the request
    nJobs = 0
    fileNumber = 0
    nEvents = 0
    while line:
       inputFile = line.replace("\n", "")
       if pars.thisGenerator != "particleGun":
         nEventsInFile = getNumEvtsInFile(inputFile)
       else:
         nEventsInFile = pars.nTotalEvents
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

            condorOutputInfo = "{0}/log/condor-{1}".format(condorDir, fileTag)

            condorFileName = "condorJob_{}.job".format(fileTag)
            condorFile = open("{0}/{1}".format(condorDir, condorFileName), "w")
            condorFile.write("Universe        = vanilla\n")
            if myShell == '/bin/bash': condorFile.write("Executable      = {}/run_EIC_production.sh\n".format(pars.macrosPath))
            if myShell == '/bin/tcsh': condorFile.write("Executable      = {}/run_EIC_production.csh\n".format(pars.macrosPath))
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
            condorFile.write("Arguments       = \"{}\"\n".format(argument))
            condorFile.write("Output          = {}.out\n".format(condorOutputInfo))
            condorFile.write("Error           = {}.err\n".format(condorOutputInfo))
            condorFile.write("Log             = {}.log\n".format(condorOutputInfo))
            condorFile.write("Initialdir      = {}\n".format(pars.macrosPath))
            condorFile.write("PeriodicHold    = (NumJobStarts>=1 && JobStatus == 1)\n")
            condorFile.write("request_memory  = 2GB\n")
            condorFile.write("Priority        = 20\n")
            condorFile.write("job_lease_duration = 3600\n")
            condorFile.write("Queue 1\n")
            condorFile.close()

            submitScript.write("condor_submit {}\n".format(condorFileName))

            nJobs += 1
       if nEvents >= pars.nTotalEvents: 
           submitScript.close()
           break
       fileNumber += 1
       line = infile.readline()

    print("Condor submission files have been written to:\n{}".format(condorDir))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeCondorJob()
