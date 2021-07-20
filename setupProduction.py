import configurations as config
import sys, os


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
  fileName = sys.argv[2]
  nightly = ""
  macrosTag = ""
  PWG = ""
  generator = ""
  collisionType = ""
  productionTopDir = '/work/eic/users/davidl/2021.06.17.test_campaign'
  simulationsDir = productionTopDir
  submissionTopDir = os.getcwd()
  macrosRepo = "https://github.com/ECCE-EIC/macros.git" #"git@github.com:ECCE-EIC/macros.git"
  macrosBranch = "production"
  nEventsPerJob = 1000
  nTotalEvents = 0
  site = sys.argv[1]

if steering.site not in config.sites:
  print("Your submission site, {}, was not recognised".format(steering.site))
  sys.exit()

if steering.site == "BNL":
  steering.productionTopDir = '/gpfs/mnt/gpfs02/eic/DATA/ECCE_Productions/simulationProductions'
  steering.simulationsDir = steering.productionTopDir

if steering.site == "OSG@BNL":
  steering.productionTopDir = 'N/A'
  steering.simulationsDir = steering.productionTopDir

if steering.collisionType == "singlePion": steering.macrosBranch = "production_singlePion_0-20GeV"
if steering.collisionType == "singleElectron": steering.macrosBranch = "production_singleElectron_0-20GeV"
if steering.generator == "pythia8": steering.macrosBranch = "production_pythia8"

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

  checkRequirements(steering.PWG, config.ecceWorkingGroup)
  checkRequirements(steering.generator, config.ecceGenerator)
  checkRequirements(steering.collisionType, config.ecceCollision)

def getMacrosRepo():

  if steering.generator == "particleGun":
    steering.simulationsDir += "/particleGun"
    if steering.collisionType == "singlePion":
      steering.simulationsDir += "/singlePion"
    elif steering.collisionType == "singleElectron":
      steering.simulationsDir += "/singleElectron"
    else:
      print("You cannot have beam condition {} with a particle gun".format(steering.collisionType))
      sys.exit()

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
  extrasDir = steering.submissionTopDir + '/extras'
  os.chmod("{}/changeStrings.sh".format(extrasDir), 0o744)
  os.chmod("{}/setupFun4All_G4_EICDetector.sh".format(extrasDir), 0o744)
  os.chmod("{}/setupPionGun.sh".format(extrasDir), 0o744)
  os.chmod("{}/run_EIC_production.sh".format(extrasDir), 0o744)
  os.chmod("{}/setupElectronGun.sh".format(extrasDir), 0o744)
  if os.path.isdir(extrasDir):
    cmd = 'cp %s/* %s' % (extrasDir, os.getcwd() + '/detectors/EICDetector')
    print(cmd)
    os.system(cmd)


def setupJob():
  arguments = "{} {} {} {} {} {} {} {} {} {} {} {}".format(steering.nEventsPerJob, 
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
                                                           steering.nTotalEvents)

  submitScript = ""
  if steering.site == "BNL": submitScript = "makeCondorJobs.py"
  elif steering.site == "JLAB": submitScript = "makeSLURMJobs.py"
  elif steering.site == "OSG": submitScript = "makeOSGJobs.py"
  elif steering.site == "OSG@BNL": submitScript = "makeOSGJobs.py"
  else:  print("No submission scripts are implemented for the site, {}".format(steering.site))
  os.system("python {0}/{1}/{2} {3}".format(steering.submissionTopDir, steering.site, submitScript, arguments))


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
