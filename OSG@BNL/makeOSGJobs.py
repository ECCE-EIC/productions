import math
import sys, os
from os import environ
from ROOT import TFile, TObjString


nArgs = len(sys.argv)
if nArgs != 13:
    print("Usage: python makeOSGJob.py <nEventsPerJob> <physics WG> <generator> <collision> <build> <submitPath> <macrosPath> <prodTopDir> <macrosTag> <prodSite> <macrosBranch> <nTotalEvents>")
    sys.exit()


myShell = str(environ['SHELL'])
goodShells = ['/bin/bash', '/bin/tcsh']
if myShell not in goodShells:
    print("Your shell {} was not recognised".format(myShell))
    sys.exit()


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
  macrosBranch = sys.argv[11]
  nTotalEvents = int(sys.argv[12])


def getNumEvtsInFile(theFile):
    inputFile = TFile(theFile)
    return inputFile.Get("EICTree").GetEntries()


def makeCondorJob():
    print("Creating osg submission files for {} production".format(pars.thisWorkingGroup))
    #Find and open the pars.thisWorkingGroup list of input event files
    inputFileList = "{}/inputFileLists/eic-smear_{}_{}_{}.list".format(pars.prodTopDir, 
                                                                       pars.thisWorkingGroup, 
                                                                       pars.thisGenerator, 
                                                                       pars.thisCollision)
    infile = open(inputFileList, "r")
    line = infile.readline()
    #Get the current working directory to write submissions and logs to
    myOutputPath = pars.submitPath #os.getcwd()
    osgDir = "{}/osg@bnlJobs".format(myOutputPath)
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
    nEvents = 0
    while line:
       inputFile = line.replace("\n", "")
       nEventsInFile = getNumEvtsInFile(inputFile)
       nJobsFromFile = math.ceil(nEventsInFile/pars.nEventsPerJob)
       for i in range(nJobsFromFile):

            jobNumber = nJobs
            skip = i*pars.nEventsPerJob
       
            nEvents = nJobs*pars.nEventsPerJob
            if nEvents >= pars.nTotalEvents: break

            fileTag = "{0}_{1}_{2}_{3:03d}_{4:07d}_{5:04d}".format(pars.thisWorkingGroup,
                                                                   pars.thisGenerator,
                                                                   pars.thisCollision,
                                                                   fileNumber,
                                                                   skip,
                                                                   pars.nEventsPerJob)

            osgOutputInfo = "{0}/log".format(osgDir, fileTag)

            osgFileName = "osgJob_{}.xml".format(fileTag)
            osgFile = open("{0}/{1}".format(osgDir, osgFileName), "w")
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
            osgFile.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
            osgFile.write("<job name=\"grid\"   maxEvents=\"{}\"  simulateSubmission=\"false\">\n\n".format(pars.nEventsPerJob))
            osgFile.write("  <command>\n")
            osgFile.write("    <![CDATA[\n")
            osgFile.write("    mv $INPUTFILE0 $SCRATCH/\n\n")
            osgFile.write("    echo \"---------------------- starting setup script -------------------------\"\n")
            osgFile.write("    /bin/cat /cvmfs/eic.opensciencegrid.org/ecce/gcc-8.3/opt/fun4all/core/bin/ecce_setup.sh | /bin/sed 's| sed | /bin/sed |' | /bin/sed 's| awk | /usr/bin/awk |' | /bin/sed 's| find | /usr/bin/find |' | /bin/sed 's| grep | /bin/grep |' > ecce_setup.sh\n")
            osgFile.write("    source ecce_setup.sh -n {}\n".format(pars.build))
            osgFile.write("    echo \"------------------------ done with setup script -----------------------\"\n\n")
            osgFile.write("    /usr/bin/git clone https://github.com/ECCE-EIC/macros.git\n")
            osgFile.write("    cp run_EIC_production.sh macros/detectors/EICDetector\n")
            osgFile.write("    cd macros\n")
            osgFile.write("    /usr/bin/git checkout -b {}\n".format(pars.macrosBranch))
            osgFile.write("    /usr/bin/git branch --set-upstream-to=origin/{0} {0}\n".format(pars.macrosBranch))
            osgFile.write("    /usr/bin/git config --local advice.detachedHead false\n")
            osgFile.write("    /usr/bin/git checkout {}\n".format(pars.macrosHash))
            osgFile.write("    cd detectors/EICDetector\n")
            osgFile.write("    ./run_EIC_production.sh {}\n\n".format(argument))
            osgFile.write("    ]]>\n")
            osgFile.write("  </command>\n\n")
            osgFile.write("  <stdout URL=\"file:./osg-{}.log\"/>\n".format(fileTag))
            osgFile.write("  <stderr URL=\"file:./osg-{}.err\"/>\n".format(fileTag))
            osgFile.write("  <input URL=\"file:{}\"/>\n\n".format(inputFile))
            osgFile.write("  <SandBox installer=\"ZIP\">\n")
            osgFile.write("    <Package name=\"ecce_sim_package\">\n")
            osgFile.write("      <File>file:{}/extras/run_EIC_production.sh</File>\n".format(pars.prodTopDir))
            osgFile.write("   </Package>\n")
            osgFile.write(" </SandBox>\n\n")
            osgFile.write(" <output fromScratch=\"{0}\" toURL=\"{1}/\"/>\n".format(outputFile, outputPath))
            osgFile.write(" <output fromScratch=\"{0}.txt\" toURL=\"{1}/\"/>\n".format(outputFile, outputPath))
            osgFile.write(" <output fromScratch=\"osg-{0}.log\" toURL=\"{1}/\"/>\n".format(fileTag, osgOutputInfo))
            osgFile.write(" <output fromScratch=\"osg-{0}.err\" toURL=\"{1}/\"/>\n".format(fileTag, osgOutputInfo))
            osgFile.write("</job>\n")
            osgFile.close()

            submitScript.write("/cvmfs/sdcc.bnl.gov/software/sums/sums-submit {}\n".format(osgFileName))

            nJobs += 1
       if nEvents >= pars.nTotalEvents: 
           submitScript.close()
           break
       fileNumber += 1
       line = infile.readline()

    print("Condor submission files have been written to:\n{}".format(osgDir))
    print("This setup will submit {} jobs".format(nJobs))
    print("You can submit your jobs with the script:\n{}".format(submitScriptName))


makeCondorJob()
