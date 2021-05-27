import math
import sys, os
from os import environ
from ROOT import TFile, TObjString


nArgs = len(sys.argv)
if nArgs != 9:
    print("Usage: python makeCondorJob <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir>")
    sys.exit()


myShell = str(environ['SHELL'])
goodShells = ['/bin/bash', '/bin/tcsh']
if myShell not in goodShells:
    print("Your shell {} was not recognised".format(myShell))
    sys.exit()


class pars:
  simulationsTopDir = '/sphenix/user/cdean/ECCE/DST_files'
  nEventsPerJob = int(sys.argv[1])
  thisWorkingGroup = sys.argv[2]
  thisGenerator = sys.argv[3]
  thisCollision = sys.argv[4]
  build = sys.argv[5]
  submitPath = sys.argv[6]
  macrosPath = sys.argv[7]
  prodTopDir = sys.argv[8]


def getNumEvtsInFile(theFile):
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()
    #nEvents = inputFile.Get("nEvents")
    #return nEvents.GetString().Atoi()


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
    condorDir = "{}/condorJobs".format(myOutputPath)
    os.makedirs("{}/log".format(condorDir), exist_ok=True)
    submitScriptName = "{}/submitJobs.sh".format(condorDir)
    submitScript = open("{}".format(submitScriptName), "w")
    submitScript.write("#!{}\n".format(myShell))
    #Now make output directory (plus eval folder)
    outputPath = "{}/{}/{}/{}".format(pars.simulationsTopDir, 
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
    while line:
       inputFile = line.replace("\n", "")
       nEventsInFile = getNumEvtsInFile(inputFile)
       nJobsFromFile = math.ceil(nEventsInFile/pars.nEventsPerJob)
       for i in range(nJobsFromFile):

            jobNumber = nJobs
            skip = i*pars.nEventsPerJob

            condorOutputInfo = "{0}/log/condor-{1}_{2}_{3}-{4:05d}".format(condorDir, 
                                                                           pars.thisWorkingGroup, 
                                                                           pars.thisGenerator, 
                                                                           pars.thisCollision, 
                                                                           jobNumber)

            condorFileName = "condorJob_{0}_{1}_{2}-{3:05d}.job".format(pars.thisWorkingGroup, 
                                                                        pars.thisGenerator, 
                                                                        pars.thisCollision, 
                                                                        jobNumber)
            condorFile = open("{0}/{1}".format(condorDir, condorFileName), "w")
            condorFile.write("Universe        = vanilla\n")
            if myShell == '/bin/bash': condorFile.write("Executable      = {}/run_EIC_production.sh\n".format(pars.macrosPath))
            if myShell == '/bin/tcsh': condorFile.write("Executable      = {}/run_EIC_production.csh\n".format(pars.macrosPath))
            outputFile = "DST_{}_{}_{}-{:05d}.root".format(pars.thisWorkingGroup, 
                                                           pars.thisGenerator, 
                                                           pars.thisCollision,
                                                           jobNumber)

            argument = "{} {} {} {} {} {}".format(pars.nEventsPerJob, 
                                                  inputFile, 
                                                  outputFile, 
                                                  skip, 
                                                  outputPath, 
                                                  pars.build)
            condorFile.write("Arguments       = \"{}\"\n".format(argument))
            condorFile.write("Output          = {}.out\n".format(condorOutputInfo))
            condorFile.write("Error           = {}.err\n".format(condorOutputInfo))
            condorFile.write("Log             = {}.log\n".format(condorOutputInfo))
            condorFile.write("Initialdir      = {}\n".format(pars.macrosPath))
            condorFile.write("PeriodicHold    = (NumJobStarts>=1 && JobStatus == 1)\n")
            condorFile.write("request_memory  = 4GB\n")
            condorFile.write("Priority        = 20\n")
            condorFile.write("job_lease_duration = 3600\n")
            condorFile.write("Queue 1\n")

            submitScript.write("condor_submit {}\n".format(condorFileName))

            nJobs += 1
       line = infile.readline()

    print("Condor submission files have been written to:\n{}/condorJobs".format(myOutputPath))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeCondorJob()
