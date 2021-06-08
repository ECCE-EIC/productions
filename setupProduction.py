import configurations as config
import sys, os


nArgs = len(sys.argv)
if nArgs != 3:
    print("Usage: python setupProduction.py <BNL/JLab/MIT> <path/to/configurationFile>")
    sys.exit()


class steering():
  fileName = sys.argv[2]
  nightly = ""
  macrosTag = ""
  PWG = ""
  generator = ""
  collisionType = ""
  productionTopDir = '/sphenix/user/cdean/ECCE/simulationProductions'
  simulationsDir = productionTopDir
  submissionTopDir = os.getcwd()
  macrosRepo = "https://github.com/ECCE-EIC/macros.git" #"git@github.com:ECCE-EIC/macros.git"
  nEventsPerJob = 1000
  site = sys.argv[1]


if steering.site not in config.sites:
  print("Your submission site, {}, was not recongised".format(steering.site))
  sys.exit()


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

  checkRequirements(steering.PWG, config.ecceWorkingGroup)
  checkRequirements(steering.generator, config.ecceGenerator)
  checkRequirements(steering.collisionType, config.ecceCollision)


def getMacrosRepo():
  steering.simulationsDir += "/{}/{}/{}/ECCE_build_{}/macros_tag_{}".format(steering.PWG,
                                                                            steering.generator,
                                                                            steering.collisionType,
                                                                            steering.nightly,
                                                                            steering.macrosTag)
  if not os.path.isdir(steering.simulationsDir):
    os.makedirs(steering.simulationsDir)
  os.chdir(steering.simulationsDir)
  if not os.path.isdir("{}/macros".format(steering.simulationsDir)):
    os.system("git clone {}".format(steering.macrosRepo))
  os.chdir("macros")
  os.system("git checkout -b production_{}".format(steering.PWG))
  os.system("git branch --set-upstream-to=origin/production_{0} production_{0}".format(steering.PWG))
  os.system("git config --local advice.detachedHead false")
  os.system("git checkout {}".format(config.macrosVersion[steering.macrosTag]))


def setupBNLJob():
  arguments = "{} {} {} {} {} {} {} {} {} {}".format(steering.nEventsPerJob, 
                                                     steering.PWG, 
                                                     steering.generator, 
                                                     steering.collisionType, 
                                                     steering.nightly, 
                                                     submissionProdDir, 
                                                     detectorMacroLocation, 
                                                     steering.submissionTopDir,
                                                     config.macrosVersion[steering.macrosTag],
                                                     steering.site)
  os.system("python {}/{}/makeCondorJobs.py {}".format(steering.submissionTopDir, steering.site, arguments))


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
  if steering.site == "BNL": setupBNLJob()
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
  print("Checking out the correct macros version")
  getMacrosRepo()
  print("Creating production scripts")
  createSubmissionFiles()
  printSimulation()

runProduction()
