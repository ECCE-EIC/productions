import configurations as config
import sys, os, glob, shutil


nArgs = len(sys.argv)
if nArgs != 3:
    print("Usage: python setupProduction.py <BNL/JLAB/MIT> <path/to/configurationFile>")
    sys.exit()

# Path variable descriptions
#
# productionTopDir  : Directory where where this production campaign is being run from
# simulationsDir    : Directory where the "macros" directory will be cloned to (n.b. this is appended to when getMacrosRepo() is called!)
# submissionTopDir  : Directory where this script is being run from (typically "productions")

class steering():
  productionVersion = "prop.5.1_AI"
  fileName = sys.argv[2]
  nightly = ""
  macrosTag = ""
  PWG = ""
  generator = ""
  collisionType = ""
  productionTopDir = '.'
  simulationsDir = productionTopDir
  submissionTopDir = os.getcwd()
  macrosRepo = "https://github.com/ECCE-EIC/macros.git" #"git@github.com:ECCE-EIC/macros.git"
  macrosBranch = "production"
  nEventsPerJob = 2000
  nTotalEvents = 0
  site = sys.argv[1]

if steering.site not in config.sites:
  print("Your submission site, {}, was not recognised".format(steering.site))
  sys.exit()

if steering.site == "JLAB":
  steering.productionTopDir = '/work/eic2/ECCE/PRODUCTION/MACROS'
  steering.simulationsDir = steering.productionTopDir

if steering.site == "OSG":
  steering.productionTopDir = '/work/eic2/ECCE/PRODUCTION/MACROS'
  steering.simulationsDir = steering.productionTopDir

if steering.site == "BNL":
  steering.productionTopDir = '/gpfs/mnt/gpfs02/eic/DATA/ECCE_Productions/simulationProductions'
  steering.simulationsDir = steering.productionTopDir

if steering.site == "OSG@BNL":
  steering.productionTopDir = 'N/A'
  steering.simulationsDir = steering.productionTopDir

def getParameter(parameter):
  configFile = open(steering.fileName, "r")
  line = configFile.readline()
  setting = ""
  while line:
    splitLine = line.replace("\n", "").split(" ")
    if splitLine[0] == parameter:
      setting = splitLine[1]
    line = configFile.readline()
  if not setting:
    print("The parameter, {}, was not found in {}".format(parameter, configFile.name))
    sys.exit()
  return setting


def checkRequirements(parameter, parList):
  if parameter not in parList:
    print("Parameter {} was not recognised".format(parameter))
    sys.exit()


def getProductionRequirements():
  if not os.path.isfile(steering.fileName):
    print("Your production setup, {}, does not exist".format(steering.fileName))
    sys.exit()

  steering.nightly = getParameter("nightly")
  steering.macrosTag = getParameter("tag")
  steering.PWG = getParameter("PWG")
  steering.generator = getParameter("generator")
  steering.collisionType = getParameter("collision")
  steering.nTotalEvents = getParameter("nTotalEvents")
  #if "singlePion" in steering.collisionType: steering.macrosBranch = "production_singlePion_0-20GeV"
  #if "singleElectron" in steering.collisionType: steering.macrosBranch = "production_singleElectron_0-20GeV"
  if "pythia8" in steering.generator: steering.macrosBranch = "production_pythia8"
  if "particleGun" in steering.generator: steering.macrosBranch = "production_singleParticle_0-20GeV"
  if "AI" in steering.PWG: steering.macrosBranch = "production_AI_Optimization"

  checkRequirements(steering.PWG, config.ecceWorkingGroup)
  checkRequirements(steering.generator, config.ecceGenerator)
  checkRequirements(steering.collisionType, config.ecceCollision)

def getMacrosRepo():
  steering.simulationsDir += "/ECCE_build_{}/macros_tag_{}".format(steering.nightly,
                                                                   steering.macrosTag)
  if not os.path.isdir(steering.simulationsDir):
    os.makedirs(steering.simulationsDir)
  os.chdir(steering.simulationsDir)
  if not os.path.isdir("{}/macros".format(steering.simulationsDir)):
    os.system("git clone {}".format(steering.macrosRepo))
  os.chdir("macros")
  if steering.macrosBranch != "master":
    os.system("git checkout -b {}".format(steering.macrosBranch))
  os.system("git branch --set-upstream-to=origin/{0} {0}".format(steering.macrosBranch))
  os.system("git config --local advice.detachedHead false")
  os.system("git checkout {}".format(config.macrosVersion[steering.macrosTag]))
  
  # Copy all files from productions/extras into the macros directory
  # Take care not to overwrite any files. In particular the Fun4All_runEvaluators.C
  # file exists in both places. We always keep the on in macros.
  extrasDir = steering.submissionTopDir + '/extras'
  os.chmod("{}/changeStrings.sh".format(extrasDir), 0o744)
  os.chmod("{}/setupFun4All_G4_EICDetector.sh".format(extrasDir), 0o744)
  os.chmod("{}/setupPionGun.sh".format(extrasDir), 0o744)
  os.chmod("{}/run_EIC_production.sh".format(extrasDir), 0o744)
  os.chmod("{}/setupElectronGun.sh".format(extrasDir), 0o744)
  destDir = os.getcwd() + '/detectors/EICDetector'
  if os.path.isdir(extrasDir):
    for f in glob.glob( '%s/*' % extrasDir ):
      destFile = os.path.join(destDir, os.path.basename(f))
      if not os.path.exists( destFile ):
        if not os.path.isdir(f) :
            print('copying %s  ->  %s' % (f,destFile))
            shutil.copy( f, destFile )
        else:
             print('skipping copy of directory: %s  from extras' % os.path.basename(f) )
      else:
        print('skipping copy of %s since it would overwrite file already in macros directory' % os.path.basename(f) )

  # Create tarball of macros directory
  os.chdir(steering.simulationsDir)
  cmd = 'tar czf %s.tgz macros' % os.path.basename(steering.simulationsDir)
  print(cmd)
  os.system(cmd)

def setupJob():
  steering.productionVersion = steering.macrosTag[0:8]
  arguments = "{} {} {} {} {} {} {} {} {} {} {} {} {}".format(steering.nEventsPerJob, 
                                                              steering.PWG, 
                                                              steering.generator, 
                                                              steering.collisionType, 
                                                              steering.nightly, 
                                                              submissionProdDir, 
                                                              detectorMacroLocation, 
                                                              steering.submissionTopDir,
                                                              config.macrosVersion[steering.macrosTag],
                                                              steering.site, 
                                                              steering.macrosBranch,
                                                              steering.nTotalEvents,
                                                              steering.productionVersion)

  submitScript = ""
  if steering.site == "BNL": submitScript = "makeCondorJobs.py"
  elif steering.site == "JLAB": submitScript = "makeSLURMJobs.py"
  elif steering.site == "OSG": submitScript = "makeOSGJobs.py"
  elif steering.site == "OSG@BNL": submitScript = "makeOSGJobs.py"
  else:  print("No submission scripts are implemented for the site, {}".format(steering.site))
  cmd = "python {0}/{1}/{2} {3}".format(steering.submissionTopDir, steering.site, submitScript, arguments)
  print(cmd)
  os.system(cmd)


def createSubmissionFiles():
  global submissionProdDir
  global detectorMacroLocation
  submissionProdDir = "{}/submissionFiles/{}/{}/{}".format(steering.submissionTopDir, 
                                                           steering.PWG, 
                                                           steering.generator, 
                                                           steering.collisionType)
  os.makedirs(submissionProdDir, exist_ok=True)
  os.chdir(submissionProdDir)
  detectorMacroLocation = "{}/macros/detectors/EICDetector".format(steering.simulationsDir)
  if steering.site == "BNL" or steering.site == "JLAB" or steering.site == "OSG" or steering.site == "OSG@BNL": setupJob()
  else:  print("No submission scripts are implemented for the site, {}".format(steering.site))


def printSimulation():
  print("====== Your production details ======")
  print("ECCE nightly: {}".format(steering.nightly))
  print("ECCE macros repo: {}".format(steering.macrosRepo))
  print("ECCE macros tag: {}, hash: {}".format(steering.macrosTag, config.macrosVersion[steering.macrosTag]))
  print("ECCE macros directory: {}".format(steering.simulationsDir))
  print("PWG: {}".format(steering.PWG))
  print("Generator: {}".format(steering.generator))
  print("Collision Type: {}".format(steering.collisionType))
  print("Number of events per file: {}".format(steering.nEventsPerJob))
  print("====================================") 


def runProduction():
  print("Getting production requirements")
  getProductionRequirements()
  if steering.site != "OSG@BNL":
      print("Checking out the correct macros version")
      getMacrosRepo()
  print("Creating production scripts")
  createSubmissionFiles()
  printSimulation()

runProduction()
