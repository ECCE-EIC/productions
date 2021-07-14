#---------------------------------------------------------------------------------------------------
# Python Module File to describe out production environment.
#
# Author: C.Paus                                                                      (Jul 07, 2021)
#---------------------------------------------------------------------------------------------------
import os,sys
import getpass

DEBUG = 0

#---------------------------------------------------------------------------------------------------
"""
Class:  GenFile(location='undefined', fileName='undefined', nEvents=2000000)

Each generator input file can be described by this class. Very important: file names have to be
unique. Even if the location is different fileName has to be unique.
"""
#---------------------------------------------------------------------------------------------------
class GenFile:
    "Description of a Generator Input file"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,location='/tmp',fileName='ep_noradcor.18x100lowq_run001.root',nEvents=2000000):
        self.location = location
        self.fileName = fileName
        self.nEvents = nEvents

    #-----------------------------------------------------------------------------------------------
    # present what we have
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print(" File: %s in %s (nEvts: %d)"%(self.fileName,self.location,self.nEvents))

#---------------------------------------------------------------------------------------------------
"""
Class:  LogAnalyzer(request)

Each request can be analyzed by using the available log files.
"""
#---------------------------------------------------------------------------------------------------
class LogAnalyzer:
    "Description of a log file analyzer based on a given request"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,request):
        self.request = request
        self.timings = {}
        self.dstTimings = {}
        self.evalTimings = {}

        self.timingTags = { ' START --':0, ' END --':0,
                            ' START DST --':0, ' END DST --':0,
                            ' START EVAL --':0, ' END EVAL --':0 }

    #-----------------------------------------------------------------------------------------------
    # present what we have
    #-----------------------------------------------------------------------------------------------
    def findLogs(self):
        penvLog = "{}/{}_{}/{}".format(os.getenv('PENV_LOG'),\
                                       self.request.tag,self.request.hash,\
                                       self.request.sample.dataset)
        print(' Log area: %s'%(penvLog))
        for fileName in os.listdir(penvLog):
            if fileName.endswith(".out"):
                self.processTiming(penvLog,fileName)

        return
                
    def processTiming(self,dirName,fileName):
        # reset
        for key in self.timingTags:
            self.timingTags[key] = 0
        # read data
        with open("%s/%s"%(dirName,fileName),'r') as fH:
            data = fH.read()
        # process the data
        for line in data.split('\n'):
            for key in self.timingTags:
                if key in line:
                    value = line.split(' ')[-1]
                    #print(" Value (%s): %s (line: %s)"%(key,value,line))
                    self.timingTags[key] = int(value)

        self.timings[fileName] = self.timingTags[' END --'] - self.timingTags[' START --']
        self.dstTimings[fileName] = self.timingTags[' END DST --'] - self.timingTags[' START DST --']
        self.evalTimings[fileName] = self.timingTags[' END EVAL --'] - self.timingTags[' START EVAL --']
                        
    #-----------------------------------------------------------------------------------------------
    # present what we have
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print("\n ==== L o g A n a l y z e r  for Request ====")
        self.request.show()
        avg = 0.
        avgDst = 0.
        avgEval = 0.
        for key in sorted(self.timings.iterkeys()):
            print(" %s: DST %d - EVAL %d  == TOTAL %d"\
                  %(key,self.dstTimings[key],self.evalTimings[key],self.timings[key]))
            avg += float(self.timings[key])
            avgDst += float(self.dstTimings[key])
            avgEval += float(self.evalTimings[key])
        if len(self.dstTimings) > 0:
            print(" Averages: DST %f - EVAL %f  == TOTAL %f"\
                  %(avgDst/len(self.dstTimings),avgEval/len(self.evalTimings),avg/len(self.timings)))

#---------------------------------------------------------------------------------------------------
"""
Class:  Request(tag='undefined', hash='undefined', sample)

A request includes a specific configuration (tag and hash) and a sample to be processed.
"""
#---------------------------------------------------------------------------------------------------
class Request:
    "Description of a Request"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,tag,hash,sample):
        self.tag = tag
        self.hash = hash
        self.sample = sample

        self.loadCondorStatus(1) # queued
        self.loadCondorStatus(2) # running
        self.loadCondorStatus(3) # removed (should rarely occur)
        self.loadCompletedJobs() # condor does not keep completion, test whether outputfile exists
        self.loadCondorStatus(5) # held

    #-----------------------------------------------------------------------------------------------
    # load all jobs that are completed (this is MIT specific, but can be easily replaced)
    #-----------------------------------------------------------------------------------------------
    def loadCompletedJobsMit(self):

        # using MIT specific buffer location (T2)
        cmd = 'list /cms/store/user/paus/%s/%s/%s/%s/%s | grep .root$'\
              %(self.tag,self.hash,self.sample.physicsGroup,self.sample.generator,self.sample.collisions)
        if DEBUG > 0:
            print("CMD: %s"%cmd)
        for line in os.popen(cmd).readlines():
            f = line[:-1].split('/')
            lfn = f[-1]
            lfn = lfn.replace('.root','')
            lfn = lfn.replace('DST_','')
            if DEBUG > 0:
                print(' COMPLETED: %s'%(lfn))
            self.sample.addStatus(lfn,4)

    #-----------------------------------------------------------------------------------------------
    # load all jobs that are completed based on the BNL minIo (S3) storage
    #-----------------------------------------------------------------------------------------------
    def loadCompletedJobs(self):

        # using the minio output location
        cmd = 'mcs3 ls S3/eictest/ECCE/MC/%s/%s/%s/%s/%s | grep .root$'\
              %(self.tag,self.hash,self.sample.physicsGroup,self.sample.generator,self.sample.collisions)
        if DEBUG > 0:
            print("CMD: %s"%cmd)
        for line in os.popen(cmd).readlines():
            f = line[:-1].split(' ')
            lfn = f[-1]
            lfn = lfn.replace('.root','')
            lfn = lfn.replace('DST_','')
            if DEBUG > 0:
                print(' COMPLETED: %s'%(lfn))
            self.sample.addStatus(lfn,4)

    #-----------------------------------------------------------------------------------------------
    # load all jobs that are queued (again specific condor but can be easily replaced: condor, slurm, ..)
    #-----------------------------------------------------------------------------------------------
    def loadCondorStatus(self,status):

        # initialize from scratch
        user = str(getpass.getuser())
        cmd = 'condor_q %s -global -constraint JobStatus==%d'%(user,status) \
              + ' -format \'%s\n\' Args 2> /dev/null' \
              + '| grep \'%s %s\''%(self.tag,self.hash) \
              + '| grep \'%s %s %s\''%(self.sample.physicsGroup,self.sample.generator,self.sample.collisions)
        if DEBUG > 0:
            print("CMD: %s"%cmd)
        for line in os.popen(cmd).readlines():
            f = line[:-1].split(' ')
            lfn = "%s_%s_%s_%s_%s_%s"%(f[6],f[7],f[8],f[5],f[3],f[4])
            if DEBUG > 0:
                print(' Status==%d: %s'%(status,lfn))
            self.sample.addStatus(lfn,status)

    #-----------------------------------------------------------------------------------------------
    # present what we have
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print("")
        print(" Request uses Tag: %s  Hash: %s"%(self.tag,self.hash))
        self.sample.show()

#---------------------------------------------------------------------------------------------------
"""
Class:  Sample(inputDir, physicsGroup, generator, collisions, nEventsPerLfn=2000)

Each sample we are producing can be described by this class.
"""
#---------------------------------------------------------------------------------------------------
class Sample:
    "Description of a datasample to be produced"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self, inputDir, physicsGroup, generator, collisions, nEventsPerLfn):

        # copy the key parameters
        self.inputDir = inputDir
        self.physicsGroup = physicsGroup
        self.generator = generator
        self.collisions = collisions

        # derive
        self.dataset = "{}_{}_{}".format(self.physicsGroup,self.generator,self.collisions)
        self.genInput = '%s/%s_%s_%s.list'%(self.inputDir,self.physicsGroup,self.generator,self.collisions)
        self.nEventsPerLfn = nEventsPerLfn

        # define the content container
        self.genFiles = []
        self.nEventsTotal = 0
        self.allLfns = {}           # 0-missing, 1-queued, 2-running, 3-removed, 4-completed, 5-held

        # read the generator input files
        self.loadGenInput()

        # generate all resulting lfns
        self.makeLfns()

    #-----------------------------------------------------------------------------------------------
    # add status of one lfn
    #-----------------------------------------------------------------------------------------------
    def addStatus(self,lfn,status):
        if lfn in self.allLfns.keys():
            if self.allLfns[lfn] != 0:
                print(" WARNING -- lfn (%s) found in non-zero state: %d --> %d"\
                      %(lfn,self.allLfns[lfn],status))
            self.allLfns[lfn] = status
        else:
            print(" ERROR -- found lfn (%s) not in the list of all lfns."%lfn)
            print(" CRASH: %d"%(self.allLfns[lfn]))

    #-----------------------------------------------------------------------------------------------
    # read the generator input files
    #-----------------------------------------------------------------------------------------------
    def loadGenInput(self):

        # give notice that file already exists
        if os.path.exists(self.genInput):
            if DEBUG > 0:
                print(" INFO -- generator input file found: %s."%(self.genInput))
        else:
            print(" ERROR -- generator input file not found: %s."%(self.genInput))

        with open(self.genInput,'r') as fH:
            data = fH.read()

        for line in data.split('\n'):
            f = line.split(' ')
            if len(f) == 1 and f[0] != '':
                g = f[0].split('/')
                gF = GenFile("/".join(g[:-1]),g[-1],2000000)
                print(" WARNING -- line (%s) needs to contain 2 parameters (<fileName> <nEventsInFile>). Hardwired 2M for now!!"%line)
                self.genFiles.append(gF)
                self.nEventsTotal += gF.nEvents
            elif len(f) == 2:
                g = f[0].split('/')
                gF = GenFile("/".join(g[:-1]),g[-1],int(f[1]))
                self.genFiles.append(gF)
                self.nEventsTotal += gF.nEvents
            else:
                pass
                #print(" ERROR -- line (%s) needs to contain 2 parameters (<fileName> <nEventsInFile>)!"%line)

        return

    #-----------------------------------------------------------------------------------------------
    # generate the file ids that we need to produce
    #
    # IMPORTANT: if there are not enough events for a last job the events are not used, jobs with
    #            number of events smaller than requested are not made, this could be problematic
    #            if the *generated* luminosity is counted.
    # -----------------------------------------------------------------------------------------------
    def makeLfns(self):

        i = 0
        for gF in self.genFiles:
            nSkip = 0
            if DEBUG > 0:
                print(" Processing(%d): %s"%(i,gF.fileName))
            while (nSkip+self.nEventsPerLfn <= gF.nEvents):
                lfn = "%s_%03d_%07d_%05d"%(self.dataset,i,nSkip,self.nEventsPerLfn)
                self.allLfns[lfn] = 0
                nSkip += self.nEventsPerLfn
                if DEBUG > 0:
                    print(' ALL: %s'%(lfn))
            i+=1

    #-----------------------------------------------------------------------------------------------
    # present the current samples
    #-----------------------------------------------------------------------------------------------
    def show(self):
        print('')
        print(' ====  S a m p l e  ====')
        print(' Dataset       : ' + self.dataset)
        for gf in self.genFiles:
            gf.show()
        if DEBUG > 1:
            for lfn in self.allLfns:
                if self.allLfns[lfn] == 0:
                    print(" -Missing-> %s (%d)"%(lfn,self.allLfns[lfn]))

#---------------------------------------------------------------------------------------------------
"""
Class:  Submitter()

This is the engine that will allow us to submit requests which are based on a particular release
and specific samples. It is important to note that the release (defined by hash and tag) could be
changed on the fly but it requires at this point some acrobatics to do this. So, in essence it is
recommended to use only one release with a given installation.
"""
#---------------------------------------------------------------------------------------------------
class Submitter:
    "Description of a job submitter"

    #-----------------------------------------------------------------------------------------------
    # constructor
    #-----------------------------------------------------------------------------------------------
    def __init__(self,id):
        self.id = id
        self.submitFile = ""

    def submit(self,request,execute):
        # make the work directory
        penvTgz = "penv_%s_%s.tgz"%(request.tag,request.hash)
        penvBase = "{}".format(os.getenv('PENV_BASE'))
        penvLog = "{}/{}_{}/{}"\
            .format(os.getenv('PENV_LOG'),request.tag,request.hash,request.sample.dataset)
        if not os.path.exists(penvLog):
            os.makedirs(penvLog)
        # move the relevant files if they are not already there
        if not os.path.exists("%s/%s"%(penvLog,penvTgz)):
            os.system("cp %s/../%s %s"%(penvBase,penvTgz,penvLog))
        if not os.path.exists("%s/ecce_simulate.sh"%penvLog):
            os.system("cp %s/bin/ecce_simulate.sh %s"%(penvBase,penvLog))
        self.submitFile = "{}/{}_{}.sub".format(penvLog,request.sample.dataset,self.id)
        (nMissing,nQueued,nRunning,nRemoved,nCompleted,nHeld) = self._writeSubmitFile(request)

        if (nMissing > 0):
            # now push it into condor
            cmd = "cd %s; condor_submit %s"\
                  %("/".join(self.submitFile.split('/')[:-1]),self.submitFile.split('/')[-1])
            print(" --> %s"%(cmd))
            if execute:
                os.system(cmd)
            else:
                print(" This was just a test run, no jobs were submitted.")
        else:
            print("\n There are no missing jobs. We are all set.\n")

        return

    #-----------------------------------------------------------------------------------------------
    # -- internal --
    #-----------------------------------------------------------------------------------------------

    def _addJob(self,fileHandle,lfn,argument):
        fileHandle.write("arguments = %s\n"%(argument))
        fileHandle.write("error = {}.err\n".format(lfn))
        fileHandle.write("output = {}.out\n".format(lfn))
        fileHandle.write("queue 1\n\n")
    
        return

    def _writeHeader(self,fileHandle,request):
        fileHandle.write("executable = ecce_simulate.sh\n")
        fileHandle.write("request_cpus = 1\n")
        fileHandle.write("request_memory = 2 GB\n")
        fileHandle.write("request_disk = 3 GB\n")
        fileHandle.write("should_transfer_files = YES\n")
        fileHandle.write("transfer_input_files = penv_%s_%s.tgz\n"%(request.tag,request.hash))
        fileHandle.write("GetEnv = False\n")
        fileHandle.write("#------------------------------------------------------------------\n")
        fileHandle.write("Requirements = %s\n"%(os.getenv('PENV_CONDOR_REQ')))
        fileHandle.write("use_x509userproxy = True\n")
        fileHandle.write("+SkipAllChecks = True\n")
        fileHandle.write("+ProjectName = \"EIC\"\n")
        fileHandle.write("#+SingularityImage = \"/cvmfs/eic.opensciencegrid.org/singularity/rhic_sl7_ext\"\n")
        fileHandle.write("#+SingularityBindCVMFS = True\n")
        fileHandle.write("#+SingularityAutoLoad  = True\n")
        fileHandle.write("#+DESIRED_Sites=\"JLab-FARM-CE\"\n")
        fileHandle.write("log = {}.log\n\n".format(request.sample.dataset))
    
        return

    def _writeSubmitFile(self,request):
        print('')
        print(" Submit file: %s"%(self.submitFile))
        with open(self.submitFile,'w') as fH:
            self._writeHeader(fH,request)
            nMissing = 0
            nQueued = 0
            nRunning = 0
            nRemoved = 0
            nCompleted = 0
            nHeld = 0
            for lfn in sorted(request.sample.allLfns.iterkeys()):
                if request.sample.allLfns[lfn] == 0:
                    # recover pertinent information from the lfn
                    fid = lfn.split("_")[-3]
                    nskip = lfn.split("_")[-2]
                    nevts = lfn.split("_")[-1]
                    nevts.replace(".root","")
                    inputFile = "%s/%s"%(request.sample.genFiles[int(fid)].location,
                                         request.sample.genFiles[int(fid)].fileName)
                    # from ecce_simulate.sh:
                    # tag="$1" hash="$2" inputFile="$3" nskip="$4" nevts="$5" fid="$6" pwg="$7"
                    # gen="$8" coll="$9"
                    args = "%s %s %s %s %s %s %s %s %s"%\
                           (request.tag,request.hash,inputFile,nskip,nevts,fid, \
                            request.sample.physicsGroup,request.sample.generator, \
                            request.sample.collisions)
                    self._addJob(fH,lfn,args)
                    nMissing += 1
                elif request.sample.allLfns[lfn] == 1:
                    nQueued += 1
                elif request.sample.allLfns[lfn] == 2:
                    nRunning += 1
                elif request.sample.allLfns[lfn] == 3:
                    nRemoved += 1
                elif request.sample.allLfns[lfn] == 4:
                    nCompleted += 1
                elif request.sample.allLfns[lfn] == 5:
                    nHeld += 1

        print('')
        print(" ====  J o b   S u m m a r y  ==== ")
        print(" Adding to queue: %d"%(nMissing))
        print(" ----------------")
        print(" Queued         : %d"%(nQueued))
        print(" Running        : %d"%(nRunning))
        print(" Removed        : %d"%(nRemoved))
        print(" Completed      : %d"%(nCompleted))
        print(" Held           : %d"%(nHeld))
        print(" ================")
        print(" Total counts   : %d"%(len(request.sample.allLfns)))

        return (nMissing,nQueued,nRunning,nRemoved,nCompleted,nHeld)
