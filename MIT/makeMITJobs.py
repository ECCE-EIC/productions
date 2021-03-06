import math
import sys, os, subprocess
from os import environ
from ROOT import TFile, TObjString

generatedDirNameMap = {'/gpfs/mnt/gpfs02/eic':'root://xrootd.cmsaf.mit.edu//store/user/paus/ecce'}

nArgs = len(sys.argv)
if nArgs != 13:
    print("Usage: python makeMITJob.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite> <macrosBranch> <nTotalEvents>")
    sys.exit()
myShell='/bin/bash'

# Path variable descriptions
#
# simulationsTopDir : Directory where output DST files should go
# submitPath        : Directory where the batch scripts are written
# macrosPath        : Directory where Fun4All_G4_EICDetector.C lives ("macros/detector/EICDetector")
# macrosTopDir      : Directory "macros"
# prodTopDir        : Directory where setProduction.py is being run from (typically "productions")

class pars:
    simulationsTopDir = '/home/paus/ecce/mc'
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
    # For some reason pyroot is failing when using xrootd so if 
    #   that is being used, try accessing the file through the filesystem
    inputFile = TFile(theFile)
    nEvents = inputFile.Get("EICTree").GetEntries()
    print(" File %s: %d"%(theFile,nEvents))
    return nEvents


def writeHeader(fileHandle,pars):
    fileHandle.write("executable = " + pars.prodTopDir + "/MIT/ecce_mit.sh\n")
    fileHandle.write("request_cpus = 1\n")
    fileHandle.write("request_memory = 2 GB\n")
    fileHandle.write("request_disk = 3 GB\n")
    fileHandle.write("should_transfer_files  = YES\n")
    fileHandle.write("transfer_input_files   = /tmp/x509up_u5407," + pars.macrosTopDir + "," + pars.prodTopDir + "\n")
    fileHandle.write("#------------------------------------------------------------------\n")
    fileHandle.write("Requirements = ( regexp(\"T3B.*\",MACHINE) )\n")
    fileHandle.write("use_x509userproxy = True\n")
    fileHandle.write("+SkipAllChecks = True\n")
    fileHandle.write("+ProjectName = \"EIC\"\n")
    fileHandle.write("#+SingularityImage = \"/cvmfs/eic.opensciencegrid.org/singularity/rhic_sl7_ext\"\n")
    fileHandle.write("#+SingularityBindCVMFS = True\n")
    fileHandle.write("#+SingularityAutoLoad  = True\n")
    fileHandle.write("#+DESIRED_Sites=\"JLab-FARM-CE\"\n")
    fileHandle.write("log = {}_{}_{}.log\n".format(pars.thisWorkingGroup,pars.thisGenerator,pars.thisCollision))

    return

def addJob(fileHandle,mitOutputInfo,pars,argument):
    fileHandle.write("arguments = run_EIC_production.sh " + pars.simulationsTopDir + " " + argument + "\n")
    fileHandle.write("error = {}.err\n".format(mitOutputInfo))
    fileHandle.write("output = {}.out\n".format(mitOutputInfo))
    fileHandle.write("queue 1\n\n")

    return

def makeMITJob():
    print("Creating MIT condor submission files for {} production".format(pars.thisWorkingGroup))

    # Read the list of input event files
    inputFileList = "{}/inputFileLists/eic-smear_{}_{}_{}.list".format(pars.prodTopDir,
                                                                       pars.thisWorkingGroup,
                                                                       pars.thisGenerator,
                                                                       pars.thisCollision)
    infile = open(inputFileList, "r")
    line = infile.readline()

    # translation map
    for key,val in generatedDirNameMap.items():
        line = line.replace(key, val)

    # Set directory to write submission scripts and logs to
    mitDir = "{}/mitJobs".format(pars.submitPath)
    print(mitDir)
    os.makedirs("{}/log".format(mitDir), exist_ok=True)
    submitScriptName = "{}/submitJobs.sh".format(mitDir)
    submitScript = open("{}".format(submitScriptName), "w")
    os.chmod(submitScriptName,0o744)
    submitScript.write("#!{}\n".format(myShell))

    lfnsFile = open("{}_{}_{}.lfns".format(pars.thisWorkingGroup,pars.thisGenerator,pars.thisCollision), "w")
    subFile =  open("{}_{}_{}.sub".format(pars.thisWorkingGroup,pars.thisGenerator,pars.thisCollision), "w")

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
    outputLogPath  = mitDir + "/log"
    os.makedirs(outputLogPath, exist_ok=True)

    # Print input/output info
    print("Input file list: {}".format(inputFileList))
    print("Output directory: {}".format(outputPath))

    # Now loop over all input trees and make a submission script that fits the request
    nJobs = 0
    fileNumber = 0

    writeHeader(subFile,pars)

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

            mitOutputInfo = "{0}/mit-{1}".format(outputLogPath, fileTag)
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

            lfn = fileTag
            mitFileName = "mitJob_{}.job".format(fileTag)
            mitFile = open("{0}/{1}".format(mitDir, mitFileName), "w")

            mitFile.write("\n")
            mitFile.write("executable     = " + pars.prodTopDir + "/MIT/ecce_mit.sh\n")
            mitFile.write("request_cpus   = 1\n")
            mitFile.write("request_memory = 2 GB\n")
            mitFile.write("request_disk   = 3 GB\n")
            mitFile.write("\n")
            mitFile.write("should_transfer_files  = YES\n")
            mitFile.write("transfer_input_files   = /tmp/x509up_u5407," + pars.macrosTopDir + "," + pars.prodTopDir + "\n")
            mitFile.write("\n")
            mitFile.write("#------------------------------------------------------------------\n")
            mitFile.write("\n")
            mitFile.write("#Requirements = ( MACHINE == \"t3btch095.mit.edu\" ) || ( MACHINE == \"t3btch096.mit.edu\" )\n")
            mitFile.write("Requirements = ( regexp(\"T3B.*\",MACHINE) )\n")
            mitFile.write("use_x509userproxy = True\n")
            mitFile.write("\n")
            mitFile.write("+SkipAllChecks = True\n")
            mitFile.write("+ProjectName = \"EIC\"\n")
            mitFile.write("#+SingularityImage = \"/cvmfs/eic.opensciencegrid.org/singularity/rhic_sl7_ext\"\n")
            mitFile.write("#+SingularityBindCVMFS = True\n")
            mitFile.write("#+SingularityAutoLoad  = True\n")
            mitFile.write("#+DESIRED_Sites=\"JLab-FARM-CE\"\n")

            mitFile.write("arguments = run_EIC_production.sh " + pars.simulationsTopDir + " " + argument + "\n")
            mitFile.write("log = {}.log\n".format(mitOutputInfo))
            mitFile.write("error = {}.err\n".format(mitOutputInfo))
            mitFile.write("output = {}.out\n".format(mitOutputInfo))
            mitFile.write("queue 1\n")
            mitFile.close()

            submitScript.write("condor_submit {}\n".format(mitFileName))
            lfnsFile.write("{}\n".format(lfn))

            addJob(subFile,mitOutputInfo,pars,argument)

            nJobs += 1
        if nEvents >= pars.nTotalEvents: 
            submitScript.close()
            break
        fileNumber += 1
        line = infile.readline()

    print("MIT submission files have been written to:\n{}".format(mitDir))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))

    subFile.close()

makeMITJob()
